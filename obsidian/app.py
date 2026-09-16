from __future__ import annotations

from pathlib import Path
import os

from flask import Flask, jsonify, render_template, request

from .core import ObsidianCore


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def create_app(project_root: str | Path | None = None) -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    core = ObsidianCore(project_root or REPOSITORY_ROOT)
    app.config["OBSIDIAN_CORE"] = core

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/api/status")
    def status():
        return jsonify(core.status())

    @app.post("/api/command")
    def command():
        payload = request.get_json(silent=True) or {}
        text = payload.get("command", "")
        if not isinstance(text, str):
            return jsonify({"error": "command must be a string"}), 400
        return jsonify(core.command(text).to_dict())

    return app


def main() -> None:
    app = create_app()
    app.run(
        host=os.getenv("OBSIDIAN_HOST", "127.0.0.1"),
        port=int(os.getenv("OBSIDIAN_PORT", "5000")),
        debug=os.getenv("OBSIDIAN_DEBUG", "0") == "1",
    )


if __name__ == "__main__":
    main()

