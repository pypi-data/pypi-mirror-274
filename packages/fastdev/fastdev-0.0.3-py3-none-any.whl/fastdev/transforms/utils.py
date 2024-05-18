import numpy as np

COMMON_COORDS = {
    "opencv": "x: right, y: down, z: front",
    "opengl": "x: right, y: up, z: back",
    "pytorch3d": "x: left, y: up, z: front",
    "sapien": "x: front, y: left, z: up",
}


def coord_conversion(rule="opencv -> opengl", check_handness=True):
    """
    Construct a rotation matrix based on a given rule.

    Following rules are equivalent:
        - "x: right, y: down, z: front -> x: right, y: up, z: back"
        - "right, down, front -> right, up, back"
        - "opencv -> opengl"
        - "x, -y, -z"

    Args:
        rule: rule string
        return_tensor: if True return torch.Tensor, else return np.ndarray
        check_handness: if True check if the handness of the rotation matrix is correct

    Returns:
        rot_mat
    """
    if "->" in rule:
        # replace_list = [("backward", "back"), ("forward", "front")]
        # rule = [rule.replace(*item) for item in replace_list][0]
        coords = rule.split("->")
        coords = [coord.strip().lower() for coord in coords]
        coords = [COMMON_COORDS.get(coord, coord) for coord in coords]

        for idx, coord in enumerate(coords):
            if "x" in coord:
                dirs = {item.split(":")[0]: item.split(":")[1] for item in coord.split(",")}
                dirs = {k.strip(): v.strip() for k, v in dirs.items()}
                dirs = [dirs[axis] for axis in ["x", "y", "z"]]
                coords[idx] = dirs  # type: ignore
            else:
                coords[idx] = [x.strip() for x in coord.split(",")]  # type: ignore

        src_coord, dst_coord = coords

        opp_dirs = {"left": "right", "right": "left", "up": "down", "down": "up", "front": "back", "back": "front"}
        src_axes = [
            ["x", "y", "z"][src_coord.index(dir)]
            if dir in src_coord
            else "-" + ["x", "y", "z"][src_coord.index(opp_dirs[dir])]
            for dir in dst_coord
        ]
    else:
        src_axes = rule.split(",")
        src_axes = [axis.strip().lower() for axis in src_axes]

    negs = [-1 if "-" in axis else 1 for axis in src_axes]
    axes = [["x", "y", "z"].index(axis.replace("-", "")) for axis in src_axes]
    rot_mat = np.zeros((3, 3), np.float32)
    rot_mat[np.arange(3), axes] = negs

    if check_handness:
        if np.linalg.det(rot_mat) < 0:
            raise RuntimeWarning("The rotation matrix is not right-hand.")

    return rot_mat


def compose_intr_mat(fu: float, fv: float, cu: float, cv: float, skew: float = 0.0):
    """
    Args:
        fu: horizontal focal length (width)
        fv: vertical focal length (height)
        cu: horizontal principal point (width)
        cv: vertical principal point (height)
        skew: skew coefficient, default to 0
    """
    intr_mat = np.array([[fu, skew, cu], [0.0, fv, cv], [0.0, 0.0, 1.0]], dtype=np.float32)
    return intr_mat
