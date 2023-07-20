from mmk_updater import UpdaterTool
from mmk_updater.ui_tkinter import TkinterUiMod
import logging

ui_mod = TkinterUiMod()

logging.basicConfig(level=logging.DEBUG)
updater = UpdaterTool("https://st.mmk.pw/zepp_player/release.json", "0.1", ui_mod)
updater.force_show = True
# updater.ignore_ppa = False
updater.start()
