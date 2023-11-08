#!/bin/bash

if [[ -z $1 ]]
then
echo "No error log file is provided"
exit 1
fi
requip=$(awk '{print $1}' ./$1 | uniq -c | sort -r | head -n 1 )  # print first column from
echo "The most frequent visitor is: $requip"

rpage=$(awk '{print $7}' ./$1 | uniq -c | sort -r | head -n 1) # getting requested page
echo "The most frequently requested page: $rpage"

#number of requests for each IP
rrequests=$(awk '{print $1}' ./$1 | uniq -c | sort -r )
echo "The list is pretty long, do you wish to print it ? [y/n]"
read answer
if [[ $answer == y ]]
then
echo "IP and number of requests from it: $rrequests"
else
  echo "I think it means No. This list will be saved in a Apache_logs.txt file"
  echo "$rrequests" > ./Apache_logs.txt
fi

#print non-existent pages
non=$(awk '/404/{print $7, $9}' ./$1) # check pages with 404 status
echo "Pages which do not exist: $non" > ./missed_pages.txt
echo "Pages which do not exist are located in missed_pages.txt file"

#
pages=$(awk '/"-"/{next}{print $4, $11}' ./$1 | awk -F / '{print $5, $1, $2, $3}' | awk -F : '{print $1, $2}' | sort -r | uniq -c)
echo "Dates and request numbers: $pages" > ./requests.txt
echo "Dates abd request numbers are located in requests.txt file"

#Search bots
bots=$(awk /bot/'{print $14, $16, $1}' ./$1)
echo "Bots that accessed pages: $bots" > ./bots.txt
echo "List of bots is located in bots.txt file"
