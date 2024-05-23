# Copyright (C) 2024 qBraid
#
# This file is part of the qBraid-SDK
#
# The qBraid-SDK is free software released under the GNU General Public License v3
# or later. You can redistribute and/or modify it under the terms of the GPL v3.
# See the LICENSE file in the project root or <https://www.gnu.org/licenses/gpl-3.0.html>.
#
# THERE IS NO WARRANTY for the qBraid-SDK, as per Section 15 of the GPL v3.

"""
Unit tests for qir-runner Python simulator wrapper.

"""
from pathlib import Path
from unittest.mock import patch

import pytest

from qbraid_core.services.quantum.compat import get_measurement_counts
from qbraid_core.services.quantum.runner import Simulator

RESOURCE_DIR = Path(__file__).parent / "resources"


def load_resource(file_name: str, **kwargs):
    """Helper function to read content from a file."""
    mode = "rb" if file_name.endswith(".bc") else "r"
    file_path = RESOURCE_DIR / file_name

    try:
        with open(file_path, mode, **kwargs) as file:
            return file.read()
    except FileNotFoundError as err:
        raise FileNotFoundError(f"Resource file not found: {file_path}") from err


@pytest.fixture
def mock_runner_data():
    """Load QIR test program and expected stdout from resources."""
    bitcode = load_resource("qir_program.bc")
    stdout = load_resource("qir_runner_stdout.txt")

    shots = 10
    num_qubits = 5
    basis_0 = [0] * num_qubits
    basis_1 = [1] * num_qubits

    qubit_res = [0, 1, 1, 0, 0, 0, 0, 1, 0, 1]
    parsed = {f"q{i}": qubit_res for i in range(num_qubits)}
    measurements = [basis_0 if value == 0 else basis_1 for value in qubit_res]

    key_0 = "0" * num_qubits
    key_1 = "1" * num_qubits

    counts = {
        key_0: qubit_res.count(0),
        key_1: qubit_res.count(1),
    }

    data = {
        "shots": shots,
        "num_qubits": num_qubits,
        "parsed": parsed,
        "measurements": measurements,
        "counts": counts,
        "bitcode": bitcode,
        "stdout": stdout,
    }

    yield data


def test_run_qir_simulator(mock_runner_data):
    """Test qir-runner sparse simulator python wrapper(s)."""
    simulator = Simulator()

    shots = mock_runner_data["shots"]
    bitcode = mock_runner_data["bitcode"]

    with patch("subprocess.check_output") as mock_check_output:
        mock_check_output.return_value = mock_runner_data["stdout"]
        job_data = simulator.run(bitcode, shots=shots)
        job_id = job_data.get("vendorJobId")
        measurements = job_data.get("measurements")
        time_stamps: dict = job_data.get("timeStamps", {})
        execution_duration = time_stamps.get("executionDuration")

        assert isinstance(job_id, str)
        assert isinstance(measurements, list)
        assert isinstance(execution_duration, int)

        counts = get_measurement_counts(measurements)
        assert len(counts) == 2
        assert sum(counts.values()) == shots


def test_process_qir_simulator_results(mock_runner_data):
    """Test post-processing of qir runner results."""
    stdout = mock_runner_data["stdout"]
    parsed_data = Simulator._parse_results(stdout)
    measurements = Simulator._data_to_measurements(parsed_data)
    counts = get_measurement_counts(measurements)

    assert parsed_data == mock_runner_data["parsed"]
    assert measurements == mock_runner_data["measurements"]
    assert counts == mock_runner_data["counts"]
