#!/bin/bash

API_ENDPOINT=`aws cloudformation describe-stacks --stack-name dev-cpa-couponsApiStack --query 'Stacks[].Outputs[].OutputValue' | perl -ne 'print $1 if(/"(.*?)"/)'`

echo '=*=*=*=*=*=*=*=*=*=*=*=*=*=*=* API_ENDPOINT =*=*=*=*=*=*=*=*=*=*=*=*=*=*=*'
echo $API_ENDPOINT
echo '=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*'
echo

echo 'GET /coupons =>' curl -L $API_ENDPOINT;
curl -L $API_ENDPOINT; echo -e '\n'

echo 'POST /coupons =>' curl -X POST -H "Content-Type: application/json" $API_ENDPOINT
curl -X POST -H "Content-Type: application/json" $API_ENDPOINT; echo -e '\n'

echo 'GET /coupons?startdate=yyyymmdd&enddate=yyyymmdd =>' curl -L $API_ENDPOINT'?startdate=20180401&enddate=20180501'
curl -L $API_ENDPOINT'?startdate=20180401&enddate=20180501'; echo -e '\n'

echo 'POST /coupons?startdate=yyyymmdd&enddate=yyyymmdd =>' curl -X POST -H "Content-Type: application/json" -d '{"startdate":"20180401","enddate":"20180501"}' $API_ENDPOINT
curl -X POST -H "Content-Type: application/json" -d '{"startdate":"20180401","enddate":"20180501"}' $API_ENDPOINT; echo -e '\n'

echo 'GET /coupons/0001245 =>' curl -L $API_ENDPOINT'/0001245'
curl -L $API_ENDPOINT'/0001245'; echo -e '\n'
