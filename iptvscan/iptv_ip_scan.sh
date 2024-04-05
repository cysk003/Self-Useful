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
if [[ $baseurl =~ ([0-9]+)-([0-9]+) ]]; then
    start=${BASH_REMATCH[1]}
    end=${BASH_REMATCH[2]}
else
    echo "错误：无法解析起始和结束数字。"
    exit 1
fi

output_file="results.txt"

# 计算总数目
total=$((end - start + 1))
count=0

echo "开始检查视频分辨率..."

for number in $(seq -w $start $end)
do
    url="${baseurl//\[start-end\]/$number}"
    res=$(ffprobe -user_agent "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36" -timeout 5000  -select_streams v -show_streams -v quiet -of csv="p=0" -of json -i "$url")

    if [[ $res == *'"height"'* && $res == *'"width"'* ]]; then
        height=$(jq -r '.streams[0].height' <<< "$res")
        width=$(jq -r '.streams[0].width' <<< "$res")
        rate=$(jq -r '.streams[0].avg_frame_rate' <<< "$res")
        echo "$number[${width}x${height}] @ $rate, $url"
        echo "$number[${width}x${height}] @ $rate, $url" >> "$output_file"
    fi

    # 更新进度
    count=$((count + 1))
    progress=$((count * 100 / total))
    echo -ne "正在检查: $number, 进度: $progress%\r"
done

echo "检查完成，结果已保存到 $output_file"
