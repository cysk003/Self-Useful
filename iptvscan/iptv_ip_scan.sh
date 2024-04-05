#!/bin/bash

# 提示用户输入基本URL，并提供示例
echo "请输入基本URL，示例："
echo "http://example.com/video_[start-end].mp4"
echo "其中，[start-end] 是要替换的起始和结束数字部分。"

# 读取用户输入的基本URL
read -p "请输入基本URL: " baseurl

# 参数验证
if [ -z "$baseurl" ]; then
    echo "错误：未提供基本URL。"
    exit 1
fi

# 检查ffprobe和jq是否可用
if ! command -v ffprobe &> /dev/null || ! command -v jq &> /dev/null; then
    echo "错误：ffprobe 或 jq 工具未安装，请先安装 FFmpeg 和 jq。"
    exit 1
fi

# 解析基本URL中的起始和结束数字
s=$(echo $baseurl|grep -o  '\[.*\]'|sed -e 's/\[//g' -e 's/\]//g'|awk -F"-" '{print \$1}')
e=$(echo $baseurl|grep -o  '\[.*\]'|sed -e 's/\[//g' -e 's/\]//g'|awk -F"-" '{print \$2}')
output_file="results.txt"

# 计算总数目
total=$((e - s + 1))
count=0

echo "开始检查视频分辨率..."

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
      echo "$n[${w}x${h}] @ $rate, $url"
      echo "$n[${w}x${h}] @ $rate, $url" >> $output_file
    fi
  fi
  
  # 更新进度
  count=$((count + 1))
  progress=$((count * 100 / total))
  echo -ne "正在检查: $n, 进度: $progress%\r"
done

echo "检查完成，结果已保存到 $output_file"
