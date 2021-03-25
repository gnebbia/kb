#!/bin/bash

function gen_options()
{
    kb list -f
}
gen_options


TERMINAL="alacritty"

choice="$@"

if [[ -n "$choice" ]]
then
    title=$(basename "$choice")
    category=$(dirname "$choice")
    coproc ("$TERMINAL" -e kb edit -t "$title" -c "$category" > /dev/null 2>&1 )
fi
