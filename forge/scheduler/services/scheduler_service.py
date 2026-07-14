#!/usr/bin/env python3

from __future__ import annotations


class SchedulerService:
    """
    Servicio central de planificación.

    Toda decisión de asignación de workers deberá pasar por esta
    interfaz. Las políticas de planificación podrán cambiar sin
    modificar el Runtime.
    """

    def __init__(self, policy):

        self.policy = policy

    def select_worker(
        self,
        workers: dict,
    ) -> str | None:

        return self.policy.select(workers)
