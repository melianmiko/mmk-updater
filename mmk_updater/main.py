import asyncio
import glob
import json
import logging
import subprocess
import sys
from dataclasses import asdict
from datetime import datetime
from functools import cached_property
from pathlib import Path
from typing import Optional

import aiohttp

from mmk_updater.generic import IMmkUpdater, UpdateCheckerConfig, ReleaseInfo, StateData
from mmk_updater.i18n import t

log = logging.getLogger("MmkUpdaterComon")


class MmkUpdaterComon(IMmkUpdater):
    def __init__(self, config: UpdateCheckerConfig):
        super().__init__(config)
        self._task: Optional[asyncio.Task] = None

        self.state = StateData()
        if config.state_location.is_file():
            with open(config.state_location, "r") as f:
                self.state = StateData(**json.load(f))

    async def check_now(self, user_triggered: bool = False):
        async with aiohttp.ClientSession() as session:
            release_info_url = f"{self.config.server_url}/release.json"
            log.debug(f"Fetching release info from {release_info_url}")

            allow_since = datetime.fromisoformat(self.state.last_checked) + self.config.check_interval
            if allow_since < datetime.now():
                # Download release info
                try:
                    async with session.get(release_info_url) as release_info_rq:
                        self.release_info = ReleaseInfo(**await release_info_rq.json())
                    # Update last check time
                    self.state.last_checked = datetime.now().isoformat()
                    self.state.release_info_json = json.dumps(asdict(self.release_info))
                    self.save_state()
                except aiohttp.ClientError:
                    log.error(f"Can't check for updates, will try again later")
                    if user_triggered:
                        await self.show_dialog_message("Can't check for updates, network error")
                    return
            else:
                log.debug("Use cached release info due to check interval restriction")

            # If on latest release...
            if self.config.current_version == self.release_info.version:
                log.debug("No updates")
                if user_triggered:
                    await self.show_dialog_message(t("You're using latest version"))
                return

            # If win32, select target
            self.selected_target = self.release_info.windows[0]
            log.info(f"url={self.selected_target['url']}, size={self.selected_target['size']}")

            # Dismiss
            allow_since = datetime.fromisoformat(self.state.last_shown) + self.config.show_interval
            if allow_since >= datetime.now() and not user_triggered:
                log.debug("Dismiss, due to show interval")
                return

            # Begin UI staff
            if user_triggered or self.config.notify_method == UpdateCheckerConfig.NotifyMethod.POP_UP:
                update_now = await self.show_update_confirm()
            elif self.config.notify_method == UpdateCheckerConfig.NotifyMethod.DESKTOP_NOTIFICATION:
                update_now = await self.show_notification("New version is available, click here to view")
                if update_now:
                    update_now = await self.show_update_confirm()
            else:
                update_now = False

            if update_now is False:
                log.info("Save last showed time")
                self.state.last_shown = datetime.now().isoformat()
                self.save_state()

            if not update_now:
                return

            # Preparations for download
            fn = self.selected_target['url'].split("/")[-1]
            file_path = Path.home() / fn
            if file_path.exists():
                file_path.unlink()
            await self.show_update_progress()

            # Download with progressbar
            with open(file_path, "wb") as f:
                async with session.get(self.selected_target['url']) as r:
                    total_size = int(r.headers.get("content-length", "0"))
                    read_size = 0
                    async for chunk in r.content.iter_chunked(8192):
                        # noinspection PyTypeChecker
                        read_size += len(chunk)
                        await self.set_update_progress(int(read_size / total_size * 100))
                        # noinspection PyTypeChecker
                        f.write(chunk)
            log.info("File ready")
            await self.hide_update_progress()

            # Execute file
            if sys.platform == "win32":
                no_console = subprocess.STARTUPINFO()
                no_console.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                subprocess.Popen([str(file_path)], startupinfo=no_console, shell=True)
            else:
                await self.show_dialog_message(f"File downloaded, install it manually: {file_path}")

            log.debug("Closed")

    async def boot(self):
        await self.close()

        log.debug("Will check for updates in background...")
        self.release_info = json.loads(self.state.release_info_json)
        if self.release_info is not None:
            self.release_info = ReleaseInfo(**self.release_info)
        self._task = asyncio.create_task(self.check_now(False))

    async def close(self):
        if self._task is not None:
            self._task.cancel()
            await self._task
            self._task = None

    async def show_notification(self, text: str, wait: bool = True):
        log.info(f"Notification text={text}")
        return True

    async def show_update_confirm(self) -> bool:
        log.info("Dummy update dialog, will auto-confirm")
        return True

    async def show_update_progress(self):
        log.info("Downloading...")

    async def set_update_progress(self, value: int):
        log.info(f"{value}%")

    async def hide_update_progress(self):
        log.info("Downloaded, dialog hidden")

    async def show_dialog_message(self, text: str):
        log.info(f"Dialog: {text}")

    def save_state(self):
        with open(self.config.state_location, "w") as f:
            json.dump(asdict(self.state), f)

    @cached_property
    def update_through_ppa(self):
        g = glob.glob(self.config.ppa_file_glob)
        return len(g) > 0 and self.config.ignore_if_ppa_is_present

    @property
    def has_update(self):
        if self.release_info is None:
            return False
        return self.config.current_version != self.release_info.version
