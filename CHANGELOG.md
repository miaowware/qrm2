# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Added
- Flag emojis to commands with countries.
- Image attribution and description to "image" commands.
- New key in options.py: pika.


## [v2.0.0] - 2019-12-16
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


## v1.0.0 - 2019-07-31 [YANKED]


[Unreleased]: https://github.com/classabbyamp/discord-qrm2/compare/v2.0.0...HEAD
[v2.0.0]: https://github.com/classabbyamp/discord-qrm2/releases/tag/v2.0.0
