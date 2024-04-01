#!/bin/bash

# 检查ffprobe是否可用
if ! command -v ffprobe &> /dev/null; then
    echo "错误：ffprobe 工具未安装，请先安装 FFmpeg。"
    exit 1
fi

# 检查jq是否可用
if ! command -v jq &> /dev/null; then
    echo "错误：jq 工具未安装，请先安装 jq。"
    exit 1
fi


baseurl=$1
s=$(echo $baseurl|grep -o  '\[.*\]'|sed -e 's/\[//g' -e 's/\]//g'|awk -F"-" '{print $1}')
e=$(echo $baseurl|grep -o  '\[.*\]'|sed -e 's/\[//g' -e 's/\]//g'|awk -F"-" '{print $2}')
output_file="results.txt"

# 计算总数目
total=$((e - s + 1))
count=0

for n in $(seq -w $s $e)
do
  h=""
  w=""
  url=$(echo $baseurl|sed "s/\[.*\]/$n/g")
  res=$(ffprobe -user_agent "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36" -timeout 5000  -select_streams v -show_streams -v quiet -of csv="p=0" -of json -i $url)
  
  if [ $(echo $res|grep -c height) -gt 0 ]; then
    h=$(echo $res|jq .streams[].height)
    w=$(echo $res|jq .streams[].width)
    rate=$(echo $res|jq .streams[].avg_frame_rate|sed -e 's/"//g' -e 's/\/1//g')
    if [ "0$h" != "0" ] && [ "0$w" != "0" ]; then
      echo "$n[${w}X${h}],$url"
      echo "$n[${w}X${h}],$url" >> $output_file
    fi
  fi
  
  # 更新进度
  count=$((count + 1))
  progress=$((count * 100 / total))
  echo -ne "$n, Progress: $progress%\r"
done

echo "结果已保存到 $output_file"