import flet as ft
from collections import deque
from typing import Callable

class DialogQueue:
    def __init__(self, page: ft.Page):
        self.page = page
        self._queue: deque[Callable[[], None]] = deque()
        self._is_showing = False

    def enqueue(self, dialog_fn: Callable[[], None]):
        self._queue.append(dialog_fn)
        self._try_show_next()

    def _try_show_next(self):
        if self._is_showing or not self._queue:
            return

        self._is_showing = True
        dialog_fn = self._queue.popleft()

        try:
            dialog_fn()
        except Exception:
            self.notify_closed()
            raise

    def notify_closed(self):
        self._is_showing = False
        self._try_show_next()