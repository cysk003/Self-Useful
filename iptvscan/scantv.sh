#!/bin/bash

baseurl=$1
s=`echo $baseurl|grep -o  '\[.*\]'|sed -e 's/\[//g' -e 's/\]//g'|awk -F"-" 
'{print $1}'`
e=`echo $baseurl|grep -o  '\[.*\]'|sed -e 's/\[//g' -e 's/\]//g'|awk -F"-" 
'{print $2}'`


for n in $(seq -w $s $e)
do
  h=""
  w=""
  url=`echo $baseurl|sed "s/\[.*\]/$n/g"`
  res=`ffprobe -user_agent "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac 
OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 
Safari/537.36" -timeout 5000  -select_streams v -show_streams -v quiet -of 
csv="p=0" -of json -i $url`
  [ $(echo $res|grep -c height) -gt 0 ] && h=`echo $res|jq 
.streams[].height`
  [ $(echo $res|grep -c height) -gt 0 ] && w=`echo $res|jq 
.streams[].width`
  [ $(echo $res|grep -c height) -gt 0 ] && rate=`echo $res|jq 
.streams[].avg_frame_rate|sed -e 's/"//g' -e 's/\/1//g'`
  [ "0$h" != "0" ] && [ "0$w" != "0" ] && echo "$n[${w}X${h}],$url"
done
