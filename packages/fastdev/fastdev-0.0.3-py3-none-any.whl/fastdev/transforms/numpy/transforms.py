import numpy as np


def transform(pts: np.ndarray, tf_mat: np.ndarray) -> np.ndarray:
    """
    Apply a transformation matrix on a set of 3D points.

    Args:
        pts: 3D points, could be [..., N, 3]
        tf_mat: Transformation matrix, could be [..., 4, 4]

        The dimension number of pts and tf_mat should be the same.

    Returns:
        Transformed pts.
    """
    if pts.ndim != tf_mat.ndim:
        raise ValueError("The dimension number of pts and tf_mat should be the same.")

    homo_pts = to_homo(pts)
    # `homo_pts @ tf_mat.T` or `(tf_mat @ homo_pts.T).T`
    new_pts = np.matmul(homo_pts, np.swapaxes(tf_mat, -2, -1))
    return new_pts[..., :3]


def to_homo(pts_3d: np.ndarray) -> np.ndarray:
    """
    Convert Cartesian 3D points to Homogeneous 4D points.

    Args:
      pts_3d: 3D points in Cartesian coord, could be ...x3.
    Returns:
      ...x4 points in the Homogeneous coord.
    """
    return np.concatenate([pts_3d, np.ones_like(pts_3d[..., :1])], axis=-1)
