# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Module for ensuring compatibility with the qBraid Quantum API.

"""
import json
import logging
import pathlib
from typing import Any, Optional, Union

from .exceptions import QuantumServiceRequestError
from .runner import Simulator

logger = logging.getLogger(__name__)

DEFAULT_LOCAL_STORE = pathlib.Path.home() / ".qbraid" / "qir_runner"


def save_run_results(
    job_data: dict[str, Any], dir_path: Optional[Union[str, pathlib.Path]] = None
) -> None:
    """Saves the run results into a JSON file and generates a job ID.

    Args:
        data (dict[str, Any]): Simulation results to save.
        dir_path (Optional[Union[str, pathlib.Path]]): The directory path where the results
                                                       file will be saved. If None, uses
                                                       DEFAULT_LOCAL_STORE.

    """
    job_id = job_data.get("vendorJobId")

    if not job_id:
        raise ValueError("job_id not found in job_data.")

    dir_path = pathlib.Path(dir_path) if dir_path else DEFAULT_LOCAL_STORE
    dir_path.mkdir(exist_ok=True)  # Create the directory if it doesn't exist

    json_file_path = dir_path / f"{job_id}.json"
    with open(json_file_path, "w", encoding="utf-8") as file:
        json.dump(job_data, file)


def load_local_result(
    job_data: dict[str, Any], dir_path: Optional[Union[str, pathlib.Path]] = None
) -> dict[str, Any]:
    """
    Load the local result JSON file for a given job if the job is from 'qbraid_qir_simulator'.

    Args:
        job_data (dict[str, Any]): The job data dictionary.
        dir_path (Optional[Union[str, pathlib.Path]]): The directory path where the results file is
                                                       saved. If None, assumes DEFAULT_LOCAL_STORE.

    Returns:
        dict[str, Any]: The job data dictionary, potentially updated with the loaded results.
    """
    # Check if the job is from 'qbraid_qir_simulator'
    if job_data.get("qbraidDeviceId") != "qbraid_qir_simulator":
        return job_data

    # Proceed if 'vendorJobId' is available
    vendor_job_id = job_data.get("vendorJobId")
    if not vendor_job_id:
        logger.error("No vendorJobId found in job_data.")
        return job_data

    # Construct the result file path
    dir_path = pathlib.Path(dir_path) if dir_path else DEFAULT_LOCAL_STORE
    result_json_path = dir_path / f"{vendor_job_id}.json"

    # Attempt to load the JSON file
    try:
        with open(result_json_path, "r", encoding="utf-8") as file:
            job_data["result"] = json.load(file)
    except FileNotFoundError:
        logger.error("Result file not found: %s", result_json_path)
    except json.JSONDecodeError:
        logger.error("Error decoding JSON from %s", result_json_path)
    except Exception as err:  # pylint: disable=broad-except
        logger.error("An unexpected error occurred: %s", err)

    return job_data


def transform_device_data(device_data: dict[str, Any]) -> dict[str, Any]:
    """
    Transforms the device data to be compatible with the qBraid API.

    Args:
        device_data (dict): The original device data dictionary.

    Returns:
        dict: The transformed device data dictionary.
    """
    # Create a copy of the input dictionary to avoid modifying the original data
    transformed_data = device_data.copy()

    # Normalize device type to upper case if it is a simulator
    if transformed_data.get("type") == "Simulator":
        transformed_data["type"] = "SIMULATOR"

    # Check and update availability if the device is a specific type of simulator
    if transformed_data.get("qbraid_id") == "qbraid_qir_simulator":
        simulator = Simulator()
        transformed_data["isAvailable"] = simulator.status() == "ONLINE"

    # Update device status based on availability
    if transformed_data.get("status") == "ONLINE" and not transformed_data.get("isAvailable", True):
        transformed_data["status"] = "UNAVAILABLE"

    return transformed_data


def get_measurement_counts(counts: list) -> dict[str, int]:
    """Convert measurements list to histogram data."""
    row_strings = ["".join(map(str, row)) for row in counts]
    hist_data = {row: row_strings.count(row) for row in set(row_strings)}
    counts_dict = {key.replace(" ", ""): value for key, value in hist_data.items()}
    num_bits = max(len(key) for key in counts_dict)
    all_keys = [format(i, f"0{num_bits}b") for i in range(2**num_bits)]
    final_counts = {key: counts_dict.get(key, 0) for key in sorted(all_keys)}
    non_zero_counts = {key: value for key, value in final_counts.items() if value != 0}
    return non_zero_counts


def qir_job_dispatch(request_data: dict[str, Any]) -> dict[str, Any]:
    """Dispatches QIR runner job, processes results, and returns API compatible job data."""
    simulator = Simulator()
    status = simulator.status()
    if status != "ONLINE":
        raise QuantumServiceRequestError("The qir-runner simulator is not currently available")

    bitcode = request_data.pop("bitcode")
    entrypoint = request_data.pop("entrypoint")
    shots = request_data.get("shots")

    if not bitcode:
        raise QuantumServiceRequestError("bitcode is required to run qbraid_qir_simulator job")

    result_data = simulator.run(bitcode, entrypoint, shots=shots)

    job_metadata = result_data | request_data
    save_run_results(job_metadata)

    job_metadata["status"] = "COMPLETED"
    job_metadata["qbraidStatus"] = "COMPLETED"

    measurements = job_metadata.pop("measurements", [])
    job_metadata["measurementCounts"] = get_measurement_counts(measurements)

    return job_metadata
