#!/bin/bash

# A wrapper script for painless discord bots.
# v1.0.0
# Copyright (c) 2019 0x5c
# Released under the terms of the MIT license.
# Part of:
# https://github.com/0x5c/quick-bot-no-pain


# If $BOTENV is not defined, default to 'botenv'
if [[ -z ${BOTENV+x} ]]; then
    BOTENV='botenv'
fi

# Argument handling     # ? TODO: Argument passing ?
if [[ $1 == '--pass-errors' ]]; then 
    _PASS_ERRORS=1
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
            if [[ $_PASS_ERRORS -eq 0 ]]; then    # The bot crashed and:
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
    ./$BOTENV/bin/python3 main.py
    err=$?
    _message="$0: The bot exited with [$err]"
    code_handling
done
