import asyncio
from enum import Enum

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QMainWindow

from mmk_updater.generic import IMmkUpdater
from mmk_updater.i18n import t
from mmk_updater.qt.designer.update_confirm_dialg import Ui_MainWindow
from mmk_updater.utils import sizeof_fmt


class MmkUpdaterConfirmDialog(Ui_MainWindow, QMainWindow):
    class Response(Enum):
        DISMISS = 0
        LATER = 1
        CONFIRM = 2

    def __init__(self):
        super().__init__(None)
        self.setupUi(self)
        self.setVisible(False)
        self.response: MmkUpdaterConfirmDialog.Response = MmkUpdaterConfirmDialog.Response.DISMISS
        self._event = asyncio.Event()

    async def get_response(self):
        self._event.clear()
        self.show()
        await self._event.wait()

        if self.response == MmkUpdaterConfirmDialog.Response.CONFIRM:
            return True

        self.hide()
        if self.response == MmkUpdaterConfirmDialog.Response.LATER:
            return False
        return None

    def progress_mode(self):
        self.show()
        self.progress.setValue(0)
        self.progress.setVisible(True)
        self.action_bar.setVisible(False)

    def fill_window(self, ctx: IMmkUpdater):
        self.header.setText(t("New version available"))
        self.app_label.setText(ctx.config.app_display_name)
        self.version.setText(ctx.release_info.version)
        self.changelog.setText("\n".join(ctx.release_info.changelog))

        self.action_bar.setVisible(True)
        self.progress.setVisible(False)

        self.button_confirm.setVisible(not ctx.update_through_ppa)
        self.button_later.setVisible(not ctx.update_through_ppa)

        if ctx.update_through_ppa:
            self.footer.setText(t("Use your system package manager to get this update"))
        elif ctx.selected_target is not None:
            self.footer.setText(
                t("Download size:") + " " + sizeof_fmt(ctx.selected_target['size'])
            )
        else:
            self.footer.setText(t("You'll be redirected to website for update"))

        self.adjustSize()

    @pyqtSlot()
    def on_confirm(self):
        self.response = MmkUpdaterConfirmDialog.Response.CONFIRM
        self._event.set()

    @pyqtSlot()
    def on_later(self):
        self.response = MmkUpdaterConfirmDialog.Response.LATER
        self._event.set()

    @pyqtSlot()
    def on_dismiss(self):
        self.response = MmkUpdaterConfirmDialog.Response.DISMISS
        self._event.set()
