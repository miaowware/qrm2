# Development Guide for qrm

**Make sure to also read [`CONTRIBUTING.md`][0], everything in there applies here.**

### Environment Setup

1. [Fork this repo][1] into your own GitHub namespace.
1. Make sure the `master` branch is up to date, then make yourself a new branch with a descriptive name.
1. Once the forked repo is cloned and on the proper branch, you can set up the development environment.
    1. Install python 3.7 or higher.
    1. Run `make dev-install`.
       This should install everything you need to develop and run qrm.
    1. [Create a bot and token][2], and add it to `data/keys.py`.
       Also add your [QRZ credentials][3] if needed.
    1. In `data/options.py`, change values as needed.
       Some commands require adding your Discord user ID to `owner_uids`.
    1. To activate the virtual env that was created by `make`, run `source botenv/bin/activate` (or the equivelent for your shell or operating system).

These instructions are fairly \*NIX-centric, so if you would like to develop on Windows, it is suggested that the Windows Subsystem for Linux be used.

## While You Develop

To run qrm, use the command `./run.sh`.
We recommend you use the `--pass-errors` flag to avoid perpetual restart loops if you break the bot.
It exists because repeatedly mashing [Ctrl+C] at high speed to break a fast loop is not fun.

Make sure to add [type hints][4] to your code.
This is what `mypy` validates in the code.

Using `dev-notes` for documentation is especially important if you introduce a new json file format (like for maps and bandplans) or to document some development process (like the command to crush the various images in the repository).

### Test your changes

In addition to testing functionality, make sure to run `flake8` to ensure your code uses the proper style, and `mypy [files...]` to ensure proper typing.
You can also enable them for this project in your IDE if supported.
This will give you automatic and continuous linting and type checking.

### A Note on Style

qrm tries to keep to PEP 8 style whenever possible.
Use the utility `flake8` to check that you follow this style.
When you start a PR or push commits, GitHub will automatically run this for you,
but we prefer that developers check this before committing and opening PRs.

Otherwise, try to follow the existing style:
- double-quotes except when required to be single,
- indentation of mult-line structures matching other examples in the code,
- etc.

[0]: https://github.com/miaowware/.github/blob/master/CONTRIBUTING.md
[1]: https://github.com/miaowware/qrm2/fork
[2]: https://discordpy.readthedocs.io/en/latest/discord.html
[3]: https://www.qrz.com/page/xml_data.html
[4]: https://docs.python.org/3/library/typing.html