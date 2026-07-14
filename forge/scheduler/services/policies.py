#!/usr/bin/env python3

from __future__ import annotations


class LeastLoadedIdlePolicy:

    NAME = "LEAST_LOADED_IDLE"

    def select(
        self,
        workers: dict,
    ) -> str | None:

        idle = [
            (name, data)
            for name, data in workers.items()
            if data["state"] == "IDLE"
        ]

        if not idle:
            return None

        idle.sort(
            key=lambda item: (
                item[1]["running_jobs"],
                item[1]["completed_jobs"],
                item[0],
            )
        )

        return idle[0][0]
