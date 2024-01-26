#!/bin/bash

SEQS=("drone" "lab")

# iterate through all sequences
for seq in ${SEQS[@]}; do
    echo "launching experiments of seq " ${seq}
    kiss_icp_pipeline hilti_2021/${seq}/os/
done