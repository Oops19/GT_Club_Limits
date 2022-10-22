#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2022 https://github.com/Oops19
#


import functools
from typing import List, Union, Tuple

import services
import sims4
import sims4.resources
import telemetry_helper
from bucks.bucks_enums import BucksType
from clubs.club import Club
from clubs.club_telemetry import TELEMETRY_HOOK_CLUB_CREATE, TELEMETRY_FIELD_CLUB_ID, club_telemetry_writer
from clubs.club_tuning import ClubTunables
from gtcl.club_data import ClubData
from gtcl.enums.club_data_icon import ClubDataIcon
from gtcl.enums.club_interaction import ClubInteraction
from gtcl.enums.club_seed import ClubSeed
from gtcl.modinfo import ModInfo
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.choose_object_dialog import CommonChooseObjectDialog
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.option_dialogs.common_choose_sims_option_dialog import CommonChooseSimsOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.sims.common_dialog_sim_option import CommonDialogSimOption
from sims4communitylib.dialogs.option_dialogs.options.sims.common_dialog_sim_option_context import CommonDialogSimOptionContext
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ui.ui_dialog_picker import ObjectPickerRow
from world.region import get_region_instance_from_zone_id

log: CommonLog = CommonLogRegistry.get().register_log(f"{ModInfo.get_identity().name}", ModInfo.get_identity().name)
log.enable()


