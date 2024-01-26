#!/bin/bash

SEQS=("catacombs_easy" "catacombs_medium" "cloister" "math_easy" "math_medium" "quad_easy" "quad_medium" "stairs")

# iterate through all sequences
for seq in ${SEQS[@]}; do
    echo "launching experiments of seq " ${seq}
    kiss_icp_pipeline os0_newer_college/${seq}/os/
done