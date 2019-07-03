#!/bin/bash

N=1

dir_images_in_input=multiplex_eval_results/input
dir_images_in_set_a=multiplex_eval_results/supervised
dir_images_in_set_b=multiplex_eval_results/unsupervised

dir_images_out_input=validate_images_input
dir_images_out_set_a=validate_images_set_a
dir_images_out_set_b=validate_images_set_b

rm -rf ${dir_images_out_set_a}/*
rm -rf ${dir_images_out_set_b}/*
rm -rf ${dir_images_out_input}/*

for filepath in ${dir_images_in_input}/*; do
  echo $filepath
  filename=$(basename $filepath)
  cp ${dir_images_in_set_a}/${filename} ${dir_images_out_set_a}/${N}.png
  cp ${dir_images_in_set_b}/${filename} ${dir_images_out_set_b}/${N}.png
  cp ${dir_images_in_input}/${filename} ${dir_images_out_input}/${N}.png
  echo ${N} ${filename} >> $dir_images_out_input/info.txt
  echo ${filename} >> ${dir_images_out_input}/${N}_info_FN.txt
  N=$((N+1))
done


exit 0
