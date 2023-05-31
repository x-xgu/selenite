import base64
from io import BytesIO
from pathlib import Path
from typing import Union, Tuple

import ddddocr
from PIL import Image
from selene import Element, query, be
from skimage.metrics import structural_similarity as ssim

from selenite import common

# TRANSLATE_CANVAS_TO_PNG
# This script will translate canvas to png
TRANSLATE_CANVAS_TO_PNG = \
    'var canvas = self; ' \
    'return canvas.toDataURL("image/png");'

# TRANSLATE_CANVAS_TO_PNG_WITH_WHITE_BACKGROUND
# This script will add white background to canvas
TRANSLATE_CANVAS_TO_PNG_WITH_WHITE_BACKGROUND = \
    'var canvas = self;' \
    'var context = canvas.getContext("2d");' \
    'context.globalCompositeOperation="destination-over";' \
    'context.fillStyle="white";' \
    'context.fillRect(0,0,canvas.width,canvas.height);' \
    'context.globalCompositeOperation="source-over";' \
    'return canvas.toDataURL("image/png");'


def get_canvas_bytes(
        element: Element,
        add_background: bool = False
) -> bytes:
    """
    Get canvas bytes
    """
    element.wait_until(be.visible)
    img_data = element.execute_script(
        TRANSLATE_CANVAS_TO_PNG
        if not add_background
        else TRANSLATE_CANVAS_TO_PNG_WITH_WHITE_BACKGROUND
    )
    img_base64 = img_data.split(',')[1]
    img_bytes = base64.b64decode(img_base64)
    return img_bytes


def save_canvas_bytes_to_file(
        element: Element,
        path: Union[str, Path],
        add_background: bool = False
) -> None:
    """
    Save canvas bytes to file
    """
    element.wait_until(be.visible)
    image_bytes = get_canvas_bytes(element, add_background)
    with open(path, 'wb') as f:
        f.write(image_bytes)


def pic_compare_with_ssim(
        image1: bytes,
        image2: bytes
) -> float:
    """
    Compare two images with ssim
    """
    score, _ = ssim(
        common.convert.bytes_to_numpy(image1),
        common.convert.bytes_to_numpy(image2),
        full=True
    )
    return score


def compare_canvas_similarity(
        canvas: Element,
        origin_image: Union[bytes, str, Path]
) -> float:
    """
    Compare canvas similarity with origin image
    """
    img_bytes = get_canvas_bytes(canvas)
    if isinstance(origin_image, (str, Path)):
        with open(origin_image, 'rb') as f:
            origin_image = f.read()

    return pic_compare_with_ssim(img_bytes, origin_image)


def recognize_img_text(
        img_bytes: bytes,
        recognize_area: Tuple[int, int, int, int] = None
) -> str:
    """
    Recognize image text
    """
    with Image.open(BytesIO(img_bytes)) as img:
        recognize_part = img.crop(recognize_area) if recognize_area else img
        ocr = ddddocr.DdddOcr(show_ad=False)
        return ocr.classification(recognize_part) or None


def recognize_canvas_text_with_area(
        element: Element,
        left: float = 0,
        upper: float = 0,
        right: float = 1,
        lower: float = 1
) -> str:
    """
    Recognize canvas text with area
    """
    width_str = element.get(query.attribute('width'))
    height_str = element.get(query.attribute('height'))
    if width_str.isdigit() and height_str.isdigit():
        width, height = eval(width_str), eval(height_str)
        recognize_area = (
            int(left * width),
            int(upper * height),
            int(right * width),
            int(lower * height)
        )
        img_bytes = get_canvas_bytes(element, add_background=True)
        text = recognize_img_text(img_bytes, recognize_area)
        return text
    else:
        return ''
