#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2022 https://github.com/Oops19
#

import ast
import os

from gt_club_limits.enums.o19_constants import O19Constants
from gt_club_limits.modinfo import ModInfo

from sims4.math import MAX_INT32
from clubs.club import Club
from clubs.club_tuning import ClubTunables
from clubs.club_service import ClubService

from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry, CommonLog


log: CommonLog = CommonLogRegistry.get().register_log(f"{ModInfo.get_identity().name}", ModInfo.get_identity().name)
log.enable()
log.debug(f"Starting {ModInfo.get_identity().name} v{ModInfo.get_identity().version} ")

# Default configuration is used if config file CONFIG_FILE is missing.
CONFIGURATION_DATA = O19Constants()

# noinspection GrazieInspection
configuration: dict = {
    CONFIGURATION_DATA.MAX_MEMBERS_UNLIMITED: True,  # Set this to False to use the MAX_CLUB_MEMBERS value.
    CONFIGURATION_DATA.MAX_CLUB_MEMBERS: 24,  # The default maximum number of Sims that can be in a single Club. Invite-only, no '+' sign!

    CONFIGURATION_DATA.MAX_CLUBS_UNLIMITED: True,  # Set this to False to use the MAX_CLUBS value.
    CONFIGURATION_DATA.MAX_CLUBS: 9,  # The maximum number of Clubs a single Sim can be a member of at one time. Invite-only, no '+' sign!

    CONFIGURATION_DATA.NO_CLUB_ZONE_VALIDATION: True,  # Every zone can be used for gatherings
    CONFIGURATION_DATA.NO_CLUB_REQUIREMENTS_VALIDATION: True,  # Non-Human sims and sims without proper requirements may be added to a club.
}

# Read the user configuration
# noinspection PyBroadException
try:
    if os.path.isfile(CONFIGURATION_DATA.CONFIG_FILE):
        with open(CONFIGURATION_DATA.CONFIG_FILE, 'rt') as fp:
            user_configuration = ast.literal_eval(fp.read())
        configuration.update(user_configuration)
        log.info(f"Read configuration file '{CONFIGURATION_DATA.CONFIG_FILE}'.")

except:
    log.warn(f"Error reading '{CONFIGURATION_DATA.CONFIG_FILE}'.")

# Write the current configuration if missing
# noinspection PyBroadException
try:
    if not os.path.isfile(CONFIGURATION_DATA.CONFIG_FILE_W):
        with open(CONFIGURATION_DATA.CONFIG_FILE_W, 'wt') as fp:
            fp.write(f"# To modify the configuration rename '{CONFIGURATION_DATA.CONFIG_FILE_W}' to '{CONFIGURATION_DATA.CONFIG_FILE}' and edit it.\n")
            fp.write(f"# Delete '{CONFIGURATION_DATA.CONFIG_FILE}' if it exists to use the default configuration.\n")
            fp.write(f"# Delete '{CONFIGURATION_DATA.CONFIG_FILE_W}' to have it created during startup. It will not be updated if it exists.\n")
            fp.write("{\n")
            fp.write(f"\t'{CONFIGURATION_DATA.MAX_MEMBERS_UNLIMITED}': {bool(configuration.get(CONFIGURATION_DATA.MAX_MEMBERS_UNLIMITED))},  # Set this to False to use the MAX_CLUB_MEMBERS value below.\n")
            fp.write(f"\t'{CONFIGURATION_DATA.MAX_CLUB_MEMBERS}': {int(configuration.get(CONFIGURATION_DATA.MAX_CLUB_MEMBERS))},  # The default maximum number of Sims that can be in a single Club. Invite-only, no '+' sign!\n")
            fp.write(f"\t\n")
            fp.write(f"\t'{CONFIGURATION_DATA.MAX_CLUBS_UNLIMITED}': {bool(configuration.get(CONFIGURATION_DATA.MAX_CLUBS_UNLIMITED))},  # Set this to False to use the MAX_CLUBS value below.\n")
            fp.write(f"\t'{CONFIGURATION_DATA.MAX_CLUBS}': {int(configuration.get(CONFIGURATION_DATA.MAX_CLUBS))},  # The maximum number of Clubs a single Sim can be a member of at one time. Invite-only, no '+' sign!\n")
            fp.write(f"\t\n")
            fp.write(f"\t'{CONFIGURATION_DATA.NO_CLUB_ZONE_VALIDATION}': {bool(configuration.get(CONFIGURATION_DATA.NO_CLUB_ZONE_VALIDATION))},  # Every zone can be used for gatherings.\n")
            fp.write(f"\t'{CONFIGURATION_DATA.NO_CLUB_REQUIREMENTS_VALIDATION}': {bool(configuration.get(CONFIGURATION_DATA.NO_CLUB_REQUIREMENTS_VALIDATION))},  # Non-Human sims and sims without proper requirements may be added to a club.\n")
            fp.write("}\n")
            log.info(f"Wrote configuration file '{CONFIGURATION_DATA.CONFIG_FILE}'.")
except:
    log.warn(f"Error writing '{CONFIGURATION_DATA.CONFIG_FILE}'.")

# Parse the configuration
if bool(configuration.get(CONFIGURATION_DATA.MAX_MEMBERS_UNLIMITED)):
    MAX_CLUB_MEMBERS: int = MAX_INT32
else:
    MAX_CLUB_MEMBERS: int = int(configuration.get(CONFIGURATION_DATA.MAX_CLUB_MEMBERS))

if bool(configuration.get(CONFIGURATION_DATA.MAX_CLUBS_UNLIMITED)):
    MAX_CLUBS: int = MAX_INT32
else:
    MAX_CLUBS: int = int(configuration.get(CONFIGURATION_DATA.MAX_CLUBS))

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


# noinspection PyUnusedLocal
@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Club, Club.get_member_cap.__name__)
def o19_get_member_cap(original, self, *args, **kwargs) -> int:
    global MAX_CLUB_MEMBERS
    return MAX_CLUB_MEMBERS


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Club, Club.is_zone_valid_for_gathering.__name__)
def o19_is_zone_valid_for_gathering(original, self, *args, **kwargs) -> bool:
    if bool(configuration.get(CONFIGURATION_DATA.NO_CLUB_ZONE_VALIDATION)):
        return True
    else:
        return original(self, *args, **kwargs)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Club, Club.validate_sim_info.__name__)
def o19_validate_sim_info(original, self, *args, **kwargs) -> bool:
    if bool(configuration.get(CONFIGURATION_DATA.NO_CLUB_REQUIREMENTS_VALIDATION)):
        return True
    else:
        return original(self, *args, **kwargs)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), ClubService, ClubService.can_sim_info_join_more_clubs.__name__)
def o19_can_sim_info_join_more_clubs(original, self, *args, **kwargs) -> bool:
    if bool(configuration.get(CONFIGURATION_DATA.MAX_CLUBS_UNLIMITED)):
        return True
    else:
        return original(self, *args, **kwargs)
