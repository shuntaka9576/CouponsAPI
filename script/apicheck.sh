#!/bin/bash

API_ENDPOINT=$(aws cloudformation describe-stacks --stack-name dev-cpa-couponsApiStack --query 'Stacks[].Outputs[0].OutputValue' | perl -ne 'print $1 if(/"(.*?)"/)')
COLOR_ON="\033[0;36m"
COLOR_OFF="\033[0;39m"

echo '=*=*=*=*=*=*=*=*=*=*=*=*=*=*=* API_ENDPOINT =*=*=*=*=*=*=*=*=*=*=*=*=*=*=*'
echo "$API_ENDPOINT"
echo '=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*'
echo

echo -e "${COLOR_ON}GET /coupons${COLOR_OFF}"
set -x; curl -L "$API_ENDPOINT"; echo; set +x;

echo -e "${COLOR_ON}POST /coupons${COLOR_OFF}"
set -x; curl -X POST -H "Content-Type: application/json" "$API_ENDPOINT"; echo; set +x;

echo -e "${COLOR_ON}GET /coupons?startdate=yyyymmdd&enddate=yyyymmdd${COLOR_OFF}"
set -x; curl -L "$API_ENDPOINT"'?startdate=20180401&enddate=20180501'; echo; set +x;

echo -e "${COLOR_ON}POST /coupons?startdate=yyyymmdd&enddate=yyyymmdd${COLOR_OFF}"
set -x; curl -X POST -H "Content-Type: application/json" -d '{"startdate":"20180401","enddate":"20180501"}' "$API_ENDPOINT"; echo; set +x;

echo -e "${COLOR_ON}GET /coupons/0001245${COLOR_OFF}"
set -x; curl -L "$API_ENDPOINT"'/0001245'; echo; set +x;
