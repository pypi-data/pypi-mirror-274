#   -------------------------------------------------------------
#   Copyright (c) Railtown AI. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   -------------------------------------------------------------
"""Railtown AI Python SDK for tracking errors and exceptions in your Python applications"""
from __future__ import annotations
from pydantic import BaseModel
from dotenv import load_dotenv
from functools import wraps
import base64
import json
import requests
import datetime
import os

load_dotenv()

railtown_api_key: str = os.environ.get("RAILTOWN_API_KEY", None)

# TODO: Bump this
__version__ = "1.0.3"


class RailtownPayload(BaseModel):
    Message: str
    Level: str
    OrganizationId: str
    ProjectId: str
    EnvironmentId: str
    Runtime: str
    Exception: str
    TimeStamp: str
    Properties: dict


def init(token: str):
    global railtown_api_key
    railtown_api_key = token


def get_config() -> dict:
    try:
        global railtown_api_key

        if (railtown_api_key is None) or (railtown_api_key == ""):
            raise Exception("Invalid Railtown AI API Key: Ensure you call init(railtown_api_key)")

        token_base64_bytes = railtown_api_key.encode("ascii")
        token_decoded_bytes = base64.b64decode(token_base64_bytes)
        token_json = token_decoded_bytes.decode("ascii")
        jwt = json.loads(token_json)

        if "u" not in jwt:
            raise Exception("Invalid Railtown AI API Key: host is required")
        elif "o" not in jwt:
            raise Exception("Invalid Railtown AI API Key: organization_id is required")
        elif "p" not in jwt:
            raise Exception("Invalid Railtown AI API Key: project_id is required")
        elif "h" not in jwt:
            raise Exception("Invalid Railtown AI API Key: secret is required")
        elif "e" not in jwt:
            raise Exception("Invalid Railtown AI API Key: environment_id is required")

        return jwt
    except Exception as e:
        raise Exception("Invalid Railtown AI API Key: Ensure to copy it from your Railtown Project") from e


def log(error, *args, **kwargs):
    config = get_config()
    stack_trace = get_full_stack_trace()

    payload = [
        {
            "Body": str(
                RailtownPayload(
                    Message=str(error),
                    Level="error",
                    Exception=stack_trace,
                    OrganizationId=config["o"],
                    ProjectId=config["p"],
                    EnvironmentId=config["e"],
                    Runtime="python-traceback",
                    TimeStamp=datetime.datetime.now().isoformat(),
                    Properties=kwargs,
                ).model_dump()
            ),
            "UserProperties": {
                "AuthenticationCode": config["h"],
                "ClientVersion": f"Python-{__version__}",
                "Encoding": "utf-8",
                "ConnectionName": config["u"],
            },
        }
    ]

    requests.post(
        "https://" + config["u"],
        headers={"Content-Type": "application/json", "User-Agent": "railtown-py(python)"},
        json=payload,
    )


def get_full_stack_trace():
    import traceback, sys

    exc = sys.exc_info()[0]
    stack = traceback.extract_stack()[:-1]  # last one would be full_stack()
    if exc is not None:  # i.e. an exception is present
        del stack[-1]  # remove call of full_stack, the printed exception
        # will contain the caught exception caller instead
    trc = "Traceback (most recent call last):\n"
    stackstr = trc + "".join(traceback.format_list(stack))
    if exc is not None:
        stackstr += "  " + traceback.format_exc().lstrip(trc)
    return stackstr


def log_exception(exclude_params=None):
    """
    Decorator function that logs all exceptions raised by the wrapped function to the Railtown platform.

    Optionally excludes specified function arguments from logging.

    Args:
        :param exclude_params: A list of positional-argument indices (ints) and/or keyword-argument names (str) to exclude from the log

    """

    if exclude_params is None:
        exclude_params = []

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)

            except Exception as e:
                # Filter out excluded parameters
                filtered_args = [arg for i, arg in enumerate(args) if i not in exclude_params]
                filtered_kwargs = {key: value for key, value in kwargs.items() if key not in exclude_params}
                # Log the exception to Railtown
                log(f"{e}", *filtered_args, **filtered_kwargs)

                # Continue to raise the exception as usual
                raise

            return result

        return wrapper

    return decorator
