#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2022 https://github.com/Oops19
#


from typing import Any

from sims.sim import Sim
from sims4.tuning.tunable import Tunable
from event_testing.results import TestResult
from interactions.context import InteractionContext

# interaction that will run immediately without waiting for the Sim to do something
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils

from gtcl.club_utils import ClubUtils
from gtcl.enums.club_interaction import ClubInteraction
from gtcl.modinfo import ModInfo


log: CommonLog = CommonLogRegistry.get().register_log(f"{ModInfo.get_identity().name}", ModInfo.get_identity().name)
log.enable()
 

class InteractionsClub(CommonImmediateSuperInteraction):
    INSTANCE_TUNABLES = {
        'id': Tunable(tunable_type=int, default=0),
    }

    __slots__ = {'id', }

    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        # log.debug(f"InteractionsClub: on_test({interaction_sim}, {interaction_target}, {interaction_context})")
        return TestResult.TRUE

    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        log.debug(f"InteractionsClub.on_started({self.id}, {interaction_sim}, {interaction_target})")
        try:
            interaction_id = int(self.id)
            sim_info = CommonSimUtils.get_sim_info(interaction_target)  # Dangerous - the active sim should never create a club.
            cu = ClubUtils()

            options = cu.get_clubs_as_options()
            if interaction_id == ClubInteraction.Delete:
                if sim_info == CommonSimUtils.get_active_sim_info():
                    options = cu.get_clubs_as_options(exclude_sim_info=sim_info)
            elif interaction_id == ClubInteraction.Join:
                options = cu.get_clubs_as_options(exclude_sim_info=sim_info)
                if sim_info != CommonSimUtils.get_active_sim_info():
                    options.append(cu.get_addnew_as_option())  # No 'New' for active sim
            elif interaction_id == ClubInteraction.Lead:
                options = cu.get_clubs_as_options(require_sim_info=sim_info)

            log.debug(f"InteractionsClub.on_started({sim_info} {interaction_id} {len(options)})")
            cu.show_club_picker_dialog(sim_info, interaction_id, options)
        except Exception as e:
            log.error(f"{e}", throw=True)
        return CommonExecutionResult.TRUE
