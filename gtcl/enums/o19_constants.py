#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2022 https://github.com/Oops19
#


import os

from gtcl.libraries.ts4folders import TS4Folders


# Constant definitions
class O19Constants:
    def __init__(self):
        # ts4f = TS4_Folders_S4CL()
        # DATA_DIRECTORY = os.path.join(ts4f.base_folder, 'mod_data', 'gtw_club_limits')

        ts4f = TS4Folders()
        data_folder = ts4f.data_folder
        os.makedirs(data_folder, exist_ok=True)

        self.CONFIG_FILE = os.path.join(data_folder, 'clubs.ini')
        self.CONFIG_FILE_W = os.path.join(data_folder, 'clubs.ini.current.ini')

        self.MAX_MEMBERS_UNLIMITED = 'MAX_MEMBERS_UNLIMITED'
        self.MAX_CLUB_MEMBERS = 'MAX_CLUB_MEMBERS'

        self.MAX_CLUBS_UNLIMITED = 'MAX_CLUBS_UNLIMITED'
        self.MAX_CLUBS = 'MAX_CLUBS'

        self.NO_CLUB_ZONE_VALIDATION = 'NO_CLUB_ZONE_VALIDATION'
        self.NO_CLUB_REQUIREMENTS_VALIDATION = 'NO_CLUB_REQUIREMENTS_VALIDATION'
