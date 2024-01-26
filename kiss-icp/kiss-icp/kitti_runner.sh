#!/bin/bash

SEQS=("00" "01" "02" "03" "04" "05" "06" "07" "08" "09" "10")

# iterate through all sequences
for seq in ${SEQS[@]}; do
    echo "launching experiments of seq " ${seq}
    kiss_icp_pipeline kitti/data_odometry_velodyne/dataset/ --dataloader kitti --sequence ${seq}
done