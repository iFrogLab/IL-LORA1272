#!/bin/bash
service apache2 restart
service mysql restart
cd /ifroglab/IL-LORA1272/LoRa-Gateway/Gateway
python ap-01-lora-gateway-2-read-httpGet.py.py 

