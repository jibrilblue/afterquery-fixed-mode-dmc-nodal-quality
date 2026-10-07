import json, math
from pathlib import Path
import pytest

OUT = Path("/app/output/dmc.json")
GT  = Path("/tests/ground_truth.json")

TOL = {
    "energy_hartree": 5.0e-3,    # absolute energies, loose enough for Jastrow variation
    "fixed_node_kcal": 1.0,      # fixed-node error in kcal/mol
    "error_ratio": 0.5,          # statistical error must be smaller than the difference
}

@pytest.fixture(scope="module")
def sub():
    assert OUT.exists(), f"missing required artifact {OUT}"
    return json.loads(OUT.read_text())

@pytest.fixture(scope="module")
def truth():
    return json.loads(GT.read_text())

def test_jastrow_params_present(sub):
    assert "jastrow_params" in sub
    assert len(sub["jastrow_params"]) > 0
    for p in sub["jastrow_params"]:
        assert math.isfinite(float(p))

def test_vmc_energy(sub, truth):
    assert abs(sub["vmc_energy_hartree"] - truth["vmc_energy_hartree"]) <= TOL["energy_hartree"]

def test_dmc_energy(sub, truth):
    assert abs(sub["dmc_energy_hartree"] - truth["dmc_energy_hartree"]) <= TOL["energy_hartree"]

def test_multi_ref_energy(sub, truth):
    assert abs(sub["dmc_multi_ref_energy_hartree"] - truth["dmc_multi_ref_energy_hartree"]) <= TOL["energy_hartree"]

def test_fixed_node_error(sub, truth):
    assert abs(sub["fixed_node_error_kcal_mol"] - truth["fixed_node_error_kcal_mol"]) <= TOL["fixed_node_kcal"]

def test_fixed_node_error_nonzero(sub):
    # the multi-reference energy must differ from the single-reference energy
    diff = abs(sub["dmc_multi_ref_energy_hartree"] - sub["dmc_energy_hartree"])
    assert diff > 1e-4, "multi-reference DMC energy equals single-reference; CAS step was skipped"

def test_statistical_errors_are_small(sub):
    # the statistical error on each energy must be smaller than the energy differences
    for key in ("vmc_error_hartree", "dmc_error_hartree"):
        assert sub[key] < TOL["error_ratio"] * abs(sub["dmc_multi_ref_energy_hartree"] - sub["dmc_energy_hartree"])