class ClubUtils:

    id_2_description = {
        0: 'Invalid',
        1: 'Start Club Gathering',
        2: 'Lead Club',
        3: 'Join Club',
        4: 'Invite Sims',
        5: 'Delete Club',
        6: 'Join Active Gathering',
    }

    def get_addnew_as_option(self, start_value: int = 0) -> ObjectPickerRow:
        option_id = start_value
        cdi = ClubDataIcon()
        icon = sims4.resources.Key(cdi.type, cdi.instance, cdi.group)

        option = ObjectPickerRow(
                option_id=option_id,
                name=CommonLocalizationUtils.create_localized_string(0xFC089996, tokens=(' New ', )),
                row_description=CommonLocalizationUtils.create_localized_string(0xFC089996, tokens=('Create a brand new club',)),
                row_tooltip=None,
                icon=icon,
                tag=f'{option_id}',
            )
        return option

    def get_clubs_as_options(self, start_value: int = 1, exclude_sim_info: Union[None, SimInfo] = None, require_sim_info: Union[None, SimInfo] = None) -> List[ObjectPickerRow]:
        options = []
        option_id = start_value
        club_service = services.get_club_service()
        clubs = club_service.clubs
        for club in clubs:
            club: Club = club
            if exclude_sim_info in club.members:
                continue
            if require_sim_info and require_sim_info not in club.members:
                continue
            name = self._get_club_name(club)
            # club.leader club.description
            options.append(
                ObjectPickerRow(
                    option_id=option_id,
                    name=CommonLocalizationUtils.create_localized_string(0xFC089996, tokens=(name,)),
                    row_description=CommonLocalizationUtils.create_localized_string(0xFC089996, tokens=(f"{club._description}",)),
                    # name=name,
                    # row_description=club.description,
                    row_tooltip=None,
                    icon=club.icon,
                    tag=f'{club.club_id}'
                ),
            )
            option_id += 1
        return options

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

    def show_club_picker_dialog(self, sim_info: SimInfo, interaction_id: ClubInteraction, options: List[ObjectPickerRow]):
        def start_gathering(club_service, club):
            def _start_gathering(zone_id=None):
                start_gathering = functools.partial(club_service.start_gathering, club, invited_sims=(services.active_sim_info(),))
                if zone_id is None:
                    start_gathering()
                else:
                    start_gathering(zone_id=zone_id)

            zone_id = club.get_hangout_zone_id(prefer_current=True)
            if zone_id:
                current_region = services.current_region()
                hangout_region = get_region_instance_from_zone_id(zone_id)
                if not current_region.is_region_compatible(hangout_region):
                    zone_id = 0
                _start_gathering(zone_id=zone_id)
            else:
                _start_gathering()
            return True

        def _on_chosen(choice: str, outcome: CommonChoiceOutcome):
            log.debug(f"choice={choice} outcome={outcome}")
            if (outcome == CommonChoiceOutcome.CHOICE_MADE) and (choice.isdecimal()):
                club_id = int(choice)
                log.debug(f"choice={choice} club_id={club_id}")
                club_service = services.get_club_service()
                club: Club = club_service.get_club_by_id(club_id)
                if interaction_id == ClubInteraction.StartGathering:
                    start_gathering(club_service, club)
                elif interaction_id == ClubInteraction.Lead:
                    club.reassign_leader(sim_info)
                elif interaction_id == ClubInteraction.Join:
                    if club_id == 0:
                        ClubUtils().add_club(leader=sim_info, invite_only=True)
                    else:
                        club.add_member(sim_info)
                elif interaction_id == ClubInteraction.Invite:
                    self.show_sim_picker_dialog(club)
                elif interaction_id == ClubInteraction.Delete:
                    club_service.remove_club(club)
                elif interaction_id == ClubInteraction.JoinActiveGathering:
                    club_gathering = club_service.clubs_to_gatherings_map.get(club)
                    if club_gathering:
                        sim = CommonSimUtils.get_sim_instance(sim_info)
                        if sim:
                            club_gathering.invite_sim_to_job(sim, job=club_gathering.default_job())
                elif interaction_id == ClubInteraction.Points:
                    club.bucks_tracker.try_modify_bucks(BucksType.ClubBucks, 10000)

        title = CommonSimNameUtils.get_full_name(sim_info)
        descrption = ClubUtils.id_2_description.get(interaction_id)
        title_tokens = (CommonLocalizationUtils.create_localized_string(0xFC089996, tokens=(title, )), )
        description_tokens = (CommonLocalizationUtils.create_localized_string(0xFC089996, tokens=(descrption, )), )

        per_page = 25
        if len(options) > per_page:
            r = len(options) % per_page
            if r < 10:
                per_page = int(len(options) / int(len(options) / per_page)) + 1
        dialog = CommonChooseObjectDialog(
            0xFC089996,  # '{0.String}'
            0xFC089996,  # '{0.String}',
            tuple(options),
            title_tokens=title_tokens,
            description_tokens=description_tokens,
            per_page=per_page
        )
        dialog.show(on_chosen=_on_chosen, sort_rows=True)

    def add_club(self, leader: Union[None, int, Sim, SimInfo] = None, members: Union[None, List] = None,
                 name: str = '', description: str = '', invite_only: bool = True,
                 icon: Union[None, ClubDataIcon] = None, club_seed: Union[None, ClubSeed] = None) -> Club:
        club_data = ClubData(leader=leader, members=members, name=name, description=description, invite_only=invite_only, icon=icon)

        sim_info = CommonSimUtils.get_sim_info(club_data.leader)
        club_service = services.get_club_service()
        new_club = club_service.create_club(club_data=club_data)

        club_service.add_club(new_club)
        new_club.show_club_notification(sim_info, ClubTunables.CLUB_NOTIFICATION_CREATE)
        with telemetry_helper.begin_hook(club_telemetry_writer, TELEMETRY_HOOK_CLUB_CREATE) as hook:
            hook.write_int(TELEMETRY_FIELD_CLUB_ID, new_club.id)

        return new_club

    def show_sim_picker_dialog(self, club: Club):
        def _on_submit(sim_info_list: Tuple[SimInfo]):
            for sim_info in sim_info_list:
                club.add_member(sim_info)

        title = 'Invite To'
        descrption = self._get_club_name(club)
        title_tokens = (CommonLocalizationUtils.create_localized_string(0xFC089996, tokens=(title,)),)
        description_tokens = (CommonLocalizationUtils.create_localized_string(0xFC089996, tokens=(descrption,)),)

        # Create the dialog and show a number of Sims in 4 columns and being able to select up to 5 Sims.
        option_dialog = CommonChooseSimsOptionDialog(
            0xFC089996,
            0xFC089996,
            title_tokens=title_tokens,
            description_tokens=description_tokens,
            mod_identity=ModInfo.get_identity()
        )

        for sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator():
            should_select = False  # random.choice((True, False))
            is_enabled = True  # random.choice((True, False))  # TODO disable sims in club
            if sim_info in club.members:
                continue
            option_dialog.add_option(
                CommonDialogSimOption(
                    sim_info,
                    CommonDialogSimOptionContext(
                        is_enabled=is_enabled,
                        is_selected=should_select
                    )
                )
            )

        option_dialog.show(
            sim_info=CommonSimUtils.get_active_sim_info(),
            column_count=4,
            max_selectable=100,
            on_submit=_on_submit
        )
