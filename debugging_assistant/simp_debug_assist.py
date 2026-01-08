import ast

def check_syntax(code_text):
    try:
        ast.parse(code_text)
        return "No syntax errors detected."
    except SyntaxError as e:
        return f"Syntax Error: {e.msg} at line {e.lineno}"

def run_code_safely(code_text):
    try:
        exec(code_text, {})
        return "Code executed successfully."
    except Exception as e:
        return f"Runtime Error: {type(e).__name__}: {e}"

def debug_code(code_text):
    syntax_report = check_syntax(code_text)
    print("Syntax Check:", syntax_report)
    if "No syntax errors" in syntax_report:
        runtime_report = run_code_safely(code_text)
        print("Runtime Check:", runtime_report)

# ---------------- Main Loop ----------------
print("Python Debugging Assistant. Type 'exit' to quit.")

while True:
    code_input = input("\nPaste your Python code (or type 'exit'): ")
    if code_input.lower() == "exit":
        break
    debug_code(code_input)