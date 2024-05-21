Works only in Linux

1. install paddleocr_convert
2. https://github.com/RapidAI/PaddleOCRModelConvert
3. Download and convert the models

```bash
paddleocr_convert -p https://paddleocr.bj.bcebos.com/PP-OCRv3/english/en_PP-OCRv3_det_infer.tar -o models

paddleocr_convert -p https://paddleocr.bj.bcebos.com/PP-OCRv4/english/en_PP-OCRv4_rec_infer.tar -o models -txt_path https://github.com/PaddlePaddle/PaddleOCR/blob/960243862f6c6833f58e39f3b74864cba15edfeb/ppocr/utils/en_dict.txt

paddleocr_convert -p https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_mobile_v2.0_cls_infer.tar -o models
```
