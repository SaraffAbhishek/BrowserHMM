import os
import json
import asyncio
from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
import warnings
warnings.filterwarnings("ignore")

ACTIONS_FILE = Path("hmm_tracking_actions.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./gen-lang-client-0187858445-e02eab482a33.json"

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")


async def retrieve_voyage_and_arrival(booking_id: str):
    prompt = (
        f"Given a HMM booking ID '{booking_id}', retrieve the voyage number and arrival date from http://seacargotracking.net."
        "Go to http://seacargotracking.net, scroll and click on HYUNDAI Merchant Marine (HMM), it opens a new tab. Switch to that tab. Click on e-Servcie. A popup comes, close that and then enter the booking ID in the Track & Trace input box. Click on the Retrieve button to submit. Find the Voyage number and arrival date for booking id."
        "If the access is blocked by a firwewall or any error occurs, close the tab and switch back to the previous tab."
    )
    if ACTIONS_FILE.exists():
        with open(ACTIONS_FILE, "r") as f:
            recorded = json.load(f)

        cleaned = [act for act in recorded if "switch_tab" not in act]

        for act in cleaned:
            if "input_text" in act and "text" in act["input_text"]:
                act["input_text"]["text"] = booking_id

        agent = Agent(task=prompt, llm=llm, initial_actions=cleaned)

    else:
        agent = Agent(task=prompt, llm=llm)

    try:
        history = await agent.run()
        print("\n\n\nRESULT:", history.final_result())

        if not ACTIONS_FILE.exists():
            to_save = history.model_actions()
            with open(ACTIONS_FILE, "w") as f:
                json.dump(to_save, f, indent=2, default=str)
            print(f"\nRecorded {len(to_save)} steps to {ACTIONS_FILE!r}")

    except Exception as e:
        print("Clearing saved actions and re-recording a fresh run.")
        ACTIONS_FILE.unlink(missing_ok=True)
        await retrieve_voyage_and_arrival(booking_id)

if __name__ == "__main__":
    try:
        booking_id = input("Enter HMM booking ID (leave blank for sample ID): ").strip()
        if not booking_id:
            booking_id = "SINI25432400"
        asyncio.run(retrieve_voyage_and_arrival(booking_id))
        input("\n\nPress Enter to exit...")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
