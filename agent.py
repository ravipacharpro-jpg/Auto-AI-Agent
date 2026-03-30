import os
import subprocess
import g4f

COMMAND_FILE = "command.txt"
RESULT_FILE = "result.txt"
PROJECT_DIR = "project"
CODE_FILE = os.path.join(PROJECT_DIR, "main.py")

# Ensure project directory exists
os.makedirs(PROJECT_DIR, exist_ok=True)

def get_ai_response(prompt):
    """Fetches AI response using free providers"""
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_turbo,
            messages=[{"role": "user", "content": prompt}],
            provider=g4f.Provider.DuckDuckGo # Extremely stable, no API key needed
        )
        return response
    except Exception as e:
        return f"Error: {e}"

def extract_code(text):
    """Extracts only Python code from AI response"""
    if "```python" in text:
        return text.split("```python")[1].split("```")[0].strip()
    elif "```" in text:
        return text.split("```")[1].split("```")[0].strip()
    return text.strip()

def main():
    if not os.path.exists(COMMAND_FILE):
        return

    with open(COMMAND_FILE, "r") as f:
        command = f.read().strip()

    # If already done or empty, do nothing
    if not command or command.startswith("DONE:"):
        print("No new commands found. Sleeping...")
        return

    print(f"New Command Detected: {command}")
    
    prompt = f"Write a complete, working Python script for the following task: '{command}'. Return ONLY valid Python code inside ```python ``` blocks. Do not include any explanations or extra text."

    max_retries = 3
    for attempt in range(max_retries):
        print(f"Attempt {attempt + 1} of {max_retries}...")
        
        # 1. Get AI Code
        ai_response = get_ai_response(prompt)
        code = extract_code(ai_response)

        # 2. Save Code
        with open(CODE_FILE, "w") as f:
            f.write(code)

        # 3. Run and Test Code
        print("Running generated code...")
        result = subprocess.run(["python", CODE_FILE], capture_output=True, text=True)

        # 4. Auto-Debug Logic
        if result.returncode == 0:
            print("Success! Code ran without errors.")
            with open(RESULT_FILE, "w") as f:
                f.write(f"SUCCESS:\n{result.stdout}")
            with open(COMMAND_FILE, "w") as f:
                f.write(f"DONE: {command}")
            break
        else:
            error_msg = result.stderr or result.stdout
            print(f"Error detected:\n{error_msg}")
            
            prompt = f"The code you generated produced this error:\n{error_msg}\nFix the error and provide the complete corrected Python script. Return ONLY code inside ```python ``` blocks."
            
            if attempt == max_retries - 1:
                print("Max retries reached. Task failed.")
                with open(RESULT_FILE, "w") as f:
                    f.write(f"FAILED after 3 attempts. Last Error:\n{error_msg}")
                with open(COMMAND_FILE, "w") as f:
                    f.write(f"DONE (FAILED): {command}")

if __name__ == "__main__":
    main()
