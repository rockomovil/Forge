#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

CONFIG_FILE = ROOT / "runtime" / "config" / "forge_config.json"

DEFAULT_CONFIG = {
    "forge": {
        "name": "Forge",
        "version": "0.1",
        "mode": "BOOTSTRAP"
    },
    "kernel": {
        "autoload_services": True,
        "autoload_capabilities": True,
        "event_bus_enabled": True
    },
    "workspace": {
        "auto_discovery": True
    },
    "security": {
        "human_control_required": True,
        "autonomous_execution": False
    },
    "logging": {
        "level": "INFO"
    }
}


class ConfigurationManager:

    def __init__(self):

        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)

        if not CONFIG_FILE.exists():
            CONFIG_FILE.write_text(
                json.dumps(
                    DEFAULT_CONFIG,
                    indent=2,
                    ensure_ascii=False
                )
            )

    def load(self):
        return json.loads(CONFIG_FILE.read_text())

    def save(self, config):
        CONFIG_FILE.write_text(
            json.dumps(
                config,
                indent=2,
                ensure_ascii=False
            )
        )


if __name__ == "__main__":

    cfg = ConfigurationManager()

    data = cfg.load()

    print()
    print("Forge Configuration")
    print("-------------------")

    for section, values in data.items():
        print()
        print(f"[{section}]")

        for key, value in values.items():
            print(f"{key:<24} : {value}")

    print()
    print("Configuration file:")
    print(CONFIG_FILE)
