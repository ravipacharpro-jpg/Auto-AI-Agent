import os
import subprocess
import g4f

COMMAND_FILE = "command.txt"
RESULT_FILE = "result.txt"
PROJECT_DIR = "project"
CODE_FILE = os.path.join(PROJECT_DIR, "main.py")

os.makedirs(PROJECT_DIR, exist_ok=True)

def get_ai_response(prompt):
    try:
        # FIX: Model ka naam string me daala aur auto-provider use kiya
        response = g4f.ChatCompletion.create(
            model="gpt-4", 
            messages=[{"role": "user", "content": prompt}]
        )
        return response
    except Exception as e:
        return f"API_ERROR: {e}"

def extract_code(text):
    if not text: return ""
    if "```python" in text:
        return text.split("```python")[1].split("```")[0].strip()
    elif "```" in text:
        return text.split("```")[1].split("```")[0].strip()
    return text.strip()

def main():
    if not os.path.exists(COMMAND_FILE):
        with open(COMMAND_FILE, "w") as f:
            f.write("Write a script that generates the first 20 numbers of the Fibonacci sequence and prints them.")
            
    with open(COMMAND_FILE, "r") as f:
        command = f.read().strip()

    if not command or command.startswith("DONE:"):
        print("No new commands found. Sleeping...")
        return

    print(f"New Command Detected: {command}")
    
    prompt = f"Write a complete, working Python script for the following task: '{command}'. Return ONLY valid Python code inside ```python ``` blocks. Do not include any explanations or extra text."

    max_retries = 3
    for attempt in range(max_retries):
        print(f"Attempt {attempt + 1} of {max_retries}...")
        
        ai_response = get_ai_response(prompt)
        
        # FIX: Agar AI API me error aaye toh code run karne ki koshish nahi karega
        if ai_response.startswith("API_ERROR:"):
            print(f"Failed to connect to AI: {ai_response}")
            break
            
        code = extract_code(ai_response)

        with open(CODE_FILE, "w") as f:
            f.write(code)

        print("Running generated code...")
        result = subprocess.run(["python", CODE_FILE], capture_output=True, text=True)

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
