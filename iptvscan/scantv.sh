#!/bin/bash

# 参数验证
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <baseurl>"
    exit 1
fi

# 检查ffprobe和jq是否可用
if ! command -v ffprobe &> /dev/null || ! command -v jq &> /dev/null; then
    echo "错误：ffprobe 或 jq 工具未安装，请先安装 FFmpeg 和 jq。"
    exit 1
fi

baseurl=$1
s=$(echo "$baseurl" | grep -o  '\[.*\]' | sed 's/\[//g; s/\]//g' | awk -F"-" '{print $1}')
e=$(echo "$baseurl" | grep -o  '\[.*\]' | sed 's/\[//g; s/\]//g' | awk -F"-" '{print $2}')
output_file="results.txt"

# 计算总数目
total=$((e - s + 1))
count=0

# 处理函数
process_url() {
    local url="$1"
    local res=$(ffprobe -user_agent "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36" -timeout 5000  -select_streams v -show_streams -v quiet -of csv="p=0" -of json -i "$url")
    local h=""
    local w=""
    local rate=""

    if [ $(echo "$res" | jq '.streams | length') -gt 0 ]; then
        h=$(echo "$res" | jq '.streams[0].height')
        w=$(echo "$res" | jq '.streams[0].width')
        rate=$(echo "$res" | jq -r '.streams[0].avg_frame_rate' | sed 's/\/1//g')
    fi

    if [ "0$h" != "0" ] && [ "0$w" != "0" ]; then
        echo "$n[${w}X${h}],$url"
        echo "$n[${w}X${h}],$url" >> "$output_file"
    fi
}

# 并行处理URL
for n in $(seq -w "$s" "$e"); do
    url=$(echo "$baseurl" | sed "s/\[.*\]/$n/g")
    process_url "$url" &
    pids[${n}]=$!
done

# 等待所有进程结束
for pid in "${pids[@]}"; do
    wait "$pid"
    count=$((count + 1))
    progress=$((count * 100 / total))
    echo -ne "$n, Progress: $progress%\r"
done

echo "结果已保存到 $output_file"
