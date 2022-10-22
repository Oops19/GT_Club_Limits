#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2022 https://github.com/Oops19
#


from typing import Union, List, Any

from clubs.club_enums import ClubHangoutSetting, ClubOutfitSetting

from sims.sim import Sim
from sims.sim_info import SimInfo
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils

from gtcl.enums.club_data_icon import ClubDataIcon


class ClubSeed:
    def __init__(self, leader: Union[None, int, Sim, SimInfo] = None, members: Union[None, List] = None,
                 instance: int = 0, associated_color: int = 0, associated_style: int = 0, invite_only: bool = True,
                 icon: ClubDataIcon = None, club_rules: Union[None, List] = None):

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
        # seed_members=(self.leader, self.members)

        self.instance = instance
        self.membership_criteria = []

        self.associated_color = associated_color
        self.associated_style = associated_style
        self.uniform_male_child = None
        self.uniform_female_child = None
        self.uniform_male_adult = None
        self.uniform_female_adult = None
        self.bucks_tracker_data = None
        self.male_adult_mannequin = None
        self.male_child_mannequin = None
        self.female_adult_mannequin = None
        self.female_child_mannequin = None

        self.invite_only = invite_only
        if icon:
            self.icon = icon
        else:
            self.icon = ClubDataIcon()
        if club_rules:
            self.club_rules = club_rules
        else:
            self.club_rules = []
        self.hangout = ClubHangout()

        self.club_outfit_setting = ClubOutfitSetting.NO_OUTFIT


class ClubHangout:

    hangout_setting: ClubHangoutSetting = ClubHangoutSetting.HANGOUT_NONE
    hangout_venue: Any = None
    hangout_zone_id: int = 0

    def __init__(self, hangout_setting: ClubHangoutSetting = ClubHangoutSetting.HANGOUT_NONE, hangout_venue: Any = None, hangout_zone_id: int = 0):
        ClubHangout.hangout_setting = hangout_setting
        ClubHangout.hangout_venue = hangout_venue
        ClubHangout.hangout_zone_id = hangout_zone_id

    @staticmethod
    def get_hangout_data():
        return ClubHangout.hangout_setting, ClubHangout.hangout_venue, ClubHangout.hangout_zone_id
