import os
import json
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Browser
from browser_use import BrowserConfig
import warnings
import psutil

warnings.filterwarnings("ignore")
load_dotenv()

# Paths and files
ACTIONS_FILE = Path("hmm_tracking_actions.json")

# Ensure Google credentials
if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
    raise EnvironmentError(
        "Please set GOOGLE_APPLICATION_CREDENTIALS in your environment or .env file"
    )

CHROME_BINARY_PATH = os.getenv("CHROME_BINARY_PATH")  
# e.g. Mac: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
# e.g. Windows: 'C:\Program Files\Google\Chrome\Application\chrome.exe' (use where chrome)


llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", timeout=120)

if CHROME_BINARY_PATH:
    browser = Browser(
        config=BrowserConfig(
            browser_binary_path=CHROME_BINARY_PATH,
            keep_alive=False
        )
    )
else:
    browser = Browser()

async def retrieve_voyage_and_arrival(booking_id: str):
    # task_prompt = (
    #     f"Given a HMM booking ID '{booking_id}', retrieve the voyage number and arrival date from http://seacargotracking.net. "
    #     "Navigate to the site, click 'HYUNDAI Merchant Marine (HMM)' to open a new tab, switch to it, click 'e-Service', close any pop-up, "
    #     "enter the booking ID into the 'Track & Trace' input, and click 'Retrieve'. Extract Voyage number and arrival date."
    # )

    # task_prompt = (
    # f"Open http://seacargotracking.net and click 'HYUNDAI Merchant Marine (HMM)' to open the tracking page in a new tab, switch to that tab and click 'e-Service', close any pop-up that appears, enter the booking ID '{booking_id}' into the 'Track & Trace' field and click 'Retrieve', then extract and return only the 'Voyage Number' and 'Arrival Date'. Perform these steps exactly in this order and do nothing else."
    # )

    task_prompt= (
        f"Given a HMM booking ID '{booking_id}', retrieve the voyage number and arrival date from http://seacargotracking.net."
        "Go to http://seacargotracking.net, scroll and click on HYUNDAI Merchant Marine (HMM), it opens a new tab. Switch to that tab. Click on e-Servcie. A popup comes, close that and then enter the booking ID in the Track & Trace input box. Click on the Retrieve button to submit. Find the Voyage number and arrival date for booking id."
    )


    # Load recorded actions if available
    initial_actions = []
    if ACTIONS_FILE.exists():
        with open(ACTIONS_FILE, "r") as f:
            recorded = json.load(f)
        initial_actions = [a for a in recorded if "switch_tab" not in a]
        for action in initial_actions:
            if "input_text" in action and "text" in action["input_text"]:
                action["input_text"]["text"] = booking_id

    agent = Agent(
        task=task_prompt,
        llm=llm,
        initial_actions=initial_actions or None,
        browser=browser
    )

    try:
        history = await agent.run()
        result = history.final_result()
        print("\nRESULT:\n", result)

        # Record actions for next run
        if not ACTIONS_FILE.exists():
            actions = history.model_actions()
            with open(ACTIONS_FILE, "w") as f:
                json.dump(actions, f, indent=2, default=str)
            print(f"Recorded {len(actions)} actions to {ACTIONS_FILE}")
        
        for proc in psutil.process_iter(['name', 'pid']):
            if proc.info['name'] and 'chrome' in proc.info['name'].lower():
                proc.kill()


    except Exception as e:
        print(f"Error occurred: {e}")
        ACTIONS_FILE.unlink(missing_ok=True)
        await retrieve_voyage_and_arrival(booking_id)

if __name__ == "__main__":
    booking_id = input(
        "Enter HMM booking ID (or press Enter to use default 'SINI25432400'): "
    ).strip() or "SINI25432400"
    asyncio.run(retrieve_voyage_and_arrival(booking_id))
    input()
    
