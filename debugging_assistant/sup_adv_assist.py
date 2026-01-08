import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import subprocess
import tempfile
import ast
import traceback
import openai
import os

# ---------------- CONFIG ----------------
openai.api_key = "YOUR_OPENAI_API_KEY_HERE"

SUPPORTED_LANGUAGES = ["Python", "C", "C++", "Java", "JavaScript"]

# ---------------- DEBUGGING UTILS ----------------

def python_syntax_check(code_text):
    try:
        ast.parse(code_text)
        return True, "No Python syntax errors."
    except SyntaxError as e:
        return False, f"Python Syntax Error: {e.msg} at line {e.lineno}"

def python_safe_run(code_text):
    try:
        exec(code_text, {})
        return True, "Python executed successfully."
    except Exception as e:
        return False, f"Python Runtime Error: {type(e).__name__}: {e}\n{traceback.format_exc()}"

def compile_and_run_c_cpp(code_text, lang="c"):
    ext = ".c" if lang=="c" else ".cpp"
    compiler = "gcc" if lang=="c" else "g++"
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmpfile:
        tmpfile.write(code_text.encode())
        tmpfile_path = tmpfile.name
    executable = tmpfile_path.replace(ext, "")
    compile_result = subprocess.run([compiler, tmpfile_path, "-o", executable],
                                    capture_output=True, text=True)
    if compile_result.returncode != 0:
        os.remove(tmpfile_path)
        return False, f"{lang.upper()} Compilation Error:\n{compile_result.stderr}"
    run_result = subprocess.run([executable], capture_output=True, text=True)
    os.remove(tmpfile_path)
    os.remove(executable)
    if run_result.returncode != 0:
        return False, f"{lang.upper()} Runtime Error:\n{run_result.stderr}"
    return True, run_result.stdout

def compile_and_run_java(code_text, class_name="Main"):
    with tempfile.TemporaryDirectory() as tmpdir:
        java_file_path = os.path.join(tmpdir, f"{class_name}.java")
        with open(java_file_path, "w") as f:
            f.write(code_text)
        compile_result = subprocess.run(["javac", java_file_path], capture_output=True, text=True)
        if compile_result.returncode != 0:
            return False, f"Java Compilation Error:\n{compile_result.stderr}"
        run_result = subprocess.run(["java", "-cp", tmpdir, class_name],
                                    capture_output=True, text=True)
        if run_result.returncode != 0:
            return False, f"Java Runtime Error:\n{run_result.stderr}"
        return True, run_result.stdout

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
            messages=[{"role":"user", "content": prompt}],
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI suggestion failed: {e}"

def debug_code(code_text, language):
    if language.lower() == "python":
        syntax_ok, syntax_msg = python_syntax_check(code_text)
        if not syntax_ok:
            return False, syntax_msg, ai_suggest_fix(code_text, syntax_msg, "Python")
        runtime_ok, runtime_msg = python_safe_run(code_text)
        if not runtime_ok:
            return False, runtime_msg, ai_suggest_fix(code_text, runtime_msg, "Python")
        return True, runtime_msg, None
    elif language.lower() in ["c", "c++"]:
        success, result_msg = compile_and_run_c_cpp(code_text, lang=language.lower())
        if not success:
            return False, result_msg, ai_suggest_fix(code_text, result_msg, language.upper())
        return True, result_msg, None
    elif language.lower() == "java":
        success, result_msg = compile_and_run_java(code_text)
        if not success:
            return False, result_msg, ai_suggest_fix(code_text, result_msg, "Java")
        return True, result_msg, None
    else:
        return False, f"Language {language} not supported.", None

# ---------------- GUI ----------------

class AIDebuggerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Multi-Language AI Debugger")
        
        # Language selection
        self.lang_var = tk.StringVar(value=SUPPORTED_LANGUAGES[0])
        tk.Label(master, text="Select Language:").pack()
        self.lang_menu = tk.OptionMenu(master, self.lang_var, *SUPPORTED_LANGUAGES)
        self.lang_menu.pack()
        
        # Code input area
        tk.Label(master, text="Enter your code:").pack()
        self.code_text = scrolledtext.ScrolledText(master, width=80, height=20)
        self.code_text.pack()
        
        # Output area
        tk.Label(master, text="Output / AI Suggestions:").pack()
        self.output_text = scrolledtext.ScrolledText(master, width=80, height=15)
        self.output_text.pack()
        
        # Buttons
        self.run_button = tk.Button(master, text="Run & Debug", command=self.run_debug)
        self.run_button.pack(pady=5)
        
    def run_debug(self):
        code = self.code_text.get("1.0", tk.END)
        language = self.lang_var.get()
        success, msg, ai_msg = debug_code(code, language)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, msg)
        if ai_msg:
            self.output_text.insert(tk.END, "\n\n--- AI Suggested Fix ---\n" + ai_msg)

# ---------------- MAIN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    gui = AIDebuggerGUI(root)
    root.mainloop()