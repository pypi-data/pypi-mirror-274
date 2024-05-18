from PIL import ImageDraw
import fitz
import re

def rect_to_bbox(rect, page_height):
    """
    Converts a rectangle's coordinates from a PDF coordinate system (origin at bottom-left)
    to a more standard bounding box format (origin at top-left).

    This is useful for graphic operations that expect coordinates with the origin at the top-left,
    such as many image and graphics libraries.

    Args:
        rect (tuple): A tuple containing the coordinates of the rectangle (x1, y2, x2, y1)
                      where y2 > y1 in PDF coordinate system.
        page_height (float): The height of the PDF page, used to flip the y-coordinates.

    Returns:
        list: A list of coordinates [x1, y1, x2, y2] representing the bounding box with
              the origin at the top-left.
    """
    # Extract coordinates from the input tuple
    x1, y2, x2, y1 = rect
    
    # Convert PDF y-coordinates to top-left origin coordinates by subtracting from page height
    y1 = page_height - y1
    y2 = page_height - y2

    # Return the converted bounding box
    return [x1, y1, x2, y2]



def normalize_whitespace(text):
    """
    Normalize the whitespace in a text string.

    This function replaces non-breaking spaces and newlines with a single space and collapses
    multiple spaces into a single space.

    Args:
        text (str): The text to be normalized.

    Returns:
        str: The text with normalized whitespace.
    """
    text = re.sub(r"[\xa0\n]", " ", text)
    text = re.sub(r"([ ]{2,})", " ", text)
    return text.strip()



class PDFDebugger:
    """
    A class to handle PDF debugging operations, allowing visual inspection of elements within a PDF.
    Provides methods to highlight layout elements and save pages with debugging information.
    
    Attributes:
        debug (bool): A flag to enable or disable debugging operations.
        pages (fitz.Document): The PDF document opened with PyMuPDF (fitz).
    """

    def __init__(self, file_name, debug=False) -> None:
        """
        Initializes the PDFDebugger instance by opening a PDF file and setting the debug mode.

        Args:
            file_name (str): Path to the PDF file to be debugged.
            debug (bool): Whether to enable debugging features.
        """
        self.debug = debug  # Set the debugging flag
        self.pages = fitz.open(file_name)  # Open the PDF file with fitz

    @staticmethod
    def is_debug_enabled(method):
        """
        Decorator to check if debugging is enabled before executing a method.
        This is useful for controlling the execution of debugging-specific methods.
        
        Args:
            method (callable): The method to be wrapped by the decorator.
        
        Returns:
            callable: A wrapper function that checks the debug state before method execution.
        """
        def wrapper(self, *args, **kwargs):
            if not self.debug:
                return False  # If debugging is not enabled, do nothing
            return method(self, *args, **kwargs)  # Otherwise, execute the method
        return wrapper

    def get_page(self, page_number):
        """
        Retrieves a specific page from the PDF document.
        
        Args:
            page_number (int): The page number to retrieve (1-indexed).
        
        Returns:
            fitz.Page: The requested page object.
        """
        return self.pages[page_number - 1]  # Return the requested page, adjusting for zero-indexing

    @is_debug_enabled
    def layout_element(self, page, bbox, outline=(1, 0, 0)):
        """
        Draws a rectangle around a specified bounding box on a page if debugging is enabled.
        
        Args:
            page (fitz.Page): The page where the rectangle should be drawn.
            bbox (tuple): A tuple (x0, y0, x1, y1) specifying the bounding box coordinates.
            outline (tuple): A tuple (r, g, b) specifying the color of the rectangle outline.
        """
        x0, y0, x1, y1 = bbox  # Unpack the bounding box coordinates
        rect = fitz.Rect(x0, y0, x1, y1)  # Create a rectangle object
        page.draw_rect(rect, color=outline, width=1.5)  # Draw the rectangle on the page

    @is_debug_enabled
    def save_debug(self, file_name="debug/output.pdf"):
        """
        Saves the modified PDF document to a new file if debugging is enabled.
        
        Args:
            file_name (str): The file path where the debug version of the document will be saved.
        """
        self.pages.save(file_name)  # Save the document to the specified file


    
