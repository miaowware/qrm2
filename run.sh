#!/bin/sh

# A wrapper script for painless discord bots.
# v1.2.0
# Copyright (c) 2019 0x5c
# Released under the terms of the MIT license.
# Part of:
# https://github.com/0x5c/quick-bot-no-pain


# If $BOTENV is not defined, default to 'botenv'
if [ -z "$BOTENV" ]; then
    BOTENV='botenv'
fi


# Argument handling
_PASS_ERRORS=0
_NO_BOTENV=0
while [ ! -z "$1" ]; do
    case $1 in
        --pass-errors)
            _PASS_ERRORS=1
            ;;
        --no-botenv)
            _NO_BOTENV=1
            ;;
        --)
            shift
            break
            ;;
    esac
    shift
done


# If $PYTHON_BIN is not defined, default to 'python3.9'
if [ $_NO_BOTENV -eq 1 -a -z "$PYTHON_BIN" ]; then
    PYTHON_BIN='python3.9'
fi


# A function called when the bot exits to decide what to do
code_handling() {
    case $err in
        0)
            echo "$_message: exiting"
            exit 0      # The bot whishes to stay alone.
            ;;
        42)
            echo "$_message: restarting"
            return      # The bot whishes to be restarted (returns to the loop).
            ;;
        *)
            if [ $_PASS_ERRORS -eq 0 ]; then    # The bot crashed and:
                echo "$_message: restarting"
                return      # ...we should return to the loop to restart it.
            else
                echo "$_message: exiting (--pass-errors)"
                exit $err   # ...we should just exit and pass the code to our parent (probably a daemon/service manager).
            fi
            ;;
    esac
}


echo "$0: Starting bot..."

# The loop
while true; do
    if [ $_NO_BOTENV -eq 1 ]; then
        "$PYTHON_BIN" main.py $@
    else
        ./$BOTENV/bin/python3 main.py $@
    fi
    err=$?
    _message="$0: The bot exited with [$err]"
    code_handling
done
