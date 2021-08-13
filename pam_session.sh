#!/bin/sh

N_LOGIN=`who | sort --key=1,1 --unique | wc --lines`
if [ "$PAM_TYPE" = "close_session" ]; then
        if [ $N_LOGIN = 0 ]; then
                /var/bin/kasa-controller/device off
        fi
fi