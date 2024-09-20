from dataclasses import dataclass, field, fields
from datetime import timedelta
from enum import Enum
from pathlib import Path
from typing import Optional


@dataclass
class UpdateCheckerConfig:
    class NotifyMethod:
        NONE = 0
        POP_UP = 1
        DESKTOP_NOTIFICATION = 2

    server_url: str
    current_version: str
    state_location: Path

    app_display_name: str = "My Application"

    notify_method: int = NotifyMethod.POP_UP
    ppa_file_glob: str = "/etc/apt/sources.list.d/melianmiko-repo*"
    ignore_if_ppa_is_present: bool = True
    check_interval: timedelta = timedelta(days=1)
    show_interval: timedelta = timedelta(days=3)


@dataclass
class ReleaseInfo:
    app: str = ""
    title: str = ""
    version: str = ""
    website: str = ""
    changelog: list[str] = field(default_factory=list)
    windows: Optional[list[dict]] = None

    def __init__(self, **kwargs):
        names = set([f.name for f in fields(self)])
        for k, v in kwargs.items():
            if k in names:
                setattr(self, k, v)


@dataclass
class StateData:
    last_checked: str = "1970-01-01T00:00:00"
    last_shown: str = "1970-01-01T00:00:00"
    release_info_json: str = "null"


class IMmkUpdater:
    def __init__(self, config: UpdateCheckerConfig):
        self.config = config
        self.release_info: Optional[ReleaseInfo] = None
        self.selected_target: Optional[dict] = None

    @property
    def update_through_ppa(self):
        return False

    @property
    def has_update(self):
        return False

    async def boot(self):
        raise NotImplementedError

    async def check_now(self, user_triggered: bool = False):
        raise NotImplementedError
