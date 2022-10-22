#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2022 https://github.com/Oops19
#


from typing import Union, List

from sims.sim import Sim
from sims.sim_info import SimInfo
from id_generator import generate_object_id
from clubs.club_enums import ClubOutfitSetting, ClubHangoutSetting

from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils

from gtcl.enums.club_data_icon import ClubDataIcon
from gtcl.enums.club_seed import ClubSeed


class ClubData:
    def __init__(self, leader: Union[None, int, Sim, SimInfo] = None, members: Union[None, List] = None,
                 name: str = '', description: str = '', invite_only: bool = False,
                 icon: Union[None, ClubDataIcon] = None, club_seed: Union[None, ClubSeed] = None):
        if not leader:
            leader = CommonSimUtils.get_active_sim_id()
        else:
            leader = CommonSimUtils.get_sim_id(leader)
        _members = []
        if members:
            for member in members:
                _members.append(CommonSimUtils.get_sim_id(member))
        self.leader = leader  # SimId
        _members.append(leader)
        self.members = _members  # List[SimId]

        if not name:
            name = 'o19'
        self.name = name
        if not description:
            description = "Created by 'Get Together: Club Limits'"
        self.description = description
        self.invite_only = invite_only

        if icon:
            self.icon = icon
        else:
            self.icon = ClubDataIcon()
        if club_seed:
            self.club_seed = club_seed
        else:
            self.club_id = generate_object_id()  # None  # generate_object_id()
            self.club_seed = ClubSeed(instance=self.club_id)

        self.club_id = generate_object_id()  # None  # generate_object_id()
        self.club_rules = []
        self.rules = []  # None
        self.member_ids = None
        self.recent_members = []
        self.recent_member_ids = None
        self.membership_criteria = []  # None

        self.hangout_setting = ClubHangoutSetting.HANGOUT_NONE
        self.hangout_venue = None
        self.hangout_zone_id = 0
        self.venue_type = None
        self.associated_color = 0  # None
        self.associated_style = 0  # None
        self.uniform_male_child = None
        self.uniform_female_child = None
        self.uniform_male_adult = None
        self.uniform_female_adult = None
        self.bucks_tracker_data = None
        self.male_adult_mannequin = None
        self.male_child_mannequin = None
        self.female_adult_mannequin = None
        self.female_child_mannequin = None
        self.outfit_setting = ClubOutfitSetting.NO_OUTFIT
