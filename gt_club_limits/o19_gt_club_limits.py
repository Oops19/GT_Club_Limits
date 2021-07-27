#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2021 https://github.com/Oops19
#

import ast
import os

from gt_club_limits.modinfo import ModInfo
from libraries.o19_ts4_folders_s4cl import TS4_Folders_S4CL
from sims4.math import MAX_INT32

from clubs.club import Club
from clubs.club_tuning import ClubTunables
from clubs.club_service import ClubService
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry, CommonLog

log: CommonLog = CommonLogRegistry.get().register_log(f"{ModInfo.get_identity().author}_{ModInfo.get_identity().name}", ModInfo.get_identity().name)
log.enable()
log.info("GT Club Limits")


# Constant definitions
class O19Definitions:
    def __init__(self):
        ts4f = TS4_Folders_S4CL()
        DATA_DIRECTORY = os.path.join(ts4f.base_folder, 'mod_data', 'gtw_club_limits')
        os.makedirs(DATA_DIRECTORY, exist_ok=True)

        self.CONFIG_FILE = os.path.join(DATA_DIRECTORY, 'clubs.ini')
        self.CONFIG_FILE_W = os.path.join(DATA_DIRECTORY, 'clubs.ini.current.ini')

        self.MAX_MEMBERS_UNLIMITED = 'MAX_MEMBERS_UNLIMITED'
        self.MAX_CLUB_MEMBERS = 'MAX_CLUB_MEMBERS'

        self.MAX_CLUBS_UNLIMITED = 'MAX_CLUBS_UNLIMITED'
        self.MAX_CLUBS = 'MAX_CLUBS'

        self.NO_CLUB_ZONE_VALIDATION = 'NO_CLUB_ZONE_VALIDATION'
        self.NO_CLUB_REQUIREMENTS_VALIDATION = 'NO_CLUB_REQUIREMENTS_VALIDATION'


# Default configuration is used if config file CONFIG_FILE is missing.
D = O19Definitions()
configuration: dict = {
    D.MAX_MEMBERS_UNLIMITED: True,  # Set this to False to use the MAX_CLUB_MEMBERS value.
    D.MAX_CLUB_MEMBERS: 24,  # The default maximum number of Sims that can be in a single Club. Invite-only, no '+' sign!

    D.MAX_CLUBS_UNLIMITED: True,  # Set this to False to use the MAX_CLUBS value.
    D.MAX_CLUBS: 9,  # The maximum number of Clubs a single Sim can be a member of at one time. Invite-only, no '+' sign!

    D.NO_CLUB_ZONE_VALIDATION: True,  # Every zone can be used for gatherings
    D.NO_CLUB_REQUIREMENTS_VALIDATION: True,  # Non-Human sims and sims without proper requirements may be added to a club.
}

# Read the user configuration
# noinspection PyBroadException
try:
    if os.path.isfile(D.CONFIG_FILE):
        with open(D.CONFIG_FILE, 'rt') as fp:
            user_configuration = ast.literal_eval(fp.read())
        configuration.update(user_configuration)
        log.info(f"Read configuration file '{D.CONFIG_FILE}'.")

except:
    log.warn(f"Error reading '{D.CONFIG_FILE}'.")

