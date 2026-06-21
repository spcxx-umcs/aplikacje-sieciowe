#!/bin/bash

SERVER="smtp.ethereal.email" # uzywam testowego zewnetrznego maila bo interia juz nie dziala
PORT="587"

EMAIL="kenya.vonrueden@ethereal.email"
SPOOFED_SENDER="rektor@umcs.pl"
PASSWORD="YKujV2SpeeN69D5ckM"
RECIPIENT="kenya.vonrueden@ethereal.email"

encode_base64() {
    printf "%s" "$1" | base64
}

send_cmd() {
    printf "%s\n" "$1"
    sleep 1
}

(
sleep 2

send_cmd "EHLO szymonrozga"
send_cmd "AUTH LOGIN"

send_cmd "$(encode_base64 "$EMAIL")"
send_cmd "$(encode_base64 "$PASSWORD")"

send_cmd "MAIL FROM: <$EMAIL>"
send_cmd "RCPT TO: <$RECIPIENT>"

send_cmd "DATA"
send_cmd "From: <$SPOOFED_SENDER>"
send_cmd "To: <$RECIPIENT>"
send_cmd "Subject: Test spoofing"
send_cmd ""
send_cmd "Testowa wiadomosc"
send_cmd "."

sleep 2
send_cmd "QUIT"
) | openssl s_client -quiet -starttls smtp -crlf -connect $SERVER:$PORT