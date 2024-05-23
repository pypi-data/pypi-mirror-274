# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Script for getting/bumping the next pre-release version.

"""

import pathlib
from typing import Union

from qbraid_core.system import extract_version, get_bumped_version, get_latest_package_version


def get_prelease_version(
    project_root: Union[pathlib.Path, str], package_name: str, shorten: bool = True
) -> str:
    """
    Determine the bumped version of a package based on local and latest versions.

    Args:
        project_root (pathlib.Path): Path to the project root directory.
        package_name (str): Name of the package to check.
        shorten (bool): Flag to determine if prerelease versions should be shortened.

    Returns:
        str: The bumped version string.

    """
    project_root = pathlib.Path(project_root)
    pyproject_toml_path = project_root / "pyproject.toml"

    if not pyproject_toml_path.exists():
        raise FileNotFoundError("pyproject.toml not found")

    v_local = extract_version(pyproject_toml_path, shorten_prerelease=shorten)
    v_latest = get_latest_package_version(package_name, prerelease=True)
    v_prerelease = get_bumped_version(v_latest, v_local)

    return v_prerelease


if __name__ == "__main__":

    PACKAGE = "qbraid_core"
    root = pathlib.Path(__file__).parent.parent.resolve()
    version = get_prelease_version(root, PACKAGE)
    print(version)