# Write the current configuration if missing
# noinspection PyBroadException
try:
    if not os.path.isfile(D.CONFIG_FILE_W):
        with open(D.CONFIG_FILE_W, 'wt') as fp:
            fp.write(f"# To modify the configuration rename '{D.CONFIG_FILE_W}' to  '{D.CONFIG_FILE}' and edit it.\n")
            fp.write(f"# Delete '{D.CONFIG_FILE}' if it exists to use the default configuration.\n")
            fp.write(f"# Delete '{D.CONFIG_FILE_W}' to have it created during startup. It will not be updated if it exists.\n")
            fp.write("{\n")
            fp.write(f"\t'{D.MAX_MEMBERS_UNLIMITED}': {bool(configuration.get(D.MAX_MEMBERS_UNLIMITED))},  # Set this to False to use the MAX_CLUB_MEMBERS value below.\n")
            fp.write(f"\t'{D.MAX_CLUB_MEMBERS}': {int(configuration.get(D.MAX_CLUB_MEMBERS))},  # The default maximum number of Sims that can be in a single Club. Invite-only, no '+' sign!\n")
            fp.write(f"\t\n")
            fp.write(f"\t'{D.MAX_CLUBS_UNLIMITED}': {bool(configuration.get(D.MAX_CLUBS_UNLIMITED))},  # Set this to False to use the MAX_CLUBS value below.\n")
            fp.write(f"\t'{D.MAX_CLUBS}': {int(configuration.get(D.MAX_CLUBS))},  # The maximum number of Clubs a single Sim can be a member of at one time. Invite-only, no '+' sign!\n")
            fp.write(f"\t\n")
            fp.write(f"\t'{D.NO_CLUB_ZONE_VALIDATION}': {bool(configuration.get(D.NO_CLUB_ZONE_VALIDATION))},  # Every zone can be used for gatherings.\n")
            fp.write(f"\t'{D.NO_CLUB_REQUIREMENTS_VALIDATION}': {bool(configuration.get(D.NO_CLUB_REQUIREMENTS_VALIDATION))},  # Non-Human sims and sims without proper requirements may be added to a club.\n")
            fp.write("}\n")
            log.info(f"Wrote configuration file '{D.CONFIG_FILE}'.")
except:
    log.warn(f"Error writing '{D.CONFIG_FILE}'.")

# Parse the configuration
if bool(configuration.get(D.MAX_MEMBERS_UNLIMITED)):
    MAX_CLUB_MEMBERS: int = MAX_INT32
else:
    MAX_CLUB_MEMBERS: int = int(configuration.get(D.MAX_CLUB_MEMBERS))

if bool(configuration.get(D.MAX_CLUBS_UNLIMITED)):
    MAX_CLUBS: int = MAX_INT32
else:
    MAX_CLUBS: int = int(configuration.get(D.MAX_CLUBS))

# The Sims 4 related code starts here
# noinspection PyBroadException
try:
    ClubTunables.DEFAULT_MEMBER_CAP = MAX_CLUB_MEMBERS
except:
    pass
# noinspection PyBroadException
try:
    ClubTunables.MAX_CLUBS_PER_SIM = MAX_CLUBS
except:
    pass

'''
def can_sim_info_join(self, new_sim_info):
    False if sim is already in club - keep this as-is
    False if get_member_cap() is too small --> see o19_get_member_cap()
    False is validate_sim_info --> see o19_validate_sim_info()
    False if can_sim_info_join_more_clubs --> see o19_can_sim_info_join_more_clubs()
    True
'''


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Club, Club.get_member_cap.__name__)
def o19_get_member_cap(original, self, *args, **kwargs) -> int:
    global MAX_CLUB_MEMBERS
    return MAX_CLUB_MEMBERS


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Club, Club.is_zone_valid_for_gathering.__name__)
def o19_is_zone_valid_for_gathering(original, self, *args, **kwargs) -> bool:
    if bool(configuration.get(D.NO_CLUB_ZONE_VALIDATION)):
        return True
    else:
        return original(self, *args, **kwargs)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Club, Club.validate_sim_info.__name__)
def o19_validate_sim_info(original, self, *args, **kwargs) -> bool:
    if bool(configuration.get(D.NO_CLUB_REQUIREMENTS_VALIDATION)):
        return True
    else:
        return original(self, *args, **kwargs)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), ClubService, ClubService.can_sim_info_join_more_clubs.__name__)
def o19_can_sim_info_join_more_clubs(original, self, *args, **kwargs) -> bool:
    if bool(configuration.get(D.MAX_CLUBS_UNLIMITED)):
        return True
    else:
        return original(self, *args, **kwargs)
