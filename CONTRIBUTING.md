# Contributing to qrm

## Before You Start

- Make sure there's an issue for the feature, bugfix, or other improvement you want to make.
- Make sure it's something that the project maintainers want.
  We can discuss it and assign the issue to you.
- Make sure work isn't already being done on the issue.

### Environment Setup

Once all of the above is done, you can get started by setting up your development envronment.

1. [Fork this repo][1] into your own GitHub namespace.
1. Make sure the `master` branch is up to date, then make yourself a new branch with a descriptive name.
1. Once the forked repo is cloned and on the proper branch, you can set up the development environment.
    1. Run `make dev-install`.
       This should install everything you need to develop and run qrm.
    1. [Create a bot and token][2], and add it to `data/keys.py`.
       Also add your [QRZ credentials][3] if needed.
    1. In `data/options.py`, change values as needed.
       Some commands require adding your Discord user ID to `owner_uids`.
    1. To activate the virtual env that was created by `make`, run `source botenv/bin/activate` (or the equivelent for your shell or operating system).

## While You Develop

To run qrm, use the command `sh run.sh`.
If you want to break when an error happens, use the flag `--pass-errors`.

Make commits as needed, but try to keep it reasonable.
If there are too many, your contribution may be squashed when merged.
Commit messages should be descriptive and mention issues that they fix ("fixes #123") or contain progress on ("progress on #123").

Make sure to document your code as you go, in both comments and external documentation (in `/dev-notes/`) as needed.

**Test your changes.**
If your code doesn't work, it's not ready for merging.
Make sure you not only test intended behaviour, but also edge cases and error cases.

If you're making a user-facing change, put a quick summary in `CHANGELOG.md` under the `[Unreleased]` heading.
Follow the [Keep a Changelog][4] format.

### A Note on Style

qrm tries to keep to PEP 8 style whenever possible.
Use the utility `flake8` to check that you follow this style.
When you start a PR or push commits, GitHub will automatically run this for you;
if that fails, you will be expected to fix those errors before merge.

Otherwise, try to follow the existing style:
double-quotes except when required to be single,
indentation of mult-line structures matching other examples in the code,
etc.

## When You're Ready to Merge

1. When you have finished working on your contribution, create a pull request from your fork's branch into the main master branch.
1. Read through and complete the pull request template.
   If the checklist is not complete, your contribution will not be merged.
1. Your pull request will get reviewed by at least one maintainer.
1. If approved, another maintainer will merge the pull request.

[1]: https://github.com/miaowware/qrm2/fork
[2]: https://discordpy.readthedocs.io/en/latest/discord.html
[3]: https://www.qrz.com/page/xml_data.html
[4]: https://keepachangelog.com/en/1.0.0/
