#!/bin/bash

SEQS=("DCC01" "DCC02" "DCC03" "KAIST01" "KAIST02" "KAIST03" "Riverside01" "Riverside02" "Riverside03" "Sejong01" "Sejong02" "Sejong03")

# iterate through all sequences
for seq in ${SEQS[@]}; do
    echo "launching experiments of seq " ${seq}
    kiss_icp_pipeline mulran/sequences/${seq} --dataloader mulran --config /app/kiss-icp/config/mulran.yaml --deskew
done