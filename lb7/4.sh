#!/bin/bash

SERVER="pop3.ethereal.email"
PORT="995"   

EMAIL="krystina1@ethereal.email"
PASSWORD="hK5DCNzngvztC75eMf"

send_cmd() {
    printf "%s\n" "$1"
    sleep 1
}

LIST_OUTPUT=$(
(
sleep 1
echo "USER $EMAIL"
sleep 1
echo "PASS $PASSWORD"
sleep 1
echo "LIST"
sleep 2
echo "QUIT"
sleep 1
) | openssl s_client -quiet -crlf -connect $SERVER:$PORT 2>/dev/null
)

MAX_ID=""
MAX_SIZE=0

while read -r ID ROZMIAR; do
    if [[ "$ID" =~ ^[0-9]+$ ]] && [[ "$ROZMIAR" =~ ^[0-9]+$ ]]; then
        if (( ROZMIAR > MAX_SIZE )); then
            MAX_SIZE=$ROZMIAR  
            MAX_ID=$ID        
        fi
        
    fi
done <<< "$(echo "$LIST_OUTPUT" | tr -d '\r')"

(
sleep 1
echo "USER $EMAIL"
sleep 1
echo "PASS $PASSWORD"
sleep 1
echo "RETR $MAX_ID"
sleep 2
echo "QUIT"
sleep 1
) | openssl s_client -quiet -crlf -connect $SERVER:$PORT 2>/dev/null