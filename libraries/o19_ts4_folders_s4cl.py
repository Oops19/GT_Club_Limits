#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2021 https://github.com/Oops19
#

import os

from gtw_club_limits.modinfo import ModInfo
from sims4communitylib.utils.common_log_registry import CommonLogRegistry, CommonLog

log: CommonLog = CommonLogRegistry.get().register_log(f"{ModInfo.get_identity().author}_{ModInfo.get_identity().name}", ModInfo.get_identity().name)

class TS4_Folders_S4CL():
    def __init__(self):

        # If this path is not correct, change it to your Mods folder location instead.
        _home = "."  # current path
        __os = "W10"
        __env = "USERPROFILE"
        if os.name != 'nt':
            # Mac
            __os = "Mac"
            __env = 'HOME'

        try:
            _home = os.environ[__env]
        except:
            log.warn(f"{__env} is not set (detected {__os}). Set it manually!'")

        self._base_folder = os.path.join(_home, 'Documents', 'Electronic Arts', 'The Sims 4')
        log.debug(f"base_folder = '{self._base_folder}' (exists = {os.path.exists(self._base_folder)})")

        self._mods_folder = os.path.join(self._base_folder, 'Mods')
        log.debug(f"mods_folder = '{self._mods_folder}' (exists = {os.path.exists(self._mods_folder)})")

        # Location of the game's zipped binary scripts (base.zip, core.zip and simulation.zip)
        # If this path is not found properly when trying to decompile, change it to the location where you have installed The Sims 4 at, this would be the folder that contains the GameVersion.txt file
        if os.name != 'nt':
            # Mac
            self._game_folder = os.path.join(_home, 'Applications', 'The Sims 4.app', 'Contents', 'Data', 'Simulation', 'Gameplay')
        else:
            # noinspection PyBroadException
            try:
                # Windows
                import winreg as winreg
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Maxis\\The Sims 4')
                (self._game_folder, _) = winreg.QueryValueEx(key, 'Install Dir')
            except:
                self._game_folder = None
                log.warn(f"Game folder could not be set.")

        if self._game_folder:
            log.debug(f"game_folder = '{self._game_folder}' (exists = {os.path.exists(self._game_folder)})")

    @property
    def base_folder(self):
        return self._base_folder

    @property
    def mods_folder(self):
        return self._mods_folder

    @property
    def game_folder(self):
        return self._game_folder
