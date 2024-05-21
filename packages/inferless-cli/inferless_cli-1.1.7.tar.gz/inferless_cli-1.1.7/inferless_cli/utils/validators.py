import re
from prompt_toolkit.validation import ValidationError

from .constants import (
    DEPLOYMENT_TYPE,
    FRAMEWORKS,
    MACHINE_TYPE_SERVERS,
    MACHINE_TYPES_SERVERLESS,
    REGION_TYPES,
    UPLOAD_METHODS,
    GITHUB,
    HUGGINGFACE,
    HF_TASK_TYPE,
    HUGGINGFACE_TYPE,
    MACHINE_TYPES,
)


def validate_framework(choice):
    if choice not in FRAMEWORKS:
        raise ValidationError(
            message=f"Invalid choice. Please select from {', '.join(FRAMEWORKS)}"
        )
    else:
        return choice


def validate_deployment_type(choice):
    if choice not in DEPLOYMENT_TYPE:
        raise ValidationError(
            message=f"Invalid choice. Please select from {', '.join(FRAMEWORKS)}"
        )
    else:
        return choice


def validate_upload_method(choice):
    if choice not in UPLOAD_METHODS:
        raise ValidationError(
            message=f"Invalid choice. Please select from {', '.join(UPLOAD_METHODS)}"
        )
    else:
        return choice


def validate_machine_types(choice):
    if choice not in MACHINE_TYPES:
        raise ValidationError(
            message=f"Invalid choice. Please select from {', '.join(MACHINE_TYPES)}"
        )
    else:
        return choice


def validate_machine_types_serverless(choice):
    if choice not in MACHINE_TYPES_SERVERLESS:
        raise ValidationError(
            message=f"Invalid choice. Please select from {', '.join(MACHINE_TYPES_SERVERLESS)}"
        )
    else:
        return choice


def validate_region_types(choice):
    if choice not in REGION_TYPES:
        raise ValidationError(
            message=f"Invalid choice. Please select from {', '.join(REGION_TYPES)}"
        )
    else:
        return choice


def validate_machine_types_server(choice):
    if choice not in MACHINE_TYPE_SERVERS:
        raise ValidationError(
            message=f"Invalid choice. Please select from {', '.join(MACHINE_TYPE_SERVERS)}"
        )
    else:
        return choice


def validate_model_name(text):
    if not re.match(r"^[a-zA-Z0-9_-]+$", text):
        raise ValidationError(
            message="Model Name can only contain alphanumeric characters, underscores, and dashes."
        )
    if len(text) > 32:
        raise ValidationError(
            message="Character limit is reached (maximum 32 characters)."
        )
    return text


def validate_url(url):
    # Use a regular expression to check if the input matches a valid URL pattern
    url_pattern = re.compile(r"^(https?|ftp)://[^\s/$.?#].[^\s]*$", re.IGNORECASE)
    if not url_pattern.match(url):
        raise ValidationError(message="Invalid URL. Please enter a valid URL.")
    return url


def validate_email(email):
    # Define a regex pattern for a basic email validation
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    # Use the re.match() function to check if the email matches the pattern
    if re.match(email_pattern, email):
        return True
    else:
        return False


def validate_task_type(choice):
    valid_choices = [item["value"] for item in HF_TASK_TYPE]
    if choice not in valid_choices:
        raise ValidationError(
            message=f"Invalid choice. Please select from {', '.join(valid_choices)}"
        )
    else:
        return choice


def validate_workspaces(choice, options):
    valid_choices = [item["name"] for item in options]
    if choice not in valid_choices:
        raise ValidationError(
            message=f"Invalid choice. Please select from {', '.join(valid_choices)}"
        )
    else:
        return choice


def validate_volumes(choice, volumes):
    valid_choices = [item["name"] for item in volumes]
    if choice not in valid_choices:
        raise ValidationError(
            message=f"Invalid choice. Please select from {', '.join(valid_choices)}"
        )
    else:
        return choice


def validate_models(choice, models):
    valid_choices = [item["name"] for item in models]
    if choice not in valid_choices:
        raise ValidationError(
            message=f"Invalid choice. Please select from {', '.join(valid_choices)}"
        )
    else:
        return choice


def validate_templates(choice, templates):
    valid_choices = [item["name"] for item in templates]
    if choice not in valid_choices:
        raise ValidationError(
            message=f"Invalid choice. Please select from {', '.join(valid_choices)}"
        )
    else:
        return choice


def validate_huggingface_type(choice):
    valid_choices = [item["value"] for item in HUGGINGFACE_TYPE]

    if choice not in valid_choices:
        raise ValidationError(
            message=f"Invalid choice. Please select from {', '.join(valid_choices)}"
        )
    else:
        return choice


def has_github_provider(data):
    for item in data:
        if item.get("provider") == GITHUB:
            return True
    return False


def has_github_and_huggingface_providers(data):
    github_found = False
    huggingface_found = False

    for item in data:
        provider = item.get("provider")
        if provider == GITHUB:
            github_found = True
        elif provider == HUGGINGFACE:
            huggingface_found = True

    return github_found and huggingface_found


def validate_positive_number(text):
    try:
        value = int(text)
        if value < 0:
            raise ValueError()
        return value
    except ValueError as e:
        raise ValidationError(message="Please enter a positive integer.")


def validate_min_replica(text):
    value = validate_positive_number(text)
    if value > 50:
        raise ValidationError(message="Minimum replica cannot be more than 50.")
    return value


def validate_max_replica(text, min_replica_value):
    value = validate_positive_number(text)
    if value < min_replica_value:
        raise ValidationError(
            message="Maximum replica should be greater than the minimum replica."
        )
    if value > 50:
        raise ValidationError(message="Maximum replica cannot be more than 50.")
    return value


def validate_min_concurrency(text):
    value = validate_positive_number(text)
    if value > 50:
        raise ValidationError(message="Minimum concurrency cannot be more than 50.")
    return value


def validate_max_concurrency(text, min_concurrency_value):
    value = validate_positive_number(text)
    if value < min_concurrency_value:
        raise ValidationError(
            message="Maximum concurrency should be greater than the minimum concurrency."
        )
    if value > 50:
        raise ValidationError(message="Maximum concurrency cannot be more than 50.")
    return value


def validate_ideal_timeout(text):
    value = validate_positive_number(text)
    if value <= 1:
        raise ValidationError(message="Ideal timeout should be greater than 1.")
    return value


def validate_inference_timeout_time(text):
    value = validate_positive_number(text)
    if value <= 1:
        raise ValidationError(
            message="Inference timeout time should be greater than 1."
        )
    return value
