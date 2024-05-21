# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from pathlib import Path

import cv2
import numpy as np

from paddleocr_onnx.infer import predict_system
from paddleocr_onnx.infer.utility import alpha_to_color, binarize_img, str2bool
from paddleocr_onnx.ppstructure.utility import init_args


def parse_args(mMain=True):
    import argparse

    parser = init_args()
    parser.add_help = mMain
    parser.add_argument("--lang", type=str, default="en")
    parser.add_argument("--det", type=str2bool, default=True)
    parser.add_argument("--rec", type=str2bool, default=True)
    parser.add_argument("--type", type=str, default="ocr")
    parser.add_argument("--savefile", type=str2bool, default=False)
    parser.add_argument(
        "--ocr_version",
        type=str,
        default="PP-OCRv4",
        help="OCR Model version, the current model support list is as follows: "
        "1. PP-OCRv4/v3 Support Chinese and English detection and recognition model, and direction classifier model"
        "2. PP-OCRv2 Support Chinese detection and recognition model. "
        "3. PP-OCR support Chinese detection, recognition and direction classifier and multilingual recognition model.",
    )
    parser.add_argument(
        "--structure_version",
        type=str,
        default="PP-StructureV2",
        help="Model version, the current model support list is as follows:"
        " 1. PP-Structure Support en table structure model."
        " 2. PP-StructureV2 Support ch and en table structure model.",
    )

    for action in parser._actions:
        if action.dest in [
            "rec_char_dict_path",
            "table_char_dict_path",
            "layout_dict_path",
        ]:
            action.default = None
    if mMain:
        return parser.parse_args()
    else:
        inference_args_dict = {}
        for action in parser._actions:
            inference_args_dict[action.dest] = action.default
        return argparse.Namespace(**inference_args_dict)


def img_decode(content: bytes):
    np_arr = np.frombuffer(content, dtype=np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_UNCHANGED)


class PaddleOCR(predict_system.TextSystem):
    def __init__(self, **kwargs):
        """
        paddleocr package
        args:
            **kwargs: other params show in paddleocr --help
        """
        params = parse_args(mMain=False)
        params.__dict__.update(**kwargs)

        root_dir = Path(__file__).resolve().parent

        self.use_angle_cls = params.use_angle_cls

        if params.det_model_dir is None:
            params.det_model_dir = root_dir / "models/en_PP-OCRv3_det_infer.onnx"

        if params.rec_model_dir is None:
            params.rec_model_dir = root_dir / "models/en_PP-OCRv4_rec_infer.onnx"

        params.rec_image_shape = "3, 48, 320"

        if params.rec_char_dict_path is None:
            params.rec_char_dict_path = root_dir / "dict/en_dict.txt"

        # init det_model and rec_model
        super().__init__(params)
        self.page_num = params.page_num

    def ocr(
        self,
        img,
        det=True,
        rec=True,
        cls=False,
        bin=False,
        inv=False,
        alpha_color=(255, 255, 255),
    ):
        """
        OCR with PaddleOCR

        args:
            img: img for OCR, support ndarray, img_path and list or ndarray
            det: use text detection or not. If False, only rec will be exec. Default is True
            rec: use text recognition or not. If False, only det will be exec. Default is True
            cls: use angle classifier or not. Default is True. If True, the text with rotation of 180 degrees can be recognized. If no text is rotated by 180 degrees, use cls=False to get better performance. Text with rotation of 90 or 270 degrees can be recognized even if cls=False.
            bin: binarize image to black and white. Default is False.
            inv: invert image colors. Default is False.
            alpha_color: set RGB color Tuple for transparent parts replacement. Default is pure white.
        """
        assert isinstance(img, (np.ndarray, list, str, bytes))
        if isinstance(img, list) and det:
            exit(0)

        imgs = [img]

        def preprocess_image(_image):
            _image = alpha_to_color(_image, alpha_color)
            if inv:
                _image = cv2.bitwise_not(_image)
            if bin:
                _image = binarize_img(_image)
            return _image

        if det and rec:
            ocr_res = []
            for idx, img in enumerate(imgs):
                img = preprocess_image(img)
                dt_boxes, rec_res, _ = self.__call__(img, cls)
                if not dt_boxes and not rec_res:
                    ocr_res.append(None)
                    continue
                tmp_res = [[box.tolist(), res] for box, res in zip(dt_boxes, rec_res)]
                ocr_res.append(tmp_res)
            return ocr_res
