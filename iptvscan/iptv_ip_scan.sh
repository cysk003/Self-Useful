#!/bin/bash

# Check if ffprobe and jq are available
if ! command -v ffprobe &> /dev/null || ! command -v jq &> /dev/null; then
    echo "Error: ffprobe or jq not installed. Please install FFmpeg and jq."
    exit 1
fi

# Prompt the user to input the base URL and provide an example
read -p "Enter the base URL, e.g., http://example.com/video_[start-end].mp4: " baseurl

# Validate parameters
if [ -z "$baseurl" ]; then
    echo "Error: Base URL not provided."
    exit 1
fi

# Parse the start and end numbers from the base URL
if [[ $baseurl =~ \[([0-9]+)-([0-9]+)\] ]]; then
    start=${BASH_REMATCH[1]}
    end=${BASH_REMATCH[2]}
else
    echo "Error: Unable to parse start and end numbers."
    exit 1
fi

# Ensure the end number has the same length as the start number, padding with zeros if necessary
end_length=${#end}
end=$(printf "%0${end_length}d" "$end")

output_file="results.txt"

# Calculate the total number of URLs
total=$((end - start + 1))
count=0

echo "Checking video resolutions..."

# Iterate over the URL range
for ((number=start; number<=end; number++))
do
    url=$(echo "$baseurl" | sed "s/\[$start-$end\]/$number/")
    echo "Checking video: $url"
    
    # Get video information
    res=$(ffprobe -user_agent "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36" -timeout 5000  -select_streams v -show_streams -v quiet -of csv="p=0" -of json -i "$url")

    # Check if video information retrieval was successful
    if [[ -z "$res" ]]; then
        echo "Warning: Unable to retrieve video information."
    else
        # Extract resolution and frame rate
        if [[ $res == *'"height"'* && $res == *'"width"'* ]]; then
            resolution=$(jq -r '.streams[0] | "\(.width)x\(.height)"' <<< "$res")
            rate=$(jq -r '.streams[0].avg_frame_rate' <<< "$res")
            echo "$number[$resolution] @ $rate, $url"
            echo "$number[$resolution] @ $rate, $url" >> "$output_file"
        else
            echo "Warning: Video resolution or width not detected."
        fi
    fi

    # Update progress
    ((count++))
    echo "Progress: $((count * 100 / total))% complete ($count/$total)"
done

echo "Video resolution check completed. Results saved in: $output_file"
