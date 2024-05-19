from typing import List, Tuple, Any
import numpy as np
from PIL import Image
import uuid
from flexidata.config.config import Config
# Ensure necessary packages are installed
from flexidata.utils.common import check_package_installed
config = Config()

try:
    check_package_installed("paddleocr")
    check_package_installed("paddle")
    from paddleocr import PaddleOCR as PaddleOCRClient, draw_ocr
    import paddle
except ImportError as e:
    raise ImportError(f"Failed to import PaddleOCR or Paddle: {str(e)}") from e

class CustomPaddleOCR:
    """
    A wrapper class for PaddleOCR to simplify its usage in text extraction from images,
    automatically handling GPU availability.

    Attributes:
        paddle_ocr (PaddleOCRClient): The PaddleOCR client configured for use.
    """

    def __init__(self, lang: str = "en") -> None:
        """
        Initializes the CustomPaddleOCR with optional language settings and determines
        if a GPU is available for use.

        Args:
            lang (str): Default language for OCR operations. Defaults to 'en' (English).
        """
        gpu_available = paddle.device.cuda.device_count() > 0
        self.paddle_ocr = PaddleOCRClient(
            use_angle_cls=True,  # Whether to use angle classifier
            use_gpu=gpu_available,  # Enable GPU if available
            lang=lang,
            show_log=False  # Disable PaddleOCR logging
        )

    def image_to_text(self, image: Image.Image, lang: str = "en") -> List[Tuple]:
        """
        Extracts text from an image using the configured PaddleOCR client.

        Args:
            image (Image.Image): The image from which to extract text.
            lang (str): The language to use for OCR. Overrides the default if specified.

        Returns:
            List[Tuple]: A list of tuples containing OCR results, including bounding boxes and text.
        """
        #Ensure image is in the correct format for PaddleOCR
        if not isinstance(image, np.ndarray):
            image = np.array(image)

        ocr_data = self.paddle_ocr.ocr(image, cls=True)
        texts = self.group_text_to_paragraphs(ocr_data)
        return texts
    
    def debug_layout(self, image, ocr_data):
        image = Image.fromarray(image).convert('RGB')
        result = ocr_data[0]
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]
        im_show = draw_ocr(image, boxes, txts, scores, font_path='/app/flexi-data/fonts/simfang.ttf')
        im_show = Image.fromarray(im_show)
        image_name = str(uuid.uuid4())
        print(f"image_name={image_name}")
        im_show.save(f'debug/paddleocr/{image_name}.jpg')


    def get_text_from_ocr_data(self, ocr_data):
        texts = []
        for index in range(len(ocr_data)):
            res = ocr_data[index]
            for line in res:
                text = line[1][0]
                if not text:
                    continue
                texts.append(text.strip())
        return texts
    
    def group_text_to_paragraphs(self, ocr_results):
        """
        Groups OCR results into paragraphs based on vertical proximity and alignment.

        Args:
            ocr_results (list): List of OCR results where each element is a tuple containing
                                the bounding box and the recognized text.

        Returns:
            list: A list of paragraphs, each paragraph is a string.
        """
        # Define a threshold for vertical distance and horizontal misalignment
        vertical_threshold = config.get("PADDLE_OCR_PARAGRAPH_VERTICAL_THRESHOLD",50)  # pixels
        horizontal_threshold = config.get("PADDLE_OCR_PARAGRAPH_HORIZONTAL_THRESHOLD",10)  # pixels

        paragraphs = []
        current_paragraph = []
        ocr_results = ocr_results[0]
        # Sort results by the top Y coordinate of the bounding box
        ocr_results.sort(key=lambda x: x[0][0][1])
        
        for index in range(len(ocr_results)):
            bbox  = ocr_results[index][0]
            text = ocr_results[index][1][0]
            if index == 0:
                current_paragraph.append(text)
            else:
                previous_bbox = ocr_results[index - 1][0]
                # Check vertical distance and horizontal alignment
                vertical_distance = bbox[0][1] - previous_bbox[0][1]
                horizontal_misalignment = abs(bbox[0][0] - previous_bbox[0][0])
                if (vertical_distance < vertical_threshold and
                        horizontal_misalignment < horizontal_threshold):
                    current_paragraph.append(text)
                else:
                    # Combine current paragraph and start a new one
                    paragraphs.append(' '.join(current_paragraph))
                    current_paragraph = [text]

        # Add the last paragraph if any
        if current_paragraph:
            paragraphs.append(' '.join(current_paragraph))

        return paragraphs
                



