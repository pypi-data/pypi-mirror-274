import json
import requests
import rich
import typer
from inferless_cli.utils.helpers import decrypt_tokens
from sentry_sdk import capture_exception, flush


def make_request(
    url,
    method="GET",
    data=None,
    headers=None,
    params=None,
    auth=True,
    convert_json=True,
):
    """
    Make a GET or POST request.

    Args:
        url (str): The URL to send the request to.
        method (str): The HTTP method to use ('GET' or 'POST'). Default is 'GET'.
        data (dict): The request data to include in the request body for POST requests.
        headers (dict): Additional headers to include in the request.
        params (dict): URL parameters for the request.
        auth (boolean): Boolean True or False.

    Returns:
        requests.Response: The response object from the request.

    Raises:
        requests.exceptions.RequestException: If the request encounters an error.
    """
    try:
        method = method.upper()  # Ensure the method is in uppercase.

        if method not in ("GET", "POST", "PUT", "DELETE"):
            raise ValueError(
                "Invalid HTTP method. Use 'GET', 'PUT', 'DELETE', or 'POST'."
            )

        default_headers = {
            "Content-Type": "application/json",
        }

        if headers is not None:
            default_headers.update(headers)
        else:
            headers = default_headers

        if auth:
            token, _, _, _, _ = decrypt_tokens()
            if not token:
                rich.print(
                    "[red]Please login to Inferless using `inferless login`[/red]"
                )
                raise typer.Exit(1)

            auth_header = {"Authorization": f"Bearer {token}"}
            headers.update(auth_header)

        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method == "POST":
            response = requests.post(
                url, headers=headers, data=convert_json and json.dumps(data) or data
            )
        elif method == "PUT":
            response = requests.put(
                url, headers=headers, data=convert_json and json.dumps(data) or data
            )
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)

        response.raise_for_status()

        return response

    except requests.HTTPError as http_err:
        capture_exception(http_err)
        flush()
        # Handle HTTPError specifically
        error_message = ""
        if hasattr(response, "json") and callable(response.json):
            error = response.json()
            if "reason" in error:
                error_message = error["reason"]
            elif "details" in error:
                error_message = error["details"]
        else:
            error_message = "Something went wrong"
        rich.print(f"Error: [red]{error_message}[/red]")
        raise requests.HTTPError(error_message, response=response)

    except Exception as e:
        capture_exception(e)
        flush()
        error_message = ""
        if hasattr(response, "json") and callable(response.json):
            error = response.json()
            if "reason" in error:
                error_message = error["reason"]
            elif "details" in error:
                error_message = error["details"]
        else:
            error_message = "Something went wrong"
        rich.print(f"Error: [red]{error_message}[/red]")
        raise Exception(e)
