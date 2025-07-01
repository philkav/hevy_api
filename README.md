# hevy_api

A simple Python tool to interact with the [Hevy](https://hevy.com/) fitness app API and download your personal workout data.

This tool uses your personal **Hevy Developer API Key** to authenticate and retrieve your workout history with support for pagination and progress tracking.

---

## 🔧 Features

- Connects to the Hevy API via your developer key
- Downloads all workouts (paginated)
- Displays a real-time progress bar using `rich`
- Simple, modular code you can build on

---

## ⚙️ Requirements

- Python 3.8+
- A **premium Hevy account** with access to the developer API key

---

## 📥 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/hevy_api.git
cd hevy_api
pip install -r requirements.txt
```

---

## ▶️ Running the Program

First, make sure you've saved your Hevy API key to `~/.hevy_api_key`

To quickly run the tool and view your workouts in a human-readable format, use the included `workout_table.py` script:

```bash
python workout_table.py
```
