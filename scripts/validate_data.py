import json
import os
import sys

REQUIRED_FILES = [
    "learning_metrics.json",
    "skill_score.json",
    "skill_radar.json",
    "htb_stats.json"
]

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")


def main():
    missing = []

    for file in REQUIRED_FILES:
        path = os.path.join(RAW_DIR, file)
        if not os.path.exists(path):
            missing.append(file)
            continue

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if file == "skill_radar.json" and not isinstance(data, dict):
                print("[ERROR] skill_radar.json must be a JSON object")
                sys.exit(1)

        except Exception as e:
            print(f"[ERROR] Invalid JSON: {file}")
            print(e)
            sys.exit(1)

    if missing:
        print("[ERROR] Missing files:")
        for m in missing:
            print(f"- {m}")
        sys.exit(1)

    print("[OK] All raw data validated")


if __name__ == "__main__":
    main()