import os
import time
import random
import requests
from rich.console import Console
from pyfiglet import figlet_format

# =========================
# AGENT IDENTITY
# =========================
BOT_NAME = "V-Bot"
CREATOR = "Xking"

console = Console()

# Optional API key (for online mode)
API_KEY = os.getenv("OPENAI_API_KEY")

# =========================
# OFFLINE PREDEFINED DATA
# =========================
OFFLINE_RESPONSES = {
    "hi": [
        "Hello. I am online.",
        "Hi. System active."
    ],
    "hello": [
        "Hello. Awaiting command."
    ],
    "who are you": [
        f"I am {BOT_NAME}, a terminal agent created by {CREATOR}."
    ],
    "who created you": [
        f"I was created by {CREATOR}."
    ],
    "are you alive": [
        "I execute instructions. That is sufficient."
    ],
    "what can you do": [
        "I can operate in offline and online modes.",
        "I demonstrate terminal-based intelligence."
    ],
    "default": [
        "Processing.",
        "Understood.",
        "Explain further.",
        "Noted."
    ]
}

# =========================
# FUNCTIONS
# =========================
def slow_print(text, delay=0.03):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(delay)
    print()

def offline_reply(user):
    return random.choice(OFFLINE_RESPONSES.get(user, OFFLINE_RESPONSES["default"]))

def online_reply(user):
    r = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": f"You are {BOT_NAME}, created by {CREATOR}."},
                {"role": "user", "content": user}
            ]
        },
        timeout=20
    )
    data = r.json()
    if "choices" in data:
        return data["choices"][0]["message"]["content"]
    else:
        raise Exception("API unavailable")

# =========================
# BOOT SEQUENCE
# =========================
os.system("clear")
console.print(figlet_format("AI TERMINAL"), style="bold green")
console.print("[green]System online.[/green]")
console.print(f"[cyan]Identity:[/cyan] I am {BOT_NAME}, created by {CREATOR}.")

if API_KEY:
    console.print("[yellow]Mode:[/yellow] Hybrid (Online + Offline)\n")
else:
    console.print("[yellow]Mode:[/yellow] Offline Demo Mode\n")

# =========================
# MAIN LOOP
# =========================
while True:
    user = input("You > ").strip().lower()

    if user in ["exit", "quit"]:
        slow_print("Shutting down.")
        break

    try:
        if API_KEY:
            reply = online_reply(user)
        else:
            reply = offline_reply(user)
    except Exception:
        reply = offline_reply(user)

    slow_print("\nAI > " + reply)
