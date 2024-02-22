from pathlib import Path
from scipy.spatial.transform import Rotation as R
import numpy as np
from tqdm import tqdm

"""
Converts the pose of the replica dataset to the format of colmap.
make empty cameras.txt and points3D.txt

Input format:
    - CamPose.txt
        - frame_id, w2c00, w2c01, w2c02, w2c03, w2c10, w2c11, w2c12, w2c13, w2c20, w2c21, w2c22, w2c23, w2c30, w2c31, w2c32, w2c33
Output format:
    - images.txt
        - image_id, qw, qx, qy, qz, tx, ty, tz, camera_id, name
"""

def pose_converter(input_path: Path, output_path: Path) -> int:
    if not output_path.parent.exists():
        output_path.parent.mkdir(parents=True)
    count = 0
    with open(input_path, 'r') as replica_pose:
        with open(output_path, 'w') as colmap_pose:
            for line in tqdm(replica_pose):
                if line.startswith('#'):
                    continue
                else:
                    count += 1
                    line = line.strip().split(' ')
                    frame_id = line[0]
                    c2w = np.array(line[1:]).astype(np.float32).reshape(4, 4)
                    w2c = np.linalg.inv(c2w)
                    r = w2c[:3, :3]
                    t = w2c[:3, 3]
                    t = -r.T @ t
                    q = R.from_matrix(r.T).as_quat()  # x y z w
                    q = np.array([q[3], q[0], q[1], q[2]])  # w x y z
                    # colmap_pose.write(f"{int(frame_id)} {q[0]} {q[1]} {q[2]} {q[3]} {t[0]} {t[1]} {t[2]} 0 images/frame{frame_id}.jpg\n\n")  # frame000000.jpg. 6 zero padding
                    colmap_pose.write(f"{int(frame_id)} {q[0]} {q[1]} {q[2]} {q[3]} {t[0]} {t[1]} {t[2]} 0 frame{frame_id}.jpg\n\n")  # frame000000.jpg. 6 zero padding
    print(f"Total {count} frame poses are converted.")
    with open(output_path.parent / "cameras.txt", 'w') as f:
        f.write("0 PINHOLE 1280 960 640 640 640 480\n")  # intrinsic hardcoded. look capture.cpp L
    with open(output_path.parent / "points3D.txt", 'w') as f:
        f.write("")
    return count


if __name__ == "__main__":
    # input_path = Path("/home/keunmo/workspace/Replica-Dataset/output/apartment_1_cam_arr2/camPose.txt")
    # output_path = Path("/home/keunmo/workspace/Replica-Dataset/output/apartment_1_cam_arr2/sparse/model/images.txt")
    # pose_converter(input_path, output_path)
    dataset_list = ['apartment_1_test', 'room_0_test', 'room_0_cam_arr1', 'room_0_cam_arr2', 'room_0_circle1', 'room_0_slam1']
    # dataset_list = ['apartment_1_cam_arr1']
    for dataset in dataset_list:
        input_path = Path(f"/home/keunmo/workspace/Replica-Dataset/output/{dataset}/camPose.txt")
        output_path = Path(f"/home/keunmo/workspace/Replica-Dataset/output/{dataset}/sparse/model/images.txt")
        pose_converter(input_path, output_path)