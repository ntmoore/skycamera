#!/bin/bash
#
# How do you rename/cp a bunch of image files so that ffmpeg can make a movie out of them?
#

i=1000  # counter to make left padded zeros easy

for file in sky-*.jpg
do
	echo "cp" "$file" "img_${i}.jpg"
	cp "$file" "img_${i}.jpg"
	((i=i+1))
done

# then make a movie with 
# ffmpeg -r 1 -i img_10%2d.jpg -c:v libx264 -vf fps=25 -pix_fmt yuv420p out.mp4
