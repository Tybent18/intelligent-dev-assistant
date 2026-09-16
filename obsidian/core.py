from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
import ast
import json
import re
from typing import Any


@dataclass(frozen=True)
class CommandResult:
    intent: str
    response: str
    actions: tuple[dict[str, Any], ...]
    telemetry: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ObsidianCore:
    """Deterministic local core used by the Stage One HoloLab.

    It provides useful project inspection without pretending to be a hosted LLM.
    A model provider can later be added behind this interface.
    """

    def __init__(self, project_root: str | Path) -> None:
        self.project_root = Path(project_root).resolve()
        self.started_at = datetime.now(timezone.utc)
        self.command_count = 0

    def status(self) -> dict[str, Any]:
        inventory = self.inventory()
        return {
            "name": "OBSIDIAN",
            "mode": "LOCAL_DEMO",
            "state": "ONLINE",
            "voice_ready": True,
            "project_root": self.project_root.name,
            "files_indexed": inventory["files"],
            "python_modules": inventory["python_files"],
            "commands_processed": self.command_count,
            "started_at": self.started_at.isoformat(),
        }

    def inventory(self) -> dict[str, Any]:
        ignored = {".git", ".venv", "__pycache__", ".pytest_cache", "node_modules"}
        files = [
            path for path in self.project_root.rglob("*")
            if path.is_file() and not ignored.intersection(path.parts)
        ]
        extensions: dict[str, int] = {}
        for path in files:
            suffix = path.suffix.lower() or "[none]"
            extensions[suffix] = extensions.get(suffix, 0) + 1
        return {
            "files": len(files),
            "python_files": sum(path.suffix == ".py" for path in files),
            "extensions": dict(sorted(extensions.items(), key=lambda item: (-item[1], item[0]))[:8]),
        }

    def analyze_python(self) -> dict[str, Any]:
        results = []
        for path in sorted(self.project_root.rglob("*.py")):
            if any(part.startswith(".") or part == "__pycache__" for part in path.parts):
                continue
            relative = path.relative_to(self.project_root).as_posix()
            try:
                source = path.read_text(encoding="utf-8")
                tree = ast.parse(source, filename=relative)
                results.append({
                    "path": relative,
                    "status": "valid",
                    "functions": sum(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) for node in ast.walk(tree)),
                    "classes": sum(isinstance(node, ast.ClassDef) for node in ast.walk(tree)),
                    "lines": len(source.splitlines()),
                })
            except (SyntaxError, UnicodeDecodeError) as error:
                results.append({"path": relative, "status": "error", "detail": str(error)})
        return {
            "files": results,
            "valid": sum(item["status"] == "valid" for item in results),
            "errors": sum(item["status"] == "error" for item in results),
        }

    def command(self, text: str) -> CommandResult:
        self.command_count += 1
        normalized = re.sub(r"\s+", " ", text.strip().lower())
        if not normalized:
            return self._result("empty", "I need a command before I can rearrange the universe.")

        if any(term in normalized for term in ("status", "systems", "online")):
            status = self.status()
            return self._result(
                "status",
                f"All local systems are online. I have indexed {status['files_indexed']} files and processed {status['commands_processed']} commands.",
                ({"type": "focus", "target": "system"},),
                status,
            )
        if any(term in normalized for term in ("scan", "inventory", "project")):
            inventory = self.inventory()
            return self._result(
                "project_scan",
                f"Project scan complete. {inventory['files']} files detected, including {inventory['python_files']} Python modules.",
                (
                    {"type": "focus", "target": "project"},
                    {"type": "pulse", "target": "orb"},
                ),
                inventory,
            )
        if any(term in normalized for term in ("diagnose", "debug", "syntax", "analyze")):
            analysis = self.analyze_python()
            response = (
                f"Diagnostic sweep complete. {analysis['valid']} Python files parsed successfully; "
                f"{analysis['errors']} require attention."
            )
            return self._result(
                "diagnostic",
                response,
                (
                    {"type": "focus", "target": "diagnostics"},
                    {"type": "render_diagnostics", "payload": analysis},
                ),
                {"valid": analysis["valid"], "errors": analysis["errors"]},
            )
        if any(term in normalized for term in ("lab", "hololab", "expand")):
            return self._result(
                "hololab",
                "HoloLab expanded. Spatial project, diagnostic, and lineage surfaces are active.",
                (
                    {"type": "mode", "target": "expanded"},
                    {"type": "pulse", "target": "rings"},
                ),
            )
        if any(term in normalized for term in ("legacy", "history", "evolution", "lineage")):
            return self._result(
                "lineage",
                "Opening the evolution record: assistant scripts, debugging tools, reinforcement-learning experiments, dashboards, and swarm simulations converged into Obsidian.",
                ({"type": "focus", "target": "lineage"},),
            )
        if any(term in normalized for term in ("who are you", "your name", "identify")):
            return self._result(
                "identity",
                "I am Obsidian: a local developer-intelligence laboratory wearing a holographic interface. The dramatic lighting is essential science.",
                ({"type": "pulse", "target": "orb"},),
            )
        return self._result(
            "unknown",
            "That capability is not connected in local demo mode. Try status, scan project, diagnose code, open HoloLab, or show lineage.",
            ({"type": "suggest", "commands": ["status", "scan project", "diagnose code", "open hololab", "show lineage"]},),
        )

    def _result(
        self,
        intent: str,
        response: str,
        actions: tuple[dict[str, Any], ...] = (),
        telemetry: dict[str, Any] | None = None,
    ) -> CommandResult:
        return CommandResult(intent, response, actions, telemetry or {})

    def manifest(self) -> str:
        return json.dumps(self.status(), indent=2, sort_keys=True)

