# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).


## [Unreleased]
### Removed
- `?ae7q` command (#448).


## [2.7.6] - 2022-06-13
### Fixed
- Issue where `?muf` and `?fof2` would fail with an aiohttp error.


## [2.7.5] - 2022-06-08
### Changed
- Bumped ctyparser to 2.2.1.


## [2.7.4] - 2021-10-07
### Added
- a new way to support qrm's development.
### Changed
- Changed the licence to LiLiQ-Rplus-1.1.
- Moved official Docker image to Void Linux.
- Bumped discord.py to 1.7.3.
### Fixed
- Issue where the help command errored.


## [2.7.3] - 2021-04-12
### Fixed
- Issue where `?help` might not display all commands.


## [2.7.2] - 2021-04-12
### Fixed
- Issue where `?help` might not work for all people.


## [2.7.1] - 2021-04-12
### Added
- Helpful LaTeX hints for rendering errors in `?tex`.
### Fixed
- Bug where `?call` would crash if the found profile only had empty address fields.


## [2.7.0] - 2021-04-03
### Added
- `?tex` command to render a LaTeX expression.
- Configuration option to use another rTeX instance for `?tex`.
- `?miltime` command to show the current time in all 25 military timezones.
### Changed
- Main name and aliases of `?bandplan`.
- Recategorized the commands.
### Fixed
- Lack of input sanitisation in `?xkcd`.
- Incorrect capitalisation of the categories in the `?help` command.


## [2.6.0] - 2021-03-18
### Added
- MUF and foF2 maps from [prop.kc2g.com](https://prop.kc2g.com/).
- Commands to show METAR (`?metar`) and TAF (`?taf`) (aeronautical weather conditions).
- The ability to select an element of a pool in `?hamstudy`.
- The ability to answer ❓ to a HamStudy question to get the answer.
- The list of available prefixes to `?help` when there is more than one.
- `?donate` command to show ways to support qrm's development.
- `?invite` command to invite qrm to your server.
- Configuration options to disable showing the `?invite` and set default invite permissions (enabled by default).
- Configuration option to show QRZ nickname in place of first name (enabled by default).
### Changed
- New colour theme for `?greyline`.
- Moved great circle distance and bearing calculation from `?ungrid` to `?griddistance`.
- `?ungrid` to `?latlong`.
- Renamed `?cond` to `?solar`.
- Reduced `?hamstudy` timeout to 5 minutes.
- Library used for QRZ lookups.
- Python>=3.9 now required.
- Most resources are now stored on a website. New indexes are pulled at start and the images linked instead of uploaded.
### Fixed
- Weird image caching situation for `?greyline` on Discord's side.
- The help command was not using the prefix it was invoked with.
### Deprecated
- `?ungrid`.
- Deprecated old `?solar` aliases (`?cond`, etc).
- Deprecated old `?call` alias (`?qrz`).


## [2.5.1] - 2020-12-10
### Fixed
- The result of `?greyline` was cached by discord and would get out of date.
- Broken reaction functionality in `?hamstudy`.


## [2.5.0] - 2020-10-31
### Added
- Italian (`it_hf`, `it_vhf`, `it_shf`), Japanese (`jp`) and Australian (`au`) band charts.
### Fixed
- Details to the Netherlands bandplan command to accurately represent VERNON (Netherlands ARRL equivalent organisation).
- eQSL, paper QSL, and Logbook of the World status in `?qrz` sometimes being shown incorrectly.
- Fixed network error in `?greyline`.


## [2.4.1] - 2020-10-06
### Changed
- Bumped discord.py to 1.5.0


## [2.4.0] - 2020-09-27
### Added
- Canadian prefix info to the `?prefixes` command.
- `?worksplit` command.
- Maps for CQ Zones, ITU Zones, ITU Regions, and Canadian prefixes.
- Attribution for all maps.
- Option to append ` | ?help` to the playing status.
- `?dbconv` command to convert voltage, power, and antenna gain values.
### Changed
- ARRL/RAC section maps to include all current ARRL/RAC sections.
### Fixed
- Issue where multiple prefixes were not handled properly.


## [2.3.2] - 2020-07-22
### Fixed
- Dependency issues


## [2.3.1] - 2020-04-02
### Fixed
- Wordlist containing inappropriate words.


## [2.3.0] - 2020-03-30
### Added
- `?phoneticweight` command, which calculates a message's length in syllables.
- `?standards` command to display [xkcd 927](https://xkcd.com/927/).
### Changed
- Python>=3.7 now required.


## [2.2.3] - 2020-03-29
### Fixed
- Commands are no longer case-sensitive.


## [2.2.2] - 2020-02-25
### Fixed
- Fixed issue where HamStudy questions with images would cause an error.
- Added/fixed/removed typing indicators in numerous commands.


## [2.2.1] - 2020-02-20
### Fixed
- Fixed issue where some HamStudy pools will become unselectable.


## [2.2.0] - 2020-02-15
### Added
- Added Trustee field to qrz command for club callsigns.
- Added alias for `ae7q call` command (`ae7q c`).
- Added ae7q lookup by FRN and Licensee ID, and for trustee records (`ae7q frn, licensee, trustee`).
### Changed
- Changelog command to accept a version as argument.
- The qrz command can now link to a QRZ page instead of embedding the data with the `--link` flag.
- All currently-available pools can now be accessed by the `hamstudy` command.
- The `hamstudy` command now uses the syntax `?hamstudy <country> <pool>`.
- Replaced `hamstudyanswer` command with answering by reaction.
- Removed all generic error handling from commands.
- Cleaned up the description of multiple commands.
- Updated repository links from classabbyamp/discord-qrm2 to miaowware/qrm2.
### Fixed
- Fixed ditto marks (") appearing in the ae7q call command.
- Fixed issue where incorrect table was parsed in ae7q call command.
- Fixed warning emoji reaction on messages starting with "??".
- Fixed issue where `prefixes` would error when given an invalid argument.


## [2.1.0] - 2020-01-04
### Added
- New NATO "phonetics" command.
- Flag emojis to commands with countries.
- Image attribution and description to "image" commands.
- Better user-facing command error handling.
- Reacts with emojis upon specific keywords.
- Official server to info command.
- Command linking to the issue tracker.
- New key in options.py: pika.
### Changed
- The "phonetics" command is now called "funetics".
- All commands now respond in embeds.
- Playing status can now change on a schedule or randomly from a list.
### Fixed
- Fixed incorrect information in the `prefixes` command.


## [2.0.0] - 2019-12-16
### Added
- Rich lookup for AE7Q.com (callsigns only, more to come)
- Rich lookup for QRZ.com, if a QRZ subscription is present
- Current and 3-Day forecast for terrestrial weather conditions lookup commands
- Changelog command
- Command to show callsign rules
- Extension control commands
- Timestamp and requester username and avatar are now shown on embeds
- Docker support, including an [official docker image](https://hub.docker.com/r/classabbyamp/discord-qrm2) and instructions for running the bot in docker
- Global info, secrets, and options are now stored in their own files, based on [0x5c/quick-bot-no-pain](https://github.com/0x5c/quick-bot-no-pain)
### Changed
- Improved the help command, taking advantage of discord.py's new features
- Improved command and argument names to be more clear
- Embed colors now fit with discord's theme
- Re-implemented shutdown and restart commands using discord.py checks
- The contest calendar command no longer relies on `selenium` (more improvements to come)
- Rewrote code to take advantage of discord.py's cogs and extensions
- Moved most bot responses into embeds
### Removed
- CTY.DAT parsing is now its own library ([`ctyparser` available on pypi](https://pypi.org/project/ctyparser/))
- Removed Herobrine
### Fixed
- Cleaned up code to comply with the PEP8 Standard
- Issue in morse and unmorse commands where spaces were not interpreted correctly


## 1.0.0 - 2019-07-31 [YANKED]


[Unreleased]: https://github.com/miaowware/qrm2/compare/v2.7.6...HEAD
[2.7.6]: https://github.com/miaowware/qrm2/releases/tag/v2.7.6
[2.7.5]: https://github.com/miaowware/qrm2/releases/tag/v2.7.5
[2.7.4]: https://github.com/miaowware/qrm2/releases/tag/v2.7.4
[2.7.3]: https://github.com/miaowware/qrm2/releases/tag/v2.7.3
[2.7.2]: https://github.com/miaowware/qrm2/releases/tag/v2.7.2
[2.7.1]: https://github.com/miaowware/qrm2/releases/tag/v2.7.1
[2.7.0]: https://github.com/miaowware/qrm2/releases/tag/v2.7.0
[2.6.0]: https://github.com/miaowware/qrm2/releases/tag/v2.6.0
[2.5.1]: https://github.com/miaowware/qrm2/releases/tag/v2.5.1
[2.5.0]: https://github.com/miaowware/qrm2/releases/tag/v2.5.0
[2.4.1]: https://github.com/miaowware/qrm2/releases/tag/v2.4.1
[2.4.0]: https://github.com/miaowware/qrm2/releases/tag/v2.4.0
[2.3.2]: https://github.com/miaowware/qrm2/releases/tag/v2.3.2
[2.3.1]: https://github.com/miaowware/qrm2/releases/tag/v2.3.1
[2.3.0]: https://github.com/miaowware/qrm2/releases/tag/v2.3.0
[2.2.3]: https://github.com/miaowware/qrm2/releases/tag/v2.2.3
[2.2.2]: https://github.com/miaowware/qrm2/releases/tag/v2.2.2
[2.2.1]: https://github.com/miaowware/qrm2/releases/tag/v2.2.1
[2.2.0]: https://github.com/miaowware/qrm2/releases/tag/v2.2.0
[2.1.0]: https://github.com/miaowware/qrm2/releases/tag/v2.1.0
[2.0.0]: https://github.com/miaowware/qrm2/releases/tag/v2.0.0
