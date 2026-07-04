#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import json

ROOT = Path(__file__).resolve().parents[1]

LOG_FILE = ROOT / "runtime" / "logs" / "forge.log.jsonl"

LOG_FILE.parent.mkdir(parents=True, exist_ok=True)


class KernelLogger:

    def log(self, level, source, message):

        entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": level,
            "source": source,
            "message": message
        }

        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False))
            f.write("\n")

    def info(self, source, message):
        self.log("INFO", source, message)

    def warning(self, source, message):
        self.log("WARNING", source, message)

    def error(self, source, message):
        self.log("ERROR", source, message)

    def history(self):

        if not LOG_FILE.exists():
            return []

        items = []

        with LOG_FILE.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    items.append(json.loads(line))

        return items


if __name__ == "__main__":

    logger = KernelLogger()

    logger.info("F0006", "Kernel Logger initialized")
    logger.info("Kernel", "Capability Registry available")
    logger.info("Kernel", "Service Registry available")
    logger.info("Kernel", "Event Bus available")
    logger.info("Kernel", "Runtime Context available")
    logger.info("Kernel", "Configuration Manager available")

    print()
    print("Kernel Log")
    print("----------")

    for item in logger.history():
        print(
            f'{item["timestamp"]} | {item["level"]:<7} | {item["source"]:<8} | {item["message"]}'
        )

    print()
    print("Log entries :", len(logger.history()))
    print("Log file    :", LOG_FILE)
