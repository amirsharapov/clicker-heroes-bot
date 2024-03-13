from pathlib import Path

import cv2
import numpy as np


def crop(image, x, y, w, h):
    return image[y:y + h, x:x + w]


def get_alpha_mask(template: np.ndarray):
    assert template.shape[2] == 4, 'Template must have 4 channels.'

    mask = template[:, :, 3]
    mask = cv2.threshold(
        mask,
        0,
        255,
        cv2.THRESH_BINARY
    )[1]

    return mask


def match_template(
        image,
        template,
        threshold: float = 0.9,
        method: int = cv2.TM_CCOEFF_NORMED,
        mask: np.ndarray = None
):
    """
    Match a template in an image and return an iterator of 2 points.

    Both images must be grayscale.
    """
    w, h = template.shape[::-1]

    result = cv2.matchTemplate(
        image,
        template,
        method,
        None,
        mask
    )

    locations = np.where(result >= threshold)

    for point in zip(*locations[::-1]):
        yield point, (point[0] + w, point[1] + h)


def match_template_from_path(
        image: np.ndarray,
        path: str | Path,
        threshold: float = 0.8,
        method: int = cv2.TM_CCOEFF_NORMED,
        use_mask: bool = False
):
    template = cv2.imread(
        path,
        cv2.IMREAD_UNCHANGED
    )

    template_mask = get_alpha_mask(template) if use_mask else None

    template = cv2.cvtColor(
        template,
        cv2.COLOR_BGR2GRAY
    )

    for pt1, pt2 in match_template(
            image,
            template,
            threshold,
            method,
            template_mask,
    ):
        yield pt1, pt2
