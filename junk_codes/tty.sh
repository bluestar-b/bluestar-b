#!/bin/bash

MYTTY=$(tty)
echo "The current terminal is: $MYTTY"

if [ "$(tty)" = "/dev/tty1" ]; then
    echo "You are using the first virtual console."
else
    echo "You are not using the first virtual console."
fi
