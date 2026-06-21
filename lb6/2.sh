#!/bin/bash

SERVER="smtp.ethereal.email" # uzywam testowego zewnetrznego maila bo interia juz nie dziala
PORT="587"

EMAIL="kyleigh.wilkinson@ethereal.email"
PASSWORD="qddxqMHPMebfdSTDPh"
RECIPIENT1="kyleigh.wilkinson@ethereal.email"
RECIPIENT2="kenya.vonrueden@ethereal.email"

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
send_cmd "RCPT TO: <$RECIPIENT1>"
send_cmd "RCPT TO: <$RECIPIENT2>"

send_cmd "DATA"
send_cmd "From: <$EMAIL>"
send_cmd "To: <$RECIPIENT1>, <$RECIPIENT2>"
send_cmd "Subject: Test - zadanie 2"
send_cmd ""
send_cmd "Testowa wiadomosc dla wielu odbiorcow"
send_cmd "."

sleep 2
send_cmd "QUIT"
) | openssl s_client -quiet -starttls smtp -crlf -connect $SERVER:$PORT