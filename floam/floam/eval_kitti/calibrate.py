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

    velodyne_to_left_cam = np.array([
    [4.276802385584e-04, -9.999672484946e-01, -8.084491683471e-03, -1.198459927713e-02],
    [-7.210626507497e-03, 8.081198471645e-03, -9.999413164504e-01, -5.403984729748e-02],
    [9.999738645903e-01, 4.859485810390e-04, -7.206933692422e-03, -2.921968648686e-01],
    [0, 0, 0, 1]
    ])
    left_cam_to_velodyne = np.linalg.inv(velodyne_to_left_cam)

    # Apply the rotation to the isometry matrix
    rotated_poses = [np.dot(velodyne_to_left_cam, np.dot(pose, left_cam_to_velodyne)) for pose in poses]

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
    # input_file = '/media/simone/PortableSSD/datasets/kitti/floam/00/00_poses_kitti_lidar_frame.txt'
    # output_file = '/media/simone/PortableSSD/datasets/kitti/floam/00/00_poses_kitti.txt'
    # calibrate(input_file, output_file)
    
    # input_file = '/media/simone/PortableSSD/datasets/kitti/floam/01/01_poses_kitti_lidar_frame.txt'
    # output_file = '/media/simone/PortableSSD/datasets/kitti/floam/01/01_poses_kitti.txt'
    # calibrate(input_file, output_file)

    # input_file = '/media/simone/PortableSSD/datasets/kitti/floam/02/02_poses_kitti_lidar_frame.txt'
    # output_file = '/media/simone/PortableSSD/datasets/kitti/floam/02/02_poses_kitti.txt'
    # calibrate(input_file, output_file)

    # input_file = '/media/simone/PortableSSD/datasets/kitti/floam/03/03_poses_kitti_lidar_frame.txt'
    # output_file = '/media/simone/PortableSSD/datasets/kitti/floam/03/03_poses_kitti.txt'
    # calibrate(input_file, output_file)
    
    # input_file = '/media/simone/PortableSSD/datasets/kitti/floam/04/04_poses_kitti_lidar_frame.txt'
    # output_file = '/media/simone/PortableSSD/datasets/kitti/floam/04/04_poses_kitti.txt'
    # calibrate(input_file, output_file)

    # input_file = '/media/simone/PortableSSD/datasets/kitti/floam/05/05_poses_kitti_lidar_frame.txt'
    # output_file = '/media/simone/PortableSSD/datasets/kitti/floam/05/05_poses_kitti.txt'
    # calibrate(input_file, output_file)

    # input_file = '/media/simone/PortableSSD/datasets/kitti/floam/06/06_poses_kitti_lidar_frame.txt'
    # output_file = '/media/simone/PortableSSD/datasets/kitti/floam/06/06_poses_kitti.txt'
    # calibrate(input_file, output_file)
    
    # input_file = '/media/simone/PortableSSD/datasets/kitti/floam/07/07_poses_kitti_lidar_frame.txt'
    # output_file = '/media/simone/PortableSSD/datasets/kitti/floam/07/07_poses_kitti.txt'
    # calibrate(input_file, output_file)

    # input_file = '/media/simone/PortableSSD/datasets/kitti/floam/08/08_poses_kitti_lidar_frame.txt'
    # output_file = '/media/simone/PortableSSD/datasets/kitti/floam/08/08_poses_kitti.txt'
    # calibrate(input_file, output_file)

    # input_file = '/media/simone/PortableSSD/datasets/kitti/floam/09/09_poses_kitti_lidar_frame.txt'
    # output_file = '/media/simone/PortableSSD/datasets/kitti/floam/09/09_poses_kitti.txt'
    # calibrate(input_file, output_file)

    # input_file = '/media/simone/PortableSSD/datasets/kitti/floam/10/10_poses_kitti_lidar_frame.txt'
    # output_file = '/media/simone/PortableSSD/datasets/kitti/floam/10/10_poses_kitti.txt'
    # calibrate(input_file, output_file)
