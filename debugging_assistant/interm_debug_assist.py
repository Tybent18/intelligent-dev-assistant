import ast
import traceback
import openai  # Requires OpenAI API key
import sys

# ---------------- CONFIG ----------------
openai.api_key = "YOUR_OPENAI_API_KEY_HERE"  # Replace with your key

# ---------------- UTILITY FUNCTIONS ----------------

def syntax_check(code_text):
    """Check Python syntax without executing code."""
    try:
        ast.parse(code_text)
        return True, "No syntax errors detected."
    except SyntaxError as e:
        msg = f"Syntax Error: {e.msg} at line {e.lineno}"
        return False, msg

def safe_run(code_text):
    """Execute Python code safely and catch runtime errors."""
    try:
        exec(code_text, {})
        return True, "Code executed successfully."
    except Exception as e:
        tb = traceback.format_exc()
        return False, f"Runtime Error: {type(e).__name__}: {e}\n{tb}"

def ai_suggest_fix(code_text, error_msg):
    """Use GPT API to suggest fixes for the code."""
    prompt = f"""
I have the following Python code:

{code_text}

It produced this error:

{error_msg}

Please explain why this error occurred and suggest a corrected version of the code.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role":"user", "content": prompt}],
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI suggestion failed: {e}"

# ---------------- MAIN DEBUGGING FUNCTION ----------------

def debug_python_code(code_text):
    print("\n--- Syntax Check ---")
    syntax_ok, syntax_msg = syntax_check(code_text)
    print(syntax_msg)

    if not syntax_ok:
        print("\n--- AI Suggestion ---")
        suggestion = ai_suggest_fix(code_text, syntax_msg)
        print(suggestion)
        return

    print("\n--- Runtime Check ---")
    runtime_ok, runtime_msg = safe_run(code_text)
    print(runtime_msg)

    if not runtime_ok:
        print("\n--- AI Suggestion ---")
        suggestion = ai_suggest_fix(code_text, runtime_msg)
        print(suggestion)

# ---------------- MAIN LOOP ----------------

print("AI Debugging Assistant")
print("Paste your Python code. Type 'exit' to quit.\n")

while True:
    code_input = ""
    print("Enter your code (end with an empty line):")
    while True:
        line = input()
        if line.strip() == "":
            break
        code_input += line + "\n"

    if code_input.strip().lower() == "exit":
        print("Exiting AI Debugger.")
        break

    debug_python_code(code_input)