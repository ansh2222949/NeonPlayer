import asyncio
import threading
import base64
import ctypes

from winsdk.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager as Manager
)
from winsdk.windows.media import MediaPlaybackStatus
from winsdk.windows.storage.streams import DataReader


class MediaController:
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        self.manager = None
        self.data_cache = self._offline()

        t = threading.Thread(target=self._start_loop, daemon=True)
        t.start()

    # ================= LOOP =================
    def _start_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    async def _get_manager(self):
        if not self.manager:
            self.manager = await Manager.request_async()
        return self.manager

    # ================= DATA FETCH =================
    async def _update_data(self):
        try:
            manager = await self._get_manager()
            session = manager.get_current_session()

            if not session:
                self.data_cache = self._offline()
                return

            props = await session.try_get_media_properties_async()
            timeline = session.get_timeline_properties()
            playback = session.get_playback_info()

            # -------- THUMBNAIL --------
            thumb = ""
            if props.thumbnail:
                try:
                    stream = await props.thumbnail.open_read_async()
                    reader = DataReader(stream.get_input_stream_at(0))
                    await reader.load_async(stream.size)
                    buf = reader.read_buffer(stream.size)
                    addr = ctypes.addressof(ctypes.c_char.from_buffer(buf))
                    data = ctypes.string_at(addr, stream.size)
                    thumb = "data:image/png;base64," + \
                        base64.b64encode(data).decode()
                except:
                    thumb = ""

            pos = timeline.position.total_seconds()
            end = timeline.end_time.total_seconds()

            self.data_cache = {
                "title": props.title or "No Title",
                "artist": props.artist or "Unknown",
                "thumbnail": thumb,
                "progress": (pos / end * 100) if end > 0 else 0,
                "position": self._fmt(pos),
                "duration": self._fmt(end),
                "is_playing": playback.playback_status == MediaPlaybackStatus.PLAYING,
            }

        except Exception:
            self.data_cache = self._offline()

    def fetch_data(self):
        asyncio.run_coroutine_threadsafe(self._update_data(), self.loop)
        return self.data_cache

    # ================= CONTROLS =================
    def call(self, action):
        async def _cmd():
            manager = await self._get_manager()
            session = manager.get_current_session()
            if not session:
                return
            try:
                if action == "play_pause":
                    await session.try_toggle_play_pause_async()
                elif action == "next":
                    await session.try_skip_next_async()
                elif action == "prev":
                    await session.try_skip_previous_async()
            except Exception as e:
                print("Control error:", e)
        asyncio.run_coroutine_threadsafe(_cmd(), self.loop)

    # ================= SEEK =================
    def seek_to(self, percent):
        async def _seek():
            try:
                manager = await self._get_manager()
                session = manager.get_current_session()
                if not session:
                    return

                timeline = session.get_timeline_properties()
                if not timeline or not timeline.end_time:
                    return

                total_seconds = timeline.end_time.total_seconds()
                if total_seconds <= 0:
                    return

                target_ticks = int((percent / 100) *
                                   total_seconds * 10_000_000)

                await session.try_change_playback_position_async(target_ticks)
            except Exception:
                pass

        asyncio.run_coroutine_threadsafe(_seek(), self.loop)

    # ================= UTILS =================
    def _fmt(self, s):
        return f"{int(s // 60)}:{int(s % 60):02d}"

    def _offline(self):
        return {
            "title": "No Media", "artist": "Offline", "thumbnail": "",
            "progress": 0, "position": "0:00", "duration": "0:00", "is_playing": False,
        }
