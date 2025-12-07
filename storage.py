import os
import re
import json
from datetime import datetime

OUTPUT_DIR = "generated_blogs"
HISTORY_FILE = "history.json"

def sanitize_filename(title):
    clean_title = re.sub(r'[\\/*?:"<>|]', "", title)
    clean_title = clean_title.replace(" ", "-")
    return clean_title[:50]

def load_history_log():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def log_to_history(path):
    history = load_history_log()
    abs_path = os.path.abspath(path)
    if abs_path not in history:
        history.insert(0, abs_path) 
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)

def save_blog(content, path=None):
    if path:
        save_path = path
    else:
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
        lines = content.strip().split('\n')
        title_candidate = "Blog Post"
        for line in lines:
            if line.strip().startswith("#") or "Title:" in line:
                 title_candidate = line.replace("#", "").replace("Title:", "").strip()
                 break
        timestamp = datetime.now().strftime("%Y-%m-%d")
        filename = f"{timestamp}-{sanitize_filename(title_candidate)}.txt"
        save_path = os.path.join(OUTPUT_DIR, filename)

    try:
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(content)
        log_to_history(save_path) 
        return os.path.abspath(save_path)
    except Exception as e:
        raise Exception(f"Failed to save file: {str(e)}")

def get_history():
    return load_history_log()

def read_blog(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""
