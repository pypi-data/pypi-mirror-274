from flexidata.utils.common import check_package_installed
import numpy as np
from google.cloud import vision
import io
from PIL import Image

class GoogleVisionOCR:

    def __init__(self) -> None:
        self.client = vision.ImageAnnotatorClient()

    def image_to_text(self, image, lang='eng'):
        # Convert np.array to PIL Image
        pil_image = Image.fromarray(image)
    
        # Convert PIL Image to bytes
        with io.BytesIO() as output:
            pil_image.save(output, format='JPEG')
            content = output.getvalue()
    
        image = vision.Image(content=content)
    
        # Use document_text_detection instead of text_detection
        response = self.client.document_text_detection(image=image)
        texts = response.full_text_annotation
    
        result = []
        if texts:
            for page in texts.pages:
                for block in page.blocks:
                    for paragraph in block.paragraphs:
                        for word in paragraph.words:
                            word_text = ''.join([symbol.text for symbol in word.symbols])
                            vertices = [(vertex.x, vertex.y) for vertex in word.bounding_box.vertices]
                            result.append({"text": word_text, "bounding_box": vertices})
        return result