#!/bin/bash

SEQS=("01_short_experiment" "02_long_experiment" "07_parkland_mound")

# iterate through all sequences
for seq in ${SEQS[@]}; do
    echo "launching experiments of seq " ${seq}
    kiss_icp_pipeline os1_newer_college/${seq}/os/
done