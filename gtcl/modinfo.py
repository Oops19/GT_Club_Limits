from sims4communitylib.mod_support.common_mod_info import CommonModInfo


class ModInfo(CommonModInfo):
    """ Mod info for the S4CL Sample Mod. """
    # To create a Mod Identity for this mod, simply do ModInfo.get_identity(). Please refrain from using the ModInfo of The Sims 4 Community Library in your own mod and instead use yours!
    _FILE_PATH: str = str(__file__)

    @property
    def _name(self) -> str:
        # This is the name that'll be used whenever a Messages.txt or Exceptions.txt file is created <_name>_Messages.txt and <_name>_Exceptions.txt.
        return 'GT_Club_Limits'

    @property
    def _author(self) -> str:
        # This is your name.
        return 'o19'

    @property
    def _base_namespace(self) -> str:
        # This is the name of the root package
        return 'gtcl'

    @property
    def _file_path(self) -> str:
        # This is simply a file path that you do not need to change.
        return ModInfo._FILE_PATH

    @property
    def _version(self) -> str:
        return '1.0.8.2'


"""
1.1
    Remove _TS4/Mods/gtcl.ts4script (empty file to replace old name)
    Remove _TS4/Mods/gt_club_limits.ts4script (empty file to replace old name)
1.0.8.2
    Add 'Clubs'>'Points'
    'o19.gtcl.print' logs more information
    Add to doc: 'o19.gtcl.' + 'start', 'lead',  'join',  'invite',  'delete', 'print' 
1.0.8.1
    Fixed notification - X not Y has created club.
1.0.8
    Rename folders to 'gtcl' (from 'gt_club_limits')
1.0.7
    New 'Clubs'>'Start gathering' etc. interactions
1.0.6 Fixed a few typos and PEP warnings.
1.0.4 Fixed GTW strings.
1.0.2 TS4 folders are now detected differently.
"""