#!/bin/bash

N=1

rm -rf images/*
while read line; do
	FN=`echo ${line} | awk '{print $1}'`
	LB=`echo ${line} | awk '{print $2}'`
	ID=`echo ${line} | awk '{print $3}'`
	cp patches_from_heatmap/${FN} images/${N}.png
	echo ${N} ${FN} ${LB} ${ID} >> images/info.txt
        echo ${FN} >> images/${N}_info_FN.txt
        echo ${ID} >> images/${N}_info_ID.txt
	N=$((N+1))
done < ./patches_from_heatmap/label.txt

#matlab -nodisplay -r "add_center_rectangle; exit" </dev/null

exit 0
