import asyncio

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QWidget

from mmk_updater.generic import UpdateCheckerConfig
from mmk_updater.main import MmkUpdaterComon
from mmk_updater.qt.confirm_dialog import MmkUpdaterConfirmDialog


class MmkUpdaterQt(MmkUpdaterComon):
    def __init__(self, parent: QWidget, config: UpdateCheckerConfig):
        super().__init__(config)
        self.parent = parent
        self.confirm_dialog = MmkUpdaterConfirmDialog(parent)

    async def show_update_confirm(self) -> bool:
        self.confirm_dialog.fill_window(self)
        return await self.confirm_dialog.get_response()

    async def show_update_progress(self):
        self.confirm_dialog.progress_mode()

    async def set_update_progress(self, value: int):
        self.confirm_dialog.progress.setValue(value)

    async def hide_update_progress(self):
        self.confirm_dialog.hide()

    async def show_dialog_message(self, text: str):
        ev = asyncio.Event()

        def _trigger():
            ev.set()

        msg = QMessageBox(self.parent)
        msg.setText(text)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.buttonClicked.connect(_trigger)

        msg.show()
        await ev.wait()
        msg.hide()
