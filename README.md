# IT 111 Assignment 3 — Dice Game (Python + Flask)

## Overview
This project is a simple dice game built with **Python** and **Flask**. The user enters a dice roll value (2–12) to simulate controlled test data. The game applies the rules below and displays the current turn, point (if set), and win/lose status through a web interface.

### Game Rules (Craps-style)
- **Turn 1**
  - Roll **2, 3, or 12** → **Lose**
  - Roll **7 or 11** → **Win**
  - Any other roll → becomes the **Point**, continue to next turn
- **Turn 2+**
  - Roll **7** → **Lose**
  - Roll the **Point** → **Win**
  - Otherwise → keep rolling

---

## Requirements / Installation
- Python 3.x
- Flask

If needed:
```bash
pip install flask
```

## How to run
From the project root directory (the folder that contains `app.py`):

```bash
python app.py
```
Then open your browser to:
- http://127.0.0.1:5000/
