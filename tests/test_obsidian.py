from pathlib import Path

import pytest

from obsidian.app import create_app
from obsidian.core import ObsidianCore


@pytest.fixture
def project(tmp_path: Path) -> Path:
    (tmp_path / "valid.py").write_text("def hello():\n    return 'world'\n", encoding="utf-8")
    (tmp_path / "notes.md").write_text("# Demo\n", encoding="utf-8")
    return tmp_path


def test_inventory_and_status(project):
    core = ObsidianCore(project)
    assert core.inventory()["files"] == 2
    assert core.status()["state"] == "ONLINE"
    assert core.status()["python_modules"] == 1


def test_diagnostic_parses_python(project):
    result = ObsidianCore(project).command("diagnose code")
    assert result.intent == "diagnostic"
    assert result.telemetry == {"valid": 1, "errors": 0}
    assert any(action["type"] == "render_diagnostics" for action in result.actions)


@pytest.mark.parametrize(
    ("command", "intent"),
    [
        ("system status", "status"),
        ("scan project", "project_scan"),
        ("open the hololab", "hololab"),
        ("show lineage", "lineage"),
        ("who are you", "identity"),
    ],
)
def test_command_routing(project, command, intent):
    assert ObsidianCore(project).command(command).intent == intent


def test_api_contract(project):
    app = create_app(project)
    app.config.update(TESTING=True)
    client = app.test_client()
    assert client.get("/").status_code == 200
    status = client.get("/api/status")
    assert status.status_code == 200
    assert status.get_json()["name"] == "OBSIDIAN"
    response = client.post("/api/command", json={"command": "scan project"})
    assert response.status_code == 200
    assert response.get_json()["intent"] == "project_scan"


def test_api_rejects_non_string_command(project):
    app = create_app(project)
    app.config.update(TESTING=True)
    response = app.test_client().post("/api/command", json={"command": ["nope"]})
    assert response.status_code == 400

