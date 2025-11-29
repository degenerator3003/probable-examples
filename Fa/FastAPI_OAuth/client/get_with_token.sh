#!/bin/bash

TOKEN_FILE="token.txt"
# Read token back from file
TOKEN_FROM_FILE=$(cat "$TOKEN_FILE")

curl -X GET "http://localhost:8000/secure" \
     -H "Authorization: Bearer $TOKEN_FROM_FILE"

