#!/bin/bash

SERVER="pop3.ethereal.email"
PORT="995"   

EMAIL="kenya.vonrueden@ethereal.email"
PASSWORD="YKujV2SpeeN69D5ckM"

send_cmd() {
    printf "%s\n" "$1"
    sleep 1
}

(
sleep 2

send_cmd "USER $EMAIL"
send_cmd "PASS $PASSWORD"

send_cmd "STAT" # 2 wynik

sleep 2
send_cmd "QUIT"
) | openssl s_client -quiet -crlf -connect $SERVER:$PORT
# uzywam openssl, ethereal i wiekszosc serwerwo odrzuca nieszyfrowany telnet