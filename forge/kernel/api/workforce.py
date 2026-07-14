#!/usr/bin/env python3

from __future__ import annotations


class WorkforceAPI:

    def allocate(self, capability: str):

        return {
            "capability": capability,
            "state": "ALLOCATED",
        }
