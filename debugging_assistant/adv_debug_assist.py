#languages portion

import subprocess
import tempfile
import os

def run_c(code_text):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".c") as tmpfile:
        tmpfile.write(code_text.encode())
        tmp_path = tmpfile.name

    executable = tmp_path.replace(".c", "")

    compile_result = subprocess.run(
        ["gcc", tmp_path, "-o", executable],
        capture_output=True,
        text=True
    )

    if compile_result.returncode != 0:
        os.remove(tmp_path)
        return False, compile_result.stderr

    run_result = subprocess.run(
        [executable],
        capture_output=True,
        text=True
    )

    os.remove(tmp_path)
    os.remove(executable)

    if run_result.returncode != 0:
        return False, run_result.stderr

    return True, run_result.stdout


def run_java(code_text, class_name="Main"):
    with tempfile.TemporaryDirectory() as tmpdir:
        java_path = os.path.join(tmpdir, f"{class_name}.java")

        with open(java_path, "w") as f:
            f.write(code_text)

        compile_result = subprocess.run(
            ["javac", java_path],
            capture_output=True,
            text=True
        )

        if compile_result.returncode != 0:
            return False, compile_result.stderr

        run_result = subprocess.run(
            ["java", "-cp", tmpdir, class_name],
            capture_output=True,
            text=True
        )

        if run_result.returncode != 0:
            return False, run_result.stderr

        return True, run_result.stdout

#Python Execution

import subprocess
import tempfile

def run_python(code_text):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code_text)
        path = f.name

    result = subprocess.run(
        ["python", path],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return True, result.stdout or "Execution successful"
    else:
        return False, result.stderr

#Clean CLI

from core.analyzer import check_syntax
from core.executor import run_python
from core.languages import run_c, run_java
from core.ai_suggester import ai_suggest_fix


def debug(code, language, use_ai=True):
    print(f"\n=== DEBUGGING {language.upper()} ===")

    if language == "python":
        ok, msg = check_syntax(code)
        print(msg)

        if not ok:
            if use_ai:
                print("\n=== AI SUGGESTION ===")
                print(ai_suggest_fix(code, msg, "Python"))
            return

        ok, msg = run_python(code)
        print(msg)

    elif language == "c":
        ok, msg = run_c(code)
        print(msg)

    elif language == "java":
        ok, msg = run_java(code)
        print(msg)

    else:
        print("Unsupported language.")
        return

    if not ok and use_ai:
        print("\n=== AI SUGGESTION ===")
        print(ai_suggest_fix(code, msg, language))


def run_cli():
    print("AI Debugger (Python, C, Java)")

    while True:
        lang = input("\nLanguage (python/c/java or exit): ").lower()
        if lang == "exit":
            break

        print("Paste code (end with empty line):")
        code = ""

        while True:
            line = input()
            if line.strip() == "":
                break
            code += line + "\n"

        debug(code, lang)

#Entry Point

from interface.cli import run_cli

if __name__ == "__main__":
    run_cli()