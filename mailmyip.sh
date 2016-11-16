#!/bin/bash

#sleep 120

((count = 1000))                            # Maximum number to try.
while [[ $count -ne 0 ]] ; do
    ping -c 1 8.8.8.8                      # Try once. or put address that is ping-able.
    rc=$?
    if [[ $rc -eq 0 ]] ; then
        ((count = 1))                      # If okay, flag to exit loop.
    fi
    ((count = count - 1))                  # So we don't go forever.
done

if [[ $rc -eq 0 ]] ; then                  # Make final determination.
    echo 'say The internet is back up.'
        ip=$(hostname -I) 
        echo "$ip" | mail -s "New IP of $(hostname)" to@domain.com
else
    echo 'say Timeout.'
fi
