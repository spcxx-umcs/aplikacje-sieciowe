#!/bin/bash

SERVER="pop3.ethereal.email"
PORT="995"   

EMAIL="krystina1@ethereal.email"
PASSWORD="hK5DCNzngvztC75eMf"

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

MIN_ID=""
MIN_SIZE=999999999

while read -r ID ROZMIAR; do
    if [[ "$ID" =~ ^[0-9]+$ ]] && [[ "$ROZMIAR" =~ ^[0-9]+$ ]]; then
        if (( ROZMIAR < MIN_SIZE )); then
            MIN_SIZE=$ROZMIAR   
            MIN_ID=$ID          
        fi
        
    fi
done <<< "$(echo "$LIST_OUTPUT" | tr -d '\r')"

(
sleep 1
echo "USER $EMAIL"
sleep 1
echo "PASS $PASSWORD"
sleep 1
echo "DELE $MIN_ID" 
sleep 2
echo "QUIT"         
sleep 1
) | openssl s_client -quiet -crlf -connect $SERVER:$PORT 2>/dev/null