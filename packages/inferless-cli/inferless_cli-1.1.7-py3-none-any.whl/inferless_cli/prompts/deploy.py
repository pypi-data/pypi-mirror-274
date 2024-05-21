import time
import os
import tempfile
import typer

from inferless_cli.utils.exceptions import ModelImportException
from inferless_cli.utils.helpers import (
    create_yaml,
    create_zip_file,
    decrypt_tokens,
    get_current_mode,
    get_default_machine_values,
    is_inferless_yaml_present,
    log_exception,
    read_json,
    read_yaml,
    yaml,
)
import rich
from rich.progress import Progress, SpinnerColumn, TextColumn
from inferless_cli.utils.services import (
    get_model_import_details,
    get_workspaces_list,
    import_model,
    set_env_variables,
    update_model_configuration,
    upload_io,
    validate_import_model,
    start_import_model,
    upload_file,
    validate_github_url_permissions,
    create_presigned_io_upload_url,
)

from inferless_cli.utils.constants import GITHUB, GIT


def deploy_local(config_file_name, redeploy):
    is_yaml_present = is_inferless_yaml_present(config_file_name)
    old_response = None
    is_failed = False
    if is_yaml_present and not redeploy:
        config = read_yaml(config_file_name)
        _, _, _, workspace_id, _ = decrypt_tokens()

        if (
            config
            and "configuration" in config
            and "is_serverless" in config["configuration"]
            and config["configuration"]["is_serverless"]
        ):
            try:
                workspaces = get_workspaces_list()
            except Exception as e:
                rich.print(e)
                raise typer.Exit(1)
            allow_serverless = False
            for workspace in workspaces:
                if workspace["id"] == workspace_id:
                    allow_serverless = workspace["allow_serverless"]
                    break
            if not allow_serverless:
                email_address = "nilesh@inferless.com"
                rich.print(
                    f"[red]Serverless is not enabled for your account [yellow](beta feature)[/yellow][/red] \nplease contact [blue]{email_address}[/blue]",
                )
                raise typer.Abort(1)

        temp_model_id = config.get("model_import_id")
        if "model_import_id" in config:
            try:
                old_response = get_model_import_details(config.get("model_import_id"))
            except Exception as e:
                rich.print(e)
                raise typer.Exit(1)
        if old_response and old_response.get("model_import").get("status") == "FAILURE":
            is_failed = True
        if temp_model_id and not is_failed:
            rich.print(
                f"[red]model_import_id already exists in {config_file_name}.[/red] \nremove model_import_id from the {config_file_name} file for the new deployment and run command [blue]`inferless deploy`[/blue]\n"
            )
            rich.print(
                "if you want to redeploy the model please use this command [blue]`inferless model rebuild -l`[/blue]\n"
            )
            raise typer.Abort(1)
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        description_1 = (
            "Deploying from local directory (make sure you have saved your code)"
        )
        if redeploy:
            description_1 = (
                "Redeploying from local directory  (make sure you have saved your code)"
            )
        rich.print(description_1)
        task_id = progress.add_task(description="Getting warmed up...", total=None)
        config = read_yaml(config_file_name)

        if not redeploy and "model_import_id" in config and not is_failed:
            rich.print(
                f"[red]model_import_id already exists in {config_file_name}[/red]"
            )
            raise typer.Abort(1)

        if redeploy and "model_import_id" not in config:
            rich.print(
                f"[red]model_import_id not found in {config_file_name}[/red]. To deploy run command [blue]`inferless deploy`[/blue]"
            )
            raise typer.Abort(1)

        if redeploy and "model_import_id" in config:
            try:
                old_response = get_model_import_details(config.get("model_import_id"))
            except Exception as e:
                rich.print(e)
                raise typer.Exit(1)
            if config.get("name") != old_response.get("model_import").get("name"):
                rich.print(
                    f"[red]name mismatch.[/red] Remove model_import_id from the {config_file_name} file for the new deployment and run command [blue]`inferless deploy`[/blue]"
                )
                raise typer.Abort(1)

        _, _, _, workspace_id, workspace_name = decrypt_tokens()
        rich.print(f"Using Workspace: [blue]{workspace_name}[/blue]")

        payload = {
            "name": config.get("name"),
            "details": {
                "is_auto_build": False,
                "webhook_url": "",
                "upload_type": "local",
                "is_cli_deploy": True,
                "runtime": "PYTORCH",
            },
            "import_source": "FILE",
            "source_framework_type": config.get("source_framework_type"),
            "source_location": "LOCAL_FILE",
            "workspace": workspace_id,
        }
        if redeploy and not is_failed:
            payload["id"] = config.get("model_import_id")

        progress.update(task_id, description="importing model...")
        try:
            details = import_model(payload)
        except Exception as e:
            rich.print(e)
            raise typer.Exit(1)

        if "model_import" in details:
            model_id = details["model_import"]["id"]

            progress.update(
                task_id, description="Uploading model to secure location..."
            )

            with tempfile.TemporaryDirectory() as temp_dir:
                directory_to_snapshot = os.getcwd()  # Current working directory

                zip_filename = os.path.join(
                    temp_dir, f"{os.path.basename(directory_to_snapshot)}.zip"
                )

                create_zip_file(zip_filename, directory_to_snapshot)

                s3_key = f"cli_zip_files/{model_id}/{os.path.basename(directory_to_snapshot)}.zip"
                file_size = os.path.getsize(zip_filename)
                with open(zip_filename, "rb") as zip_file:
                    progress.update(
                        task_id, description="Please wait, uploading the model..."
                    )
                    try:
                        model_url = upload_file(zip_file, s3_key, file_size, type="ZIP")
                    except Exception as e:
                        rich.print(e)
                        raise typer.Exit(1)
                    payload["details"]["model_url"] = model_url
                    payload["id"] = model_id
            try:
                _ = import_model(payload)
            except Exception as e:
                rich.print(e)
                raise typer.Exit(1)
            io_schema = False
            if "io_schema" in config:
                io_schema = config["io_schema"]

            if not io_schema:
                # inputs = read_json(config["optional"]["input_file_name"])
                # outputs = read_json(config["optional"]["output_file_name"])
                try:
                    input_file_name = f"{model_id}/input.json"
                    output_file_name = f"{model_id}/output.json"
                    input_payload = {
                        "url_for": "INPUT_OUTPUT_JSON_UPLOAD",
                        "file_name": input_file_name,
                    }
                    output_payload = {
                        "url_for": "INPUT_OUTPUT_JSON_UPLOAD",
                        "file_name": output_file_name,
                    }
                    create_presigned_io_upload_url(
                        input_payload, config["optional"]["input_file_name"]
                    )
                    create_presigned_io_upload_url(
                        output_payload, config["optional"]["output_file_name"]
                    )
                    S3_BUCKET_NAME = "infer-data"
                    if get_current_mode() == "DEV":
                        S3_BUCKET_NAME = "infer-data-dev"
                    s3_input_url = f"s3://{S3_BUCKET_NAME}/{input_file_name}"
                    s3_output_url = f"s3://{S3_BUCKET_NAME}/{output_file_name}"
                    _ = upload_io(
                        {
                            "id": model_id,
                            "input_json": {"s3_infer_data_url": s3_input_url},
                            "output_json": {"s3_infer_data_url": s3_output_url},
                        }
                    )
                except Exception as e:
                    rich.print(e)
                    raise typer.Exit(1)
            # inputs = read_json(config["optional"]["input_file_name"])
            # outputs = read_json(config["optional"]["output_file_name"])
            # try:
            #     _ = upload_io(
            #         {"id": model_id, "input_json": inputs, "output_json": outputs}
            #     )
            # except Exception as e:
            #     rich.print(e)
            #     raise typer.Exit(1)

            progress.update(task_id, description="Validating the model...")
            try:
                _ = start_import_model({"id": model_id})

            except ModelImportException:
                del config["model_import_id"]
                create_yaml(config, config_file_name)
                rich.print(
                    f"[red]Could'nt find Model Import ID[/red] we have removed the model_import_id from the {config_file_name} file. for the new deployment and run command [blue]`inferless deploy`[/blue]"
                )
                raise typer.Exit(1)

            except Exception as e:
                rich.print(e)
                raise typer.Exit(1)

            status, res = poll_model_status(model_id)
            if status == "FAILURE":
                error_msg = res["model_import"]["import_error"]["message"]
                rich.print(f"[red]{error_msg}[/red]")
                raise typer.Abort(1)

            default_values = get_default_machine_values(
                config["configuration"]["gpu_type"],
                "dedicated" if config["configuration"]["is_dedicated"] else "shared",
            )

            config_payload = {
                "id": model_id,
                "configuration": {
                    "runtime": "PYTORCH",
                    "cpu": float(default_values["cpu"]),
                    "inference_time": config["configuration"]["inference_time"],
                    "is_auto_build": False,
                    "is_dedicated": config["configuration"]["is_dedicated"],
                    "machine_type": config["configuration"]["gpu_type"],
                    "is_serverless": config["configuration"]["is_serverless"],
                    "max_replica": config["configuration"]["max_replica"],
                    "min_replica": config["configuration"]["min_replica"],
                    "memory": float(default_values["memory"]),
                    "scale_down_delay": config["configuration"]["scale_down_delay"],
                },
            }

            if (
                config["configuration"]["custom_volume_id"]
                and config["configuration"]["custom_volume_name"]
            ):
                config_payload["configuration"]["custom_volume_config"] = config[
                    "configuration"
                ]["custom_volume_id"]
                config_payload["configuration"]["custom_volume_name"] = config[
                    "configuration"
                ]["custom_volume_name"]

            if config["configuration"]["custom_runtime_id"]:
                config_payload["configuration"]["custom_docker_template"] = config[
                    "configuration"
                ]["custom_runtime_id"]
                config_payload["configuration"]["custom_docker_config"] = ""
            progress.update(task_id, description="Updating model configuration...")
            try:
                _ = update_model_configuration(config_payload)
            except Exception as e:
                rich.print(e)
                raise typer.Exit(1)

            if config["env"] or config["secrets"]:
                env_payload = {
                    "model_import_id": model_id,
                    "variables": config["env"] or {},
                    "credential_ids": config["secrets"] or [],
                    "patch": False,
                }
                progress.update(task_id, description="Setting environment variables...")
                try:
                    _ = set_env_variables(env_payload)
                except Exception as e:
                    rich.print(e)
                    raise typer.Exit(1)
            try:
                _ = validate_import_model({"id": model_id})
            except Exception as e:
                rich.print(e)
                raise typer.Exit(1)
            progress.remove_task(task_id)
            description_2 = "Model import started, here is your model_import_id: "
            if redeploy:
                description_2 = "Redeploying the model, here is your model_import_id: "

            with open(config_file_name, "r") as yaml_file:
                config = yaml.load(yaml_file)
                config["model_import_id"] = model_id
                create_yaml(config, config_file_name)

            rich.print(f"{description_2} [blue]{model_id}[/blue] \n")
            message = (
                "You can check the logs by running this command:\n\n"
                f"[blue]inferless log -i {model_id}[/blue]"
            )
            rich.print(message)


