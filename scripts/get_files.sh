#!/usr/bin/env bash
while IFS="" read -r url; do
	echo "Downloading $url"
	wget $url -P "../srcpdfs"
done < ../urls/urls.txt
