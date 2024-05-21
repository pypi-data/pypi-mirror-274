from infer.utility import init_args as infer_args
from infer.utility import str2bool, str2int_tuple


def init_args():
    parser = infer_args()

    # params for output
    parser.add_argument("--output", type=str, default="./output")
    # params for table structure
    parser.add_argument("--table_max_len", type=int, default=488)
    parser.add_argument("--table_algorithm", type=str, default="TableAttn")
    parser.add_argument("--table_model_dir", type=str)
    parser.add_argument("--merge_no_span_structure", type=str2bool, default=True)
    parser.add_argument(
        "--table_char_dict_path",
        type=str,
        default="../ppocr/utils/dict/table_structure_dict_ch.txt",
    )
    # params for layout
    parser.add_argument("--layout_model_dir", type=str)
    parser.add_argument(
        "--layout_dict_path",
        type=str,
        default="../ppocr/utils/dict/layout_dict/layout_publaynet_dict.txt",
    )
    parser.add_argument(
        "--layout_score_threshold", type=float, default=0.5, help="Threshold of score."
    )
    parser.add_argument(
        "--layout_nms_threshold", type=float, default=0.5, help="Threshold of nms."
    )
    # params for kie
    parser.add_argument("--kie_algorithm", type=str, default="LayoutXLM")
    parser.add_argument("--ser_model_dir", type=str)
    parser.add_argument("--re_model_dir", type=str)
    parser.add_argument("--use_visual_backbone", type=str2bool, default=True)
    parser.add_argument(
        "--ser_dict_path", type=str, default="../train_data/XFUND/class_list_xfun.txt"
    )
    # need to be None or tb-yx
    parser.add_argument("--ocr_order_method", type=str, default=None)
    # params for inference
    parser.add_argument(
        "--mode",
        type=str,
        choices=["structure", "kie"],
        default="structure",
        help="structure and kie is supported",
    )
    parser.add_argument(
        "--image_orientation",
        type=bool,
        default=False,
        help="Whether to enable image orientation recognition",
    )
    parser.add_argument(
        "--layout",
        type=str2bool,
        default=True,
        help="Whether to enable layout analysis",
    )
    parser.add_argument(
        "--table",
        type=str2bool,
        default=True,
        help="In the forward, whether the table area uses table recognition",
    )
    parser.add_argument(
        "--ocr",
        type=str2bool,
        default=True,
        help="In the forward, whether the non-table area is recognition by ocr",
    )
    # param for recovery
    parser.add_argument(
        "--recovery",
        type=str2bool,
        default=False,
        help="Whether to enable layout of recovery",
    )
    parser.add_argument(
        "--use_pdf2docx_api",
        type=str2bool,
        default=False,
        help="Whether to use pdf2docx api",
    )
    parser.add_argument(
        "--invert",
        type=str2bool,
        default=False,
        help="Whether to invert image before processing",
    )
    parser.add_argument(
        "--binarize",
        type=str2bool,
        default=False,
        help="Whether to threshold binarize image before processing",
    )
    parser.add_argument(
        "--alphacolor",
        type=str2int_tuple,
        default=(255, 255, 255),
        help="Replacement color for the alpha channel, if the latter is present; R,G,B integers",
    )

    return parser
