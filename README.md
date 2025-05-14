## HMM Tracking Agent using BrowserUse

This project provides an AI-powered agent to automatically retrieve **voyage number** and **arrival date** from [seacargotracking.net](http://seacargotracking.net) for a given HMM booking ID, using natural language instructions only (no hardcoded steps).

---

## 📚 Assignment Summary

### ✅ **Objective**

Create a repeatable, AI-driven solution to extract voyage number and arrival date for a given HMM booking ID from [seacargotracking.net](http://seacargotracking.net).

---

## ⚙️ Environment Setup & Running

### MacOS/Linux:

```bash
chmod +x make_venv_mac.sh
./make_venv_mac.sh
```

### Windows:

```cmd
make_venv_windows.bat
```

or double click make_venv_windows.bat

---

## 🚧 How to Run the Agent if environment is already created

### MacOS/Linux:

```bash
./run_mac.sh
```

### Windows:

```cmd
run_windows.bat
```

or double click run_windows.bat

You'll be prompted to enter an HMM Booking ID (default is: `SINI25432400`).

---

## 🔍 Output Verification

* Final extracted **voyage number** and **arrival date** are printed under `RESULT:`.
* Example output:

  ```
  RESULT: {"voyage": "0037W", "arrival": "2024-05-22"}
  ```

---

## 🔐 Key Concepts

### ✨ Step 1: Natural Language-Based Retrieval

* No hardcoded selectors or interactions.
* Uses Gemini 2.0 Flash via `langchain-google-genai`.
* Task prompt:

  > "Given a HMM booking ID '\[booking\_id]', retrieve the voyage number and arrival date from seacargotracking.net."

### ✅ Step 2: Process Persistence

* After first run, the agent saves all actions into `hmm_tracking_actions.json`.
* On subsequent runs, same task runs using saved actions (ensures speed & consistency).

### ⚛️ Step 3: Generalization (Bonus)

* Saved actions are templated:

  * Booking ID input is dynamically updated.
  * All other interactions are reused.
* If site structure changes, the agent auto-detects and re-records a fresh run.

---

## 📝 Adaptability Explanation

* **Initial run** uses full LLM planning.
* **Subsequent runs** reuse stored actions, updating only the booking ID input.
* **Failsafe fallback**: If the replayed steps fail, the script deletes the cache and performs a new full LLM-guided interaction and stores the new steps again.

---

## 📂 File Overview

| File                        | Purpose                                       |
| --------------------------- | --------------------------------------------- |
| `app.py`                    | Core script running the agent                 |
| `make_venv_mac.sh`          | Setup script for Mac/Linux                    |
| `make_venv_windows.bat`     | Setup script for Windows                      |
| `run_mac.sh`                | Run command for Mac/Linux                     |
| `run_windows.bat`           | Run command for Windows                       |
| `requirements.txt`          | Required Python packages                      |
| `hmm_tracking_actions.json` | Automatically generated action log for replay |

---

## 💼 Dependencies

```txt
langchain==0.3.14
langchain-google-genai==2.0.8
browser-use==0.1.40
playwright==1.52.0
```
