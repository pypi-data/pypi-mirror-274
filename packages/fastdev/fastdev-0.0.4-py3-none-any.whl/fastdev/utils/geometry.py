from typing import Dict, Literal, Sequence, Union

import numpy as np

box_data = {
    "vertices": [
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 1.0],
        [0.0, 1.0, 0.0],
        [0.0, 1.0, 1.0],
        [1.0, 0.0, 0.0],
        [1.0, 0.0, 1.0],
        [1.0, 1.0, 0.0],
        [1.0, 1.0, 1.0],
    ],
    "faces": [
        [1, 3, 0],
        [4, 1, 0],
        [0, 3, 2],
        [2, 4, 0],
        [1, 7, 3],
        [5, 1, 4],
        [5, 7, 1],
        [3, 7, 2],
        [6, 4, 2],
        [2, 7, 6],
        [6, 5, 4],
        [7, 5, 6],
    ],
    "face_normals": [
        [-1, 0, 0],
        [0, -1, 0],
        [-1, 0, 0],
        [0, 0, -1],
        [0, 0, 1],
        [0, -1, 0],
        [0, 0, 1],
        [0, 1, 0],
        [0, 0, -1],
        [0, 1, 0],
        [1, 0, 0],
        [1, 0, 0],
    ],
}


def create_box(
    half_size: Union[Sequence[float], np.ndarray] = [1.0, 1.0, 1.0],
) -> Dict[Literal["vertices", "faces"], np.ndarray]:
    vertices = np.asarray(box_data["vertices"], dtype=np.float32)
    vertices = (vertices - 0.5) * 2.0 * half_size
    faces = np.asarray(box_data["faces"], dtype=np.int32)
    return {"vertices": vertices, "faces": faces}
