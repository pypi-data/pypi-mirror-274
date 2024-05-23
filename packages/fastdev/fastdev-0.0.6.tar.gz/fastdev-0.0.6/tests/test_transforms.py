import torch
import numpy as np
from fastdev.transforms import rot_tl_to_tf_mat, transform


def test_transforms():
    pts = torch.tensor([[1, 2, 3], [4, 5, 6]], dtype=torch.float32)
    rot_mat = torch.tensor([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=torch.float32)
    tl = torch.tensor([1, 2, 3], dtype=torch.float32)
    tf_mat = rot_tl_to_tf_mat(rot_mat, tl)

    new_pts = transform(pts, tf_mat)

    tgt_pts = torch.tensor([[3, 5, 4], [6, 8, 7]], dtype=torch.float32)
    assert torch.allclose(new_pts, tgt_pts)

    new_pts = transform(pts.numpy(), tf_mat.numpy())
    assert torch.allclose(torch.tensor(new_pts), tgt_pts)

    new_pts = transform(pts[None], tf_mat[None])[0]
    assert torch.allclose(new_pts, tgt_pts)

    new_pts = transform(pts.to(dtype=torch.float16), tf_mat.to(dtype=torch.float16))
    assert torch.allclose(new_pts, tgt_pts.to(dtype=torch.float16))
    assert new_pts.dtype == torch.float16

    new_pts = transform(pts.numpy().astype("float16"), tf_mat.numpy().astype("float16"))
    assert new_pts.dtype == np.float16
    assert torch.allclose(torch.tensor(new_pts), tgt_pts.to(dtype=torch.float16))

if __name__ == "__main__":
    test_transforms()
