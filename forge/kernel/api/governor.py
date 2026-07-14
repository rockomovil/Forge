#!/usr/bin/env python3

from __future__ import annotations


class GovernorAPI:

    def evaluate(self, metrics: dict):

        return {
            "decision": "KEEP_CONFIGURATION",
            "metrics": metrics,
        }
