import os
import subprocess
import requests

API_KEY = os.getenv("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")

def read_command():
    if not os.path.exists("command.txt"):
        return None
    with open("command.txt", "r") as f:
        return f.read().strip()

def generate_ai_response(task):
    if not API_KEY:
        return "❌ API KEY NOT FOUND"

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openrouter/auto",
        "messages": [
            {
                "role": "system",
                "content": "You are an expert developer. Give full working code only."
            },
            {
                "role": "user",
                "content": task
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        else:
            return "❌ API ERROR: " + str(result)

    except Exception as e:
        return "❌ ERROR: " + str(e)

def save_result(result):
    with open("result.txt", "w") as f:
        f.write(result)

def push_to_github():
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "🤖 AI generated result"], check=False)
    subprocess.run(["git", "push"], check=False)

def main():
    task = read_command()

    if not task:
        save_result("❌ No command found")
        return

    print("Processing:", task)

    result = generate_ai_response(task)
    save_result(result)
    push_to_github()

if __name__ == "__main__":
    main()
