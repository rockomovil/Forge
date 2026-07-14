#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

from forge.kernel.services.kernel_service import KernelService


class KernelRuntime:

    def __init__(self):

        self.root = Path(__file__).resolve().parents[3]
        self.runtime = self.root / "runtime" / "kernel"

    def service(self, module: str, status: str) -> KernelService:

        return KernelService(module, status)
