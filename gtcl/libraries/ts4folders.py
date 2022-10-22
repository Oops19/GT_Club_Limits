#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2021 https://github.com/Oops19
#


import os
from typing import Union

from sims4communitylib.utils.common_log_registry import CommonLogRegistry, CommonLog

from gtcl.modinfo import ModInfo


log: CommonLog = CommonLogRegistry.get().register_log(f"{ModInfo.get_identity().name}", ModInfo.get_identity().name)


class TS4Folders:
    env_ts4_base_folder = 'TS4_BASE_FOLDER'
    env_ts4_game_folder = 'TS4_GAME_FOLDER'

    def __init__(self):
        if os.name == 'nt':
            __os = "W10/W11"
            __env = "USERPROFILE"
        else:
            # Mac
            __os = "Mac"
            __env = 'HOME'
        log.debug(f"Detected OS: {__os}")

        # noinspection PyBroadException
        try:
            _home = os.environ[__env]
        except:
            log.warn(f"Variable '{__env}' is not set. Consider setting it manually.'")
            _home = "."

        self._base_folder = self._set_base_folder(_home)
        log.info(f"Base folder: '{self._log_folder(self._base_folder)}'.")

        self._mods_folder = os.path.join(self._base_folder, 'Mods')
        self._data_folder = os.path.join(self._base_folder, 'mod_data', ModInfo.get_identity().base_namespace)

        self._game_folder = self._set_game_folder(_home)
        log.info(f"Game folder: '{self._log_folder(self._game_folder)}' (For most mods 'None' is just fine).")

    # noinspection PyBroadException
    @staticmethod
    def _log_folder(folder) -> str:
        _folder = folder
        if log.enabled:
            rep = {
                'USERPROFILE': '%USERPROFILE%',
                f"{os.sep}{os.environ['USERNAME']}{os.sep}": f"{os.sep}%USERNAME%{os.sep}",
                'PROGRAMFILES': '%ProgramFiles%',
                'PROGRAMFILES(X86)': '%ProgramFiles(x86)%',
                'PROGRAMW6432': '%ProgramW6432%',
                'HOME': '$HOME',
            }
            for k, v in rep.items():
                try:
                    _folder = _folder.replace(os.environ[k], v)
                except:
                    pass
        return _folder

    # noinspection PyBroadException
    @staticmethod
    def _set_base_folder(_home) -> str:
        try:
            _base_folder = os.environ[TS4Folders.env_ts4_base_folder]
            if os.path.exists(_base_folder):
                return _base_folder
            else:
                log.warn(f"'{TS4Folders.env_ts4_base_folder}' points to '{_base_folder} which doesn't exist. Please fix this.")
        except:
            log.debug(f"Set '{TS4Folders.env_ts4_base_folder}' to define a custom 'The Sims 4' folder (which contains 'Mods', ...).")

        _base_folder = os.path.dirname(os.path.abspath(__file__)).partition(f"{os.sep}Mods{os.sep}")[0]
        if os.path.exists(_base_folder):
            return _base_folder

        _base_folder = os.path.join(_home, 'Documents', 'Electronic Arts', 'The Sims 4')
        if os.path.exists(_base_folder):
            return _base_folder

        _base_folder = os.path.dirname(os.path.abspath(__file__))
        log.error(f"Could not locate the 'The Sims 4' folder. Using '{_base_folder}'.")
        return _base_folder

    # noinspection PyBroadException
    def _set_game_folder(self, _home) -> Union[None, str]:
        try:
            _game_folder = os.environ[TS4Folders.env_ts4_game_folder]
            if os.path.exists(_game_folder):
                return _game_folder
            else:
                log.warn(f"'{TS4Folders.env_ts4_base_folder}' points to '{_game_folder} which doesn't exist. Please fix this.")
        except:
            log.debug(f"Set '{TS4Folders.env_ts4_game_folder}' to define a custom 'The Sims 4' folder (which contains 'Game', 'EPnn', 'FP01', 'GPnn', 'SPnn', ...).")

        if os.name == 'nt':
            try:
                # Windows
                import winreg as winreg
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Maxis\\The Sims 4')
                (_game_folder, _) = winreg.QueryValueEx(key, 'Install Dir')
                if os.path.exists(_game_folder):
                    return _game_folder
                else:
                    log.warn(f"'{_game_folder} (winreg) doesn't exist. Trying to locate a different folder.")
            except Exception as e:
                self._game_folder = None
                log.info(f"Game folder could not be set ({e}).")

            for program_files in ['ProgramFiles(x86)', 'ProgramFiles', 'ProgramW6432']:
                try:
                    _program_files = os.environ[program_files]
                    _game_folder = os.path.join(_program_files, 'Origin Games', 'The Sims 4')
                    if os.path.exists(os.path.join(_game_folder, 'Game')):
                        return _game_folder
                except Exception:
                    pass
        else:
            _game_folder = os.path.join(os.environ['HOME'], 'Applications', 'The Sims 4.app', 'Contents')
            if os.path.exists(_game_folder):
                return _game_folder

        return None

    @property
    def base_folder(self):
        return self._base_folder

    @property
    def mods_folder(self):
        return self._mods_folder

    @property
    def data_folder(self):
        return self._data_folder

    @property
    def game_folder(self):
        return self._game_folder
