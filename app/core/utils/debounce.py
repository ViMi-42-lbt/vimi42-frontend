import flet as ft
from typing import Callable, Any


class Debounce:
    def __init__(self, page: ft.Page, delay: float):
        self.page = page
        self.delay = delay
        self._timer_id: int | None = None
        self.page.on_close = self._dispose

    def run(self, callback: Callable[..., Any], *args, **kwargs):
        if self._timer_id is not None:
            self.page.timer.cancel(self._timer_id)
            self._timer_id = None

        def _wrapper():
            callback(*args, **kwargs)
            self._timer_id = None

        self._timer_id = self.page.timer(self.delay, _wrapper)

    def cancel(self):
        if self._timer_id is not None:
            self.page.timer.cancel(self._timer_id)
            self._timer_id = None

    def _dispose(self, _=None):
        self.cancel()
