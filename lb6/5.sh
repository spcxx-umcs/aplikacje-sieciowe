#!/bin/bash

SERVER="smtp.ethereal.email" # uzywam testowego zewnetrznego maila bo interia juz nie dziala
PORT="587"

EMAIL="kenya.vonrueden@ethereal.email"
PASSWORD="YKujV2SpeeN69D5ckM"
RECIPIENT="kenya.vonrueden@ethereal.email"

FILE_NAME="test.png"
FILE_BASE64=$(cat $FILE_NAME | openssl base64)
BOUNDARY="MIME_BOUNDARY_IMAGE"

encode_base64() {
    printf "%s" "$1" | base64
}

send_cmd() {
    printf "%s\n" "$1"
    sleep 0.5
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
send_cmd "From: <$EMAIL>"
send_cmd "To: <$RECIPIENT>"
send_cmd "Subject: Test - zalaczniki"

send_cmd "MIME-Version: 1.0"
send_cmd "Content-Type: multipart/mixed; boundary=\"$BOUNDARY\""
send_cmd ""
send_cmd "--$BOUNDARY"
send_cmd "Content-Type: text/plain; charset=\"utf-8\""
send_cmd "Content-Transfer-Encoding: 7bit"
send_cmd ""
send_cmd "Testowa wiadomosc z obrazkiem w zalaczniku"
send_cmd ""
send_cmd "--$BOUNDARY"
send_cmd "Content-Type: image/png; name=\"$FILE_NAME\""
send_cmd "Content-Disposition: attachment; filename=\"$FILE_NAME\""
send_cmd "Content-Transfer-Encoding: base64"
send_cmd ""
send_cmd "$FILE_BASE64"
send_cmd ""
send_cmd "--$BOUNDARY--"
send_cmd "."

sleep 2
send_cmd "QUIT"
) | openssl s_client -quiet -starttls smtp -crlf -connect $SERVER:$PORT