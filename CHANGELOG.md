# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Added
- Global info, secrets, and options are now stored in their own files, using [0x5c/quick-bot-no-pain](https://github.com/0x5c/quick-bot-no-pain)
- Rich lookup for AE7Q (callsigns only, more to come)
- Rich lookup for QRZ, if a QRZ subscription is present
- Timestamp and requester username and avatar are now shown on embeds
- Current and 3-Day Forecast terrestrial weather conditions lookup commands
### Changed
- Rewrote code to take advantage of discord.py's cogs
- Moved most bot responses into embeds
- Re-implemented shutdown and restart commands using discord.py checks
- Embed colors now fit with discord's theme
- The contest calendar command no longer relies on `selenium`
### Removed
- CTY.DAT parsing is now its own library (`ctyparser` available on pypi)
- Removed Herobrine
### Fixed
- Cleaned up code to comply with the PEP8 Standard
