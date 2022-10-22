#  GetTogether Club Limits for TS4
The mod removes various GT club limits.

It will not break with every TS4 update as it is script based. So there will be usually no new release after a TS4 update.

You may copy the contents of this file to https://dillinger.io/ far a better representation if you don't have a MarkDown viewer available.

### Installation
This Mod comes as an archive to be extracted into `The Sims 4`. Only the `o19_gt_club_limits.ts4script` file is needed and it may be placed also elsewhere.

##### Dependencies
This mod relies on S4CL which can be downloaded from https://github.com/ColonolNutty/Sims4CommunityLibrary/releases/latest

As long as S4CL is not already installed in your mods folder I highly recommend to install it into `The Sims 4/Mods/_cn_/`

##### Final directory structure
Some users are new to Mods and need help. Here's the directory structure which works for me:

`The Sims 4/Mods/_cn_/sims4communitylib.ts4script` - The dependency from above

`The Sims 4/Mods/_cn_/sims4communitylib.package`

`The Sims 4/Mods/_o19_/o19_gt_club_limits.ts4script` - This mod itself.


`The Sims 4/mod_description/` - Optional directory with references for you regarding this and other mods.

`The Sims 4/mod_logs/` - Will be created later by S4CL and contain the logs.

`The Sims 4/mod_data/` - Will be created later by GT-Club-Limits and contain the mod settings.

### Updates
New versions of S4CL and GT-Club-Limits should be extracted in the installation directories from above and overwrite the existing files.
A restart of the game is required (if it was running) to load the updated script mods. 
 
### Configuration
After startup the mod writes a new configuration template to `The Sims 4/mod_data/gt_club_limits/clubs.ini.current.ini`. This file can be copied to `clubs.ini` and modified to change the default settings.
There is no PIE menu to change the settings.

##### PIE menu options
PIE menu options to
* Join existing existing or new clubs (*1)
* Delete existing clubs (*1)
* Become the leader of a club
* Invite multiple sims to a club (up to 100 per invitation, use this with care)
* Start a club gathering (While at work one can not join an active gathering.)
* Add 10,000 points to a club

(*1) With the UI not updating properly the active sim itself can not delete its own clubs or join a new one. Click on any other random sim for these interactions.
A new club is always named 'o19'. Switch to the sim who is the owner of the new club to configure it as usual (name, description, rules, ...).

##### Cheat Commands #####
For testing purposes cheats have been added, they affect the active sim.
* `GT_Club_Limits.help` - Print and log the following cheat commands:
* `o19.gtcl.join` - Join existing existing club
* `o19.gtcl.delete` - Delete existing clubs (*1)
* `o19.gtcl.lead` - Become the leader of a club
* `o19.gtcl.invite` - Invite multiple sims to a club
* `o19.gtcl.start` - Start a club gathering
* `o19.gtcl.points` - Add 10,000 points to a club
* `o19.gtcl.print` - Write all club names and leaders to the log file

##### Maximum number of Sims that can be in a single Club.
As soons as Sim is in 3 Clubs it can not create a new Club but it still can join Clubs or other household Sims can add it to a Club.

`MAX_MEMBERS_UNLIMITED:  True` can be set to `MAX_MEMBERS_UNLIMITED:  False` and then the `MAX_CLUB_MEMBERS` can be set. The default removes all limits.

##### Maximum number of Clubs a Sim can be a member of
The number of Clubs can be limited. Depending on the screen resolution and settings about 9 clubs can be displayed without a scroll-bar.

`MAX_CLUBS_UNLIMITED:  True` can be set to `MAX_CLUBS_UNLIMITED:  False` and then the `MAX_CLUBS` can be set. The default removes all limits.

##### Zones for Club gatherings
With `NO_CLUB_ZONE_VALIDATION:  True` all zones should be accepted to start a club gathering. This can be disabled with `NO_CLUB_ZONE_VALIDATION: False`.

##### Club Requirements
With `NO_CLUB_REQUIREMENTS_VALIDATION: True` everyone should be able to join the club. This can be disabled with `NO_CLUB_REQUIREMENTS_VALIDATION: False`. It may allow to add non-humans to clubs.

### Copyright and License
LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode

© 2021 https://github.com/Oops19
