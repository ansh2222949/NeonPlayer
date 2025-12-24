import time
import win32gui
import win32con
import threading


class PinHandler:
    def __init__(self):
        self.is_pinned = False
        self.hwnd = None
        self._lock = threading.Lock()

    def _get_hwnd(self, window):

        with self._lock:

            if self.hwnd and win32gui.IsWindow(self.hwnd):
                return self.hwnd

            for _ in range(15):
                hwnd = win32gui.FindWindow(None, window.title)
                if hwnd:
                    self.hwnd = hwnd
                    return hwnd
                time.sleep(0.05)

            return None

    def toggle(self, window):

        try:
            hwnd = self._get_manager_hwnd(window) if hasattr(
                self, '_get_manager_hwnd') else self._get_hwnd(window)

            if not hwnd or not win32gui.IsWindow(hwnd):
                print("[PinHandler] Active window handle not found.")
                return self.is_pinned

            flags = win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE

            if not self.is_pinned:
                # Set Always on Top
                win32gui.SetWindowPos(
                    hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, flags)
            else:
                # Remove Always on Top
                win32gui.SetWindowPos(
                    hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, flags)

            self.is_pinned = not self.is_pinned
            return self.is_pinned

        except Exception as e:
            print(f"[PinHandler] Critical Error: {e}")
            return self.is_pinned

    def force_unpin(self):

        if self.hwnd and win32gui.IsWindow(self.hwnd):
            win32gui.SetWindowPos(self.hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                                  win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
            self.is_pinned = False
