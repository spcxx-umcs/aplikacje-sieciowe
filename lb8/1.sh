#!/bin/bash

SERVER="imap.ethereal.email"
PORT="993"   

EMAIL="krystina1@ethereal.email"
PASSWORD="hK5DCNzngvztC75eMf"

send_cmd() {
    printf "%s\n" "$1"
    sleep 1
}

(
sleep 2

send_cmd "A1 LOGIN $EMAIL $PASSWORD"
send_cmd "A2 LIST \"\" *"
send_cmd "A3 SELECT INBOX"
send_cmd "A4 FETCH 1 BODY[TEXT]"
send_cmd "A5 STORE 1 +FLAGS (\Seen)"
send_cmd "A6 LOGOUT"

) | openssl s_client -quiet -crlf -connect $SERVER:$PORT
# uzywam openssl, ethereal i wiekszosc serwerow odrzuca nieszyfrowany telnet