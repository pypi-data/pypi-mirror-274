from typing import Union
import numpy as np
from PIL import Image

# Ensure necessary packages are installed
from flexidata.utils.common import check_package_installed
try:
    check_package_installed('pytesseract')
    import pytesseract
except ImportError as e:
    raise ImportError(f"Failed to import pytesseract: {str(e)}") from e

class TesseractOCR:
    def __init__(self) -> None:
        """Initializes the TesseractOCR object."""
        pass

    def image_to_text(self, image: Union[Image.Image, np.ndarray], lang: str = 'eng') -> str:
        """
        Converts an image to text using Tesseract OCR, handling both PIL Image objects and numpy arrays.

        Args:
            image (Union[Image.Image, np.ndarray]): The image to be processed, which can be either
                a PIL Image object or a numpy array.
            lang (str): The language to use for OCR processing. Defaults to 'eng'.

        Returns:
            str: The extracted text from the image as a string.
        """
        # Convert numpy array to PIL Image if necessary
        if isinstance(image, np.ndarray):
            # Ensure the array is in a format suitable for conversion to an Image
            if image.ndim == 3 and image.shape[2] in [3, 4]:  # Check for 3 (RGB) or 4 (RGBA) channels
                image = Image.fromarray(image)
            else:
                raise ValueError("Unsupported numpy array shape for image conversion to PIL Image.")

        elif not isinstance(image, Image.Image):
            raise TypeError("The image must be a PIL.Image.Image or numpy.ndarray.")

        # Perform OCR using pytesseract
        return pytesseract.image_to_string(image, lang=lang)

