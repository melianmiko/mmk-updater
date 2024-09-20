import asyncio
import logging
import sys
from pathlib import Path

from PyQt6.QtWidgets import QWidget
from qasync import QApplication, QEventLoop

from mmk_updater.qt.main import MmkUpdaterQt
from .generic import UpdateCheckerConfig

config = UpdateCheckerConfig(server_url="https://st.mmk.pw/openfreebuds",
                             state_location=Path.cwd() / "state.json",
                             current_version="0")


async def main():
    updater = MmkUpdaterQt(None, config)

    await updater.boot()
    print("Started")

    await updater._task
    app.exit()
    await app_close_event.wait()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("qasync._QThreadWorker").disabled = True
    logging.getLogger("qasync.QThreadExecutor").disabled = True

    app = QApplication(sys.argv)

    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)

    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set)

    root = QWidget(None)
    root.hide()

    event_loop.run_until_complete(main())
