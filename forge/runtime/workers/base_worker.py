#!/usr/bin/env python3

from __future__ import annotations


class BaseWorker:

    NAME = "BaseWorker"
    TOPIC = "base"

    def handle(self, message):

        raise NotImplementedError
