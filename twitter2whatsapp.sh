#!/bin/bash

#cd /home/ahmadt/WhatsTwitter

python sent-tweets.py cnnbrk 966560000000
python sent-tweets.py BreakingNews 966560000000
python sent-tweets.py BreakingF24_ar 966560000000

echo Done
exit 0
