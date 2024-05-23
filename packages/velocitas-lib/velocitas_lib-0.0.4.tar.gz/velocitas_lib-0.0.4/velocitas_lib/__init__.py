# Copyright (c) 2023-2024 Contributors to the Eclipse Foundation
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0

import json
import os
import sys
from io import TextIOWrapper
from typing import Any, Dict

import requests


def require_env(name: str) -> str:
    """Require and return an environment variable.

    Args:
        name (str): The name of the variable.

    Raises:
        ValueError: In case the environment variable is not set.

    Returns:
        str: The value of the variable.
    """
    var = os.getenv(name)
    if not var:
        raise ValueError(f"Environment variable {name!r} not set!")
    return var


def get_workspace_dir() -> str:
    """Return the workspace directory."""
    return require_env("VELOCITAS_WORKSPACE_DIR")


def get_app_manifest() -> Dict[str, Any]:
    manifest_data = json.loads(require_env("VELOCITAS_APP_MANIFEST"))
    if isinstance(manifest_data, dict):
        return manifest_data
    elif isinstance(manifest_data, list) and isinstance(manifest_data[0], dict):
        return manifest_data[0]
    else:
        raise TypeError("Manifest must be a dict or array!")


def get_script_path() -> str:
    """Return the absolute path to the directory the invoked Python script
    is located in."""
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def get_package_path() -> str:
    """Return the absolute path to the package directory the invoked Python
    script belongs to."""
    return require_env("VELOCITAS_PACKAGE_DIR")


def get_project_cache_dir() -> str:
    """Return the project's cache directory.

    Returns:
        str: The path to the project's cache directory.
    """
    return require_env("VELOCITAS_CACHE_DIR")


def get_cache_data() -> Dict[str, Any]:
    """Return the data of the cache as Python object."""
    cache_data = json.loads(require_env("VELOCITAS_CACHE_DATA"))

    if not isinstance(cache_data, dict):
        raise TypeError("VELOCITAS_CACHE_DATA has to be a JSON object!")

    return cache_data


def get_log_file_name(service_id: str, runtime_id: str) -> str:
    """Build the log file name for the given service and runtime.

    Args:
        service_id (str): The ID of the service to log.
        runtime_id (str): The ID of the runtime to log.

    Returns:
        str: The log file name.
    """
    return os.path.join(get_workspace_dir(), "logs", runtime_id, f"{service_id}.log")


def get_programming_language() -> str:
    """Return the programming language of the project."""
    return require_env("language")


def create_log_file(service_id: str, runtime_id: str) -> TextIOWrapper:
    """Create a log file for the given service and runtime.

    Args:
        service_id (str): The ID of the service to log.
        runtime_id (str): The ID of the runtime to log.

    Returns:
        TextIOWrapper: The log file.
    """
    log_file_name = get_log_file_name(service_id, runtime_id)
    os.makedirs(os.path.dirname(log_file_name), exist_ok=True)
    return open(log_file_name, "w", encoding="utf-8")


def download_file(uri: str, local_file_path: str) -> None:
    with requests.get(uri, timeout=30) as infile:
        os.makedirs(os.path.split(local_file_path)[0], exist_ok=True)
        with open(local_file_path, "wb") as outfile:
            for chunk in infile.iter_content(chunk_size=8192):
                outfile.write(chunk)
