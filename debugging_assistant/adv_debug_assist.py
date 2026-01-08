import subprocess
import tempfile
import os
import ast
import traceback
import openai

# ---------------- CONFIG ----------------
openai.api_key = "YOUR_OPENAI_API_KEY_HERE"  # Replace with your key

# ---------------- UTILITY FUNCTIONS ----------------

# --- Python Utilities ---
def python_syntax_check(code_text):
    try:
        ast.parse(code_text)
        return True, "No Python syntax errors."
    except SyntaxError as e:
        msg = f"Python Syntax Error: {e.msg} at line {e.lineno}"
        return False, msg

def python_safe_run(code_text):
    try:
        exec(code_text, {})
        return True, "Python code executed successfully."
    except Exception as e:
        tb = traceback.format_exc()
        return False, f"Python Runtime Error: {type(e).__name__}: {e}\n{tb}"

# --- C Utilities ---
def compile_and_run_c(code_text):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".c") as tmpfile:
        tmpfile.write(code_text.encode())
        tmpfile_path = tmpfile.name

    executable = tmpfile_path.replace(".c", "")
    compile_cmd = ["gcc", tmpfile_path, "-o", executable]
    compile_result = subprocess.run(compile_cmd, capture_output=True, text=True)

    if compile_result.returncode != 0:
        os.remove(tmpfile_path)
        return False, f"C Compilation Error:\n{compile_result.stderr}"

    run_result = subprocess.run([executable], capture_output=True, text=True)
    os.remove(tmpfile_path)
    os.remove(executable)

    if run_result.returncode != 0:
        return False, f"C Runtime Error:\n{run_result.stderr}"
    return True, f"C Output:\n{run_result.stdout}"

# --- Java Utilities ---
def compile_and_run_java(code_text, class_name="Main"):
    with tempfile.TemporaryDirectory() as tmpdir:
        java_file_path = os.path.join(tmpdir, f"{class_name}.java")
        with open(java_file_path, "w") as f:
            f.write(code_text)

        compile_result = subprocess.run(
            ["javac", java_file_path],
            capture_output=True, text=True
        )

        if compile_result.returncode != 0:
            return False, f"Java Compilation Error:\n{compile_result.stderr}"

        run_result = subprocess.run(
            ["java", "-cp", tmpdir, class_name],
            capture_output=True, text=True
        )

        if run_result.returncode != 0:
            return False, f"Java Runtime Error:\n{run_result.stderr}"
        return True, f"Java Output:\n{run_result.stdout}"

# --- AI Suggestion Utility ---
def ai_suggest_fix(code_text, error_msg, language="Python"):
    prompt = f"""
I have the following {language} code:

{code_text}

It produced this error:

{error_msg}

Please explain why this error occurred and provide a corrected version.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI suggestion failed: {e}"

# ---------------- DEBUGGING FUNCTION ----------------
def debug_code(code_text, language):
    print(f"\n--- Debugging {language} code ---")
    if language.lower() == "python":
        syntax_ok, syntax_msg = python_syntax_check(code_text)
        print(syntax_msg)
        if not syntax_ok:
            print("\n--- AI Suggestion ---")
            print(ai_suggest_fix(code_text, syntax_msg, "Python"))
            return

        runtime_ok, runtime_msg = python_safe_run(code_text)
        print(runtime_msg)
        if not runtime_ok:
            print("\n--- AI Suggestion ---")
            print(ai_suggest_fix(code_text, runtime_msg, "Python"))

    elif language.lower() == "c":
        success, result_msg = compile_and_run_c(code_text)
        print(result_msg)
        if not success:
            print("\n--- AI Suggestion ---")
            print(ai_suggest_fix(code_text, result_msg, "C"))

    elif language.lower() == "java":
        success, result_msg = compile_and_run_java(code_text)
        print(result_msg)
        if not success:
            print("\n--- AI Suggestion ---")
            print(ai_suggest_fix(code_text, result_msg, "Java"))

    else:
        print(f"Language {language} not supported yet.")

# ---------------- MAIN LOOP ----------------
print("Multi-Language AI Debugging Assistant")
print("Supported languages: Python, C, Java")
print("Paste your code, type 'exit' as language to quit.\n")

while True:
    language = input("Enter language (python/c/java): ").strip().lower()
    if language == "exit":
        print("Exiting AI Debugger.")
        break

    code_input = ""
    print("Enter your code (end with an empty line):")
    while True:
        line = input()
        if line.strip() == "":
            break
        code_input += line + "\n"

    debug_code(code_input, language)