def deploy_git(config_file_name):
    is_yaml_present = is_inferless_yaml_present(config_file_name)
    if is_yaml_present:
        config = read_yaml(config_file_name)
        _, _, _, workspace_id, _ = decrypt_tokens()

        if (
            config
            and "configuration" in config
            and "is_serverless" in config["configuration"]
            and config["configuration"]["is_serverless"]
        ):
            try:
                workspaces = get_workspaces_list()
            except Exception as e:
                rich.print(e)
                raise typer.Exit(1)
            allow_serverless = False
            for workspace in workspaces:
                if workspace["id"] == workspace_id:
                    allow_serverless = workspace["allow_serverless"]
                    break
            if not allow_serverless:
                email_address = "nilesh@inferless.com"
                rich.print(
                    f"[red]Serverless is not enabled for your account [yellow](beta feature)[/yellow][/red] \nplease contact [blue]{email_address}[/blue]",
                )
                raise typer.Abort(1)
        temp_model_id = config.get("model_import_id")
        if temp_model_id:
            rich.print(
                f"[red]model_import_id already exists in {config_file_name}.[/red] \nremove model_import_id from the {config_file_name} file for the new deployment and run command [blue]`inferless deploy`[/blue]\n"
            )
            rich.print(
                "if you want to redeploy the model please use this command [blue]`inferless model rebuild`[/blue]\n"
            )
            raise typer.Abort(1)
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        rich.print("Deploying from git (make sure you have pushed your code to git)")
        task_id = progress.add_task(description="Getting warmed up...", total=None)
        config = read_yaml(config_file_name)

        _, _, _, workspace_id, workspace_name = decrypt_tokens()

        rich.print(f"Using Workspace: [blue]{workspace_name}[/blue]")

        payload = {
            "name": config.get("name"),
            "details": {
                "is_auto_build": False,
                "webhook_url": "",
                "github_url": config.get("model_url"),
                "runtime": "PYTORCH",
            },
            "import_source": GIT,
            "source_framework_type": config.get("source_framework_type"),
            "provider": GITHUB,
            "workspace": workspace_id,
        }
        progress.update(task_id, description="Creating model...")
        try:
            details = import_model(payload)
        except Exception as e:
            rich.print(e)
            raise typer.Exit(1)

        if "model_import" in details:
            model_id = details["model_import"]["id"]
            io_schema = False
            if "io_schema" in config:
                io_schema = config["io_schema"]

            if not io_schema:
                # inputs = read_json(config["optional"]["input_file_name"])
                # outputs = read_json(config["optional"]["output_file_name"])
                try:
                    input_file_name = f"{model_id}/input.json"
                    output_file_name = f"{model_id}/output.json"
                    input_payload = {
                        "url_for": "INPUT_OUTPUT_JSON_UPLOAD",
                        "file_name": input_file_name,
                    }
                    output_payload = {
                        "url_for": "INPUT_OUTPUT_JSON_UPLOAD",
                        "file_name": output_file_name,
                    }
                    create_presigned_io_upload_url(
                        input_payload, config["optional"]["input_file_name"]
                    )
                    create_presigned_io_upload_url(
                        output_payload, config["optional"]["output_file_name"]
                    )
                    S3_BUCKET_NAME = "infer-data"
                    if get_current_mode() == "DEV":
                        S3_BUCKET_NAME = "infer-data-dev"
                    s3_input_url = f"s3://{S3_BUCKET_NAME}/{input_file_name}"
                    s3_output_url = f"s3://{S3_BUCKET_NAME}/{output_file_name}"
                    _ = upload_io(
                        {
                            "id": model_id,
                            "input_json": {"s3_infer_data_url": s3_input_url},
                            "output_json": {"s3_infer_data_url": s3_output_url},
                        }
                    )
                except Exception as e:
                    rich.print(e)
                    raise typer.Exit(1)

            progress.update(task_id, description="Validating the model...")
            try:
                _ = validate_github_url_permissions(url=config.get("model_url"))
                _ = start_import_model({"id": model_id})

            except Exception as e:
                rich.print(e)
                raise typer.Exit(1)

            status, res = poll_model_status(model_id)
            if status == "FAILURE":
                error_msg = res["model_import"]["import_error"]["message"]
                rich.print(f"[red]{error_msg}[/red]")
                raise typer.Abort(1)

            default_values = get_default_machine_values(
                config["configuration"]["gpu_type"],
                "dedicated" if config["configuration"]["is_dedicated"] else "shared",
            )

            config_payload = {
                "id": model_id,
                "configuration": {
                    "runtime": "PYTORCH",
                    "cpu": float(default_values["cpu"]),
                    "inference_time": config["configuration"]["inference_time"],
                    "is_auto_build": False,
                    "is_dedicated": config["configuration"]["is_dedicated"],
                    "machine_type": config["configuration"]["gpu_type"],
                    "is_serverless": config["configuration"]["is_serverless"],
                    "max_replica": config["configuration"]["max_replica"],
                    "min_replica": config["configuration"]["min_replica"],
                    "memory": float(default_values["memory"]),
                    "scale_down_delay": config["configuration"]["scale_down_delay"],
                },
            }

            if (
                config["configuration"]["custom_volume_id"]
                and config["configuration"]["custom_volume_name"]
            ):
                config_payload["configuration"]["custom_volume_config"] = config[
                    "configuration"
                ]["custom_volume_id"]
                config_payload["configuration"]["custom_volume_name"] = config[
                    "configuration"
                ]["custom_volume_name"]

            if config["configuration"]["custom_runtime_id"]:
                config_payload["configuration"]["custom_docker_template"] = config[
                    "configuration"
                ]["custom_runtime_id"]
                config_payload["configuration"]["custom_docker_config"] = ""

            progress.update(task_id, description="Updating model configuration...")
            try:
                _ = update_model_configuration(config_payload)
            except Exception as e:
                rich.print(e)
                raise typer.Exit(1)
            if config["env"] or config["secrets"]:
                env_payload = {
                    "model_import_id": model_id,
                    "variables": config["env"] or {},
                    "credential_ids": config["secrets"] or [],
                    "patch": False,
                }
                progress.update(task_id, description="Setting environment variables...")
                try:
                    _ = set_env_variables(env_payload)
                except Exception as e:
                    rich.print(e)
                    raise typer.Exit(1)
            try:
                _ = validate_import_model({"id": model_id})
            except Exception as e:
                rich.print(e)
                raise typer.Exit(1)
            progress.remove_task(task_id)

            with open(config_file_name, "r") as yaml_file:
                config = yaml.load(yaml_file)
                config["model_import_id"] = model_id
                create_yaml(config, config_file_name)

            rich.print(
                f"Model import started, here is your model_import_id: [blue]{model_id}[/blue] \n"
            )

            message = (
                "You can check the logs by running this command:\n\n"
                f"[blue]inferless log -i {model_id}[/blue]"
            )
            rich.print(message)


def poll_model_status(id):
    try:
        start_time = time.time()
        while True:
            try:
                response = get_model_import_details(id)
            except Exception as e:
                rich.print(e)
                raise typer.Exit(1)

            status = response.get("model_import", {}).get("status")

            if status in ["FILE_STRUCTURE_VALIDATED", "SUCCESS", "FAILURE"]:
                return status, response

            if status in ["FILE_STRUCTURE_VALIDATION_FAILED", "IMPORT_FAILED"]:
                raise Exception("Status was %s, response was: %s" % (status, response))

            elapsed_time = time.time() - start_time
            if elapsed_time >= 5 * 60:
                raise TimeoutError("Structure validation timed out after 5 minutes")

            time.sleep(5)
    except Exception as e:
        log_exception(e)
