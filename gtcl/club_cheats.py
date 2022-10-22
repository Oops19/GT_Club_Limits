#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2022 https://github.com/Oops19
#


import services
from clubs.club import Club

from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils

from gtcl.club_utils import ClubUtils
from gtcl.enums.club_interaction import ClubInteraction
from gtcl.modinfo import ModInfo


log: CommonLog = CommonLogRegistry.get().register_log(f"{ModInfo.get_identity().name}", ModInfo.get_identity().name)
log.enable()


@CommonConsoleCommand(ModInfo.get_identity(), 'o19.gtcl.start', "Starts a club gathering")
def o19_cmd_gtcl_start_club_gathering(output: CommonConsoleCommandOutput):
    try:
        sim_info = CommonSimUtils.get_active_sim_info()
        cu = ClubUtils()
        options = cu.get_clubs_as_options()
        cu.show_club_picker_dialog(sim_info, ClubInteraction.StartGathering, options)
        output("ok")
    except Exception as e:
        output(f"Error: {e}")
        log.error(f"{e}", throw=True)


@CommonConsoleCommand(ModInfo.get_identity(), 'o19.gtcl.lead', "Take leadership of club(s)")
def o19_cmd_gtcl_take_leadership(output: CommonConsoleCommandOutput):
    try:
        sim_info = CommonSimUtils.get_active_sim_info()
        cu = ClubUtils()
        options = cu.get_clubs_as_options()
        cu.show_club_picker_dialog(sim_info, ClubInteraction.Lead, options)
        output("ok")
    except Exception as e:
        output(f"Error: {e}")
        log.error(f"{e}", throw=True)


@CommonConsoleCommand(ModInfo.get_identity(), 'o19.gtcl.join', "Join a (new) club")
def o19_cmd_gtcl_join_club(output: CommonConsoleCommandOutput):
    try:
        sim_info = CommonSimUtils.get_active_sim_info()  # Dangerous - the active sim should never create a club.
        cu = ClubUtils()
        options = cu.get_clubs_as_options()
        options.append(cu.get_addnew_as_option())
        cu.show_club_picker_dialog(sim_info, ClubInteraction.Join, options)
        output("ok")
    except Exception as e:
        output(f"Error: {e}")
        log.error(f"{e}", throw=True)


@CommonConsoleCommand(ModInfo.get_identity(), 'o19.gtcl.invite', "Invite sims to club")
def o19_cmd_gtcl_add_sims_to_club(output: CommonConsoleCommandOutput):
    try:
        sim_info = CommonSimUtils.get_active_sim_info()
        cu = ClubUtils()
        options = cu.get_clubs_as_options()
        cu.show_club_picker_dialog(sim_info, ClubInteraction.Invite, options)
        output("ok")
    except Exception as e:
        output(f"Error: {e}")
        log.error(f"{e}", throw=True)


@CommonConsoleCommand(ModInfo.get_identity(), 'o19.gtcl.delete', "Delete club(c)")
def o19_cmd_gtcl_delete_club(output: CommonConsoleCommandOutput):
    try:
        sim_info = CommonSimUtils.get_active_sim_info()
        cu = ClubUtils()
        options = cu.get_clubs_as_options()
        cu.show_club_picker_dialog(sim_info, ClubInteraction.Delete, options)
        output("ok")
    except Exception as e:
        output(f"Error: {e}")
        log.error(f"{e}", throw=True)


@CommonConsoleCommand(ModInfo.get_identity(), 'o19.gtcl.delete', "Delete club(c)")
def o19_cmd_gtcl_delete_club(output: CommonConsoleCommandOutput):
    try:
        sim_info = CommonSimUtils.get_active_sim_info()
        cu = ClubUtils()
        options = cu.get_clubs_as_options()
        cu.show_club_picker_dialog(sim_info, ClubInteraction.Points, options)
        output("ok")
    except Exception as e:
        output(f"Error: {e}")
        log.error(f"{e}", throw=True)


@CommonConsoleCommand(ModInfo.get_identity(), 'o19.gtcl.agjoin', "Join Active Gathering")
def o19_cmd_gtcl_print_club(output: CommonConsoleCommandOutput):
    try:
        sim_info = CommonSimUtils.get_active_sim_info()
        cu = ClubUtils()
        options = cu.get_clubs_as_options()
        cu.show_club_picker_dialog(sim_info, ClubInteraction.JoinActiveGathering, options)
        output("ok")
    except Exception as e:
        output(f"Error: {e}")
        log.error(f"{e}", throw=True)


@CommonConsoleCommand(ModInfo.get_identity(), 'o19.gtcl.print', "Log all clubs to file")
def o19_cmd_gtcl_print_club(output: CommonConsoleCommandOutput):
    try:
        cu = ClubCheats()
        cu.print_club()
        output("ok")
    except Exception as e:
        output(f"Error: {e}")
        log.error(f"{e}", throw=True)


class ClubCheats:
    def print_club(self):
        log.debug(f"Existing clubs:")
        log.debug(f"# 'Name' 'Description' (Id) - InviteOnly - 'Leader'- 'Icon'")
        try:
            club_service = services.get_club_service()
            clubs = club_service.clubs
            for club in clubs:
                name = self._get_club_name(club)
                log.debug(f"'{name}' '{club._description}' ({club.club_id}) - {club.invite_only} - '{club.leader}' - '{club.icon}'")
                # log.debug(f"{inspect.getmembers(club)}")
        except Exception as e:
            log.error(f"Error: {e}")

    @staticmethod
    def _get_club_name(club: Club) -> str:
        name = club._name
        if name is None:
            club_seed = club.club_seed
            if club_seed:
                name = f"{club_seed.__name__}"
                if name.startswith('clubSeed_InitialSeeds_'):
                    name = f"{name[22:]} (seed)"
                elif "_" in name:
                    name = f"{name.rsplit('_', 1)[1]} (seed)"
        return name
