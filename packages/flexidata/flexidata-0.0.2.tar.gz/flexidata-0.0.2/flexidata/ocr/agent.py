from typing import Type
from flexidata.utils.constants import OCREngine

# Define a map from OCR engine enum values to their corresponding class paths.
engine_map = {
    OCREngine.TESSERACT: "flexidata.ocr.tesseract.TesseractOCR",
    OCREngine.PADDLE: "flexidata.ocr.paddle.CustomPaddleOCR",
    OCREngine.GOOGLE_VISION: "flexidata.ocr.google_vision.GoogleVisionOCR",
}

def get_ocr_agent(engine: OCREngine = OCREngine.TESSERACT) -> Type:
    """
    Dynamically imports and returns an OCR agent class based on the specified engine.

    The function looks up the class path from the `engine_map` dictionary using the provided
    `engine` parameter. It then dynamically imports the module and retrieves the class
    by name to instantiate and return an instance of the class.

    Args:
        engine (OCREngine): The OCR engine type from the OCREngine enumeration.

    Returns:
        An instance of the OCR agent class corresponding to the specified engine.

    Raises:
        ValueError: If the specified engine is not supported.
        ImportError: If there's an issue importing the required OCR module.
    """
    try:
        # Split the fully qualified class name to module and class name
        module_path, class_name = engine_map[engine].rsplit('.', 1)
        print(f"module_path={module_path} class_name={class_name}")
        # Dynamically import the module containing the OCR class
        module = __import__(module_path, fromlist=[class_name])
        # Create and return an instance of the OCR class
        return getattr(module, class_name)()
    except KeyError:
        raise ValueError(f"Unsupported OCR engine: {engine}")
    except ImportError as e:
        raise ImportError(f"Could not import the required OCR module: {e}")

