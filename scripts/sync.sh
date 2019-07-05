#!/bin/bash
# author: gfw-breaker

cd $(dirname $0)

channelMap="zhoukan:qikan_type_id=5179
zhongguo:qikan_type_id=5178
mingbai:qikan_type_id=5140
zhenxiang:qikan_type_id=5240
huisheng:qikan_type_id=5638
xiwang:qikan_type_id=5406
cangsheng:qikan_type_id=5139
huabao:qikan_type_id=6272
hongfu:qikan_type_id=5360"

## get feeds files
for entry in $channelMap ; do
	channel=$(echo $entry | cut -d':' -f1)
	category=$(echo $entry | cut -d':' -f2)
	mkdir -p ../pages/$channel
	url="http://qikan.minghui.org/display.aspx?$category"
	echo "getting channel: $url"
	python parse_mhqikan.py $channel "$url"
done

## git 
git pull
git add ../*
git commit -a -m ok
git push


