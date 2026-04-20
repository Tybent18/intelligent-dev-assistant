import ast
import subprocess
import tempfile

# ---------------- SYNTAX CHECK ----------------
def check_syntax(code_text):
    try:
        ast.parse(code_text)
        return True, "No syntax errors detected."
    except SyntaxError as e:
        return False, f"Syntax Error: {e.msg} at line {e.lineno}"


# ---------------- SAFE EXECUTION ----------------
def run_code_safely(code_text):
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as temp_file:
            temp_file.write(code_text)
            temp_file_path = temp_file.name

        result = subprocess.run(
            ["python", temp_file_path],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return True, result.stdout.strip() or "Code executed successfully."
        else:
            return False, result.stderr.strip()

    except Exception as e:
        return False, f"Execution Error: {type(e).__name__}: {e}"


# ---------------- DEBUG PIPELINE ----------------
def debug_code(code_text):
    print("\n=== SYNTAX CHECK ===")
    syntax_ok, syntax_msg = check_syntax(code_text)
    print(syntax_msg)

    if not syntax_ok:
        return

    print("\n=== RUNTIME ===")
    runtime_ok, runtime_msg = run_code_safely(code_text)
    print(runtime_msg)


# ---------------- MAIN LOOP ----------------
def main():
    print("Python Debugging Assistant (Safe Mode). Type 'exit' to quit.")

    while True:
        code_input = input("\nPaste your Python code (or type 'exit'): ")
        if code_input.lower() == "exit":
            break

        debug_code(code_input)


if __name__ == "__main__":
    main()