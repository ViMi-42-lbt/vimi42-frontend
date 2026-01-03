from app.core.theme.theme_mode import ThemeMode


class AppState:
    def __init__(self):
        self.theme_mode: ThemeMode = ThemeMode.SYSTEM
        self._listeners: list[callable] = []

    def set_theme_mode(self, mode: ThemeMode) -> None:
        if self.theme_mode != mode:
            self.theme_mode = mode
            self._notify()

    def subscribe(self, callback: callable) -> None:
        self._listeners.append(callback)

    def _notify(self) -> None:
        for callback in self._listeners:
            callback()