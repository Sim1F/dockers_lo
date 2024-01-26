import numpy as np
import math

def inverse_pose(pose):
    return np.linalg.inv(pose)

def calibrate(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    poses = []

    for line in lines:
        data = line.strip().split(' ')
        if len(data) == 12:
            # skip first one
            # tx, ty, tz = float(data[1]), float(data[2]), float(data[3])
            # qx, qy, qz, qw = float(data[4]), float(data[5]), float(data[6]), float(data[7])

            # skip first two
            # tx, ty, tz = float(data[2]), float(data[3]), float(data[4])
            # qx, qy, qz, qw = float(data[5]), float(data[6]), float(data[7]), float(data[8])

            # # Normalize quaternion
            # norm = np.linalg.norm([qx, qy, qz, qw])
            # qx, qy, qz, qw = qx / norm, qy / norm, qz / norm, qw / norm

            # # Construct the isometry matrix
            # isometry_matrix = np.identity(4)
            # isometry_matrix[:3, :3] = np.array([
            #     [1 - 2 * (qy**2 + qz**2), 2 * (qx*qy - qw*qz), 2 * (qx*qz + qw*qy)],
            #     [2 * (qx*qy + qw*qz), 1 - 2 * (qx**2 + qz**2), 2 * (qy*qz - qw*qx)],
            #     [2 * (qx*qz - qw*qy), 2 * (qy*qz + qw*qx), 1 - 2 * (qx**2 + qy**2)]
            # ])
            # isometry_matrix[:3, 3] = np.array([tx, ty, tz])

            isometry_matrix = np.array([
                [float(data[0]), float(data[1]), float(data[2]), float(data[3])],
                [float(data[4]), float(data[5]), float(data[6]), float(data[7])],
                [float(data[8]), float(data[9]), float(data[10]), float(data[11])],
                [0, 0, 0, 1]
            ])

            # Store the isometry matrix
            poses.append(isometry_matrix)

    ouster_to_base = np.array([
    [-1.0000, -0.0058, 0.0000, 1.7042],
    [0.0058, -1.0000, -0.0000, -0.0210],
    [0.0000, -0.0000, 1.0000, 1.8047],
    [0, 0, 0, 1]
    ])
    base_to_ouster = np.linalg.inv(ouster_to_base)

    # Apply the rotation to the isometry matrix
    rotated_poses = [np.dot(ouster_to_base, np.dot(pose, base_to_ouster)) for pose in poses]

    # Get the first rotated pose as the reference
    reference_pose = rotated_poses[0]

    # Pre-multiply every pose by the inverse of the reference pose
    multiplied_poses = [np.dot(inverse_pose(reference_pose), pose) for pose in rotated_poses]

    with open(output_file, 'w') as f:
        for pose in multiplied_poses:
            # Extract the first 3 rows (12 elements) and write them in the specified order
            for i in range(3):
                for j in range(4):
                    f.write('%.6f ' % pose[i, j])
            f.write('\n')

if __name__ == '__main__':
    input_file = '/media/simone/PortableSSD/datasets/mulran/floam/DCC/DCC01/DCC01_poses_kitti_lidar_frame.txt'
    output_file = '/media/simone/PortableSSD/datasets/mulran/floam/DCC/DCC01/DCC01_poses_kitti.txt'
    calibrate(input_file, output_file)

    input_file = '/media/simone/PortableSSD/datasets/mulran/floam/DCC/DCC02/DCC02_poses_kitti_lidar_frame.txt'
    output_file = '/media/simone/PortableSSD/datasets/mulran/floam/DCC/DCC02/DCC02_poses_kitti.txt'
    calibrate(input_file, output_file)

    input_file = '/media/simone/PortableSSD/datasets/mulran/floam/DCC/DCC03/DCC03_poses_kitti_lidar_frame.txt'
    output_file = '/media/simone/PortableSSD/datasets/mulran/floam/DCC/DCC03/DCC03_poses_kitti.txt'
    calibrate(input_file, output_file)


    input_file = '/media/simone/PortableSSD/datasets/mulran/floam/KAIST/KAIST01/KAIST01_poses_kitti_lidar_frame.txt'
    output_file = '/media/simone/PortableSSD/datasets/mulran/floam/KAIST/KAIST01/KAIST01_poses_kitti.txt'
    calibrate(input_file, output_file)

    input_file = '/media/simone/PortableSSD/datasets/mulran/floam/KAIST/KAIST02/KAIST02_poses_kitti_lidar_frame.txt'
    output_file = '/media/simone/PortableSSD/datasets/mulran/floam/KAIST/KAIST02/KAIST02_poses_kitti.txt'
    calibrate(input_file, output_file)

    input_file = '/media/simone/PortableSSD/datasets/mulran/floam/KAIST/KAIST03/KAIST03_poses_kitti_lidar_frame.txt'
    output_file = '/media/simone/PortableSSD/datasets/mulran/floam/KAIST/KAIST03/KAIST03_poses_kitti.txt'
    calibrate(input_file, output_file)


    input_file = '/media/simone/PortableSSD/datasets/mulran/floam/Riverside/Riverside01/Riverside01_poses_kitti_lidar_frame.txt'
    output_file = '/media/simone/PortableSSD/datasets/mulran/floam/Riverside/Riverside01/Riverside01_poses_kitti.txt'
    calibrate(input_file, output_file)

    input_file = '/media/simone/PortableSSD/datasets/mulran/floam/Riverside/Riverside02/Riverside02_poses_kitti_lidar_frame.txt'
    output_file = '/media/simone/PortableSSD/datasets/mulran/floam/Riverside/Riverside02/Riverside02_poses_kitti.txt'
    calibrate(input_file, output_file)

    input_file = '/media/simone/PortableSSD/datasets/mulran/floam/Riverside/Riverside03/Riverside03_poses_kitti_lidar_frame.txt'
    output_file = '/media/simone/PortableSSD/datasets/mulran/floam/Riverside/Riverside03/Riverside03_poses_kitti.txt'
    calibrate(input_file, output_file)


    input_file = '/media/simone/PortableSSD/datasets/mulran/floam/Sejong/Sejong01/Sejong01_poses_kitti_lidar_frame.txt'
    output_file = '/media/simone/PortableSSD/datasets/mulran/floam/Sejong/Sejong01/Sejong01_poses_kitti.txt'
    calibrate(input_file, output_file)

    input_file = '/media/simone/PortableSSD/datasets/mulran/floam/Sejong/Sejong02/Sejong02_poses_kitti_lidar_frame.txt'
    output_file = '/media/simone/PortableSSD/datasets/mulran/floam/Sejong/Sejong02/Sejong02_poses_kitti.txt'
    calibrate(input_file, output_file)

    input_file = '/media/simone/PortableSSD/datasets/mulran/floam/Sejong/Sejong03/Sejong03_poses_kitti_lidar_frame.txt'
    output_file = '/media/simone/PortableSSD/datasets/mulran/floam/Sejong/Sejong03/Sejong03_poses_kitti.txt'
    calibrate(input_file, output_file)