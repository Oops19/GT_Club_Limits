#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2022 https://github.com/Oops19
#


from typing import Tuple
from objects.script_object import ScriptObject

from sims4communitylib.services.interactions.interaction_registration_service import CommonInteractionRegistry, CommonInteractionType, CommonScriptObjectInteractionHandler
from sims4communitylib.utils.common_type_utils import CommonTypeUtils


@CommonInteractionRegistry.register_interaction_handler(CommonInteractionType.ON_SCRIPT_OBJECT_LOAD)
class _RegisterInteractionsClub_GT_Club_Limits_0(CommonScriptObjectInteractionHandler):
    @property
    def interactions_to_add(self) -> Tuple[int]:
        interactions: Tuple = (
            0x286151C0794E5328,  # 'Start Gathering' - fnv('o19_GT_Club_Limits_121407_PMA_Start_Gathering')  # 0x98A651C8
            0x0687F2104CE8E3AC,  # 'Lead' - fnv('o19_GT_Club_Limits_121407_PMA_Lead')
            0x18A03C105760B7FE,  # 'Join' - fnv('o19_GT_Club_Limits_121407_PMA_Join')
            0x036461C39848B135,  # 'Invite' - fnv('o19_GT_Club_Limits_121407_PMA_Invite')
            0xF0BEA8F5FDF6A1E3,  # 'Delete' - fnv('o19_GT_Club_Limits_121407_PMA_Delete')
            0x4E5533392999BD73,  # 'Points' - fnv('o19_GT_Club_Limits_121407_PMA_Points')
        )
        return interactions

    def should_add(self, script_object: ScriptObject, *args, **kwargs) -> bool:
        if not CommonTypeUtils.is_sim_instance(script_object):
            return False  # If the object is not a Sim, return False.
        return True
