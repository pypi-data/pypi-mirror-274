import re
from flexidata.utils.constants import Patterns
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from functools import wraps
from nltk import pos_tag
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from flexidata.Logger import Logger

logger = Logger()


def ensure_nltk_package(package_category, package_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # Try to find the package
                nltk.find(f"{package_category}/{package_name}")
            except LookupError:
                # If not found, download the package
                print(f"{package_name} not found, downloading now...")
                nltk.download(package_name)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@ensure_nltk_package('tokenizers', 'punkt')
def tokenize_sentences(text):
    """
    Tokenizes the given text into sentences.
    
    Parameters:
    text (str): The text to tokenize into sentences.
    
    Returns:
    list: A list of sentences extracted from the text.
    
    Example:
    >>> sample_text = "Hello world. This is an example sentence. Short here."
    >>> tokenize_sentences(sample_text)
    ['Hello world. ', 'This is an example sentence.', 'Short here.']
    """
    return sent_tokenize(text)

@ensure_nltk_package('tokenizers','punkt')
def tokenize_words(text):
    """
    Tokenizes the input text into words using NLTK's word_tokenize.
    
    Parameters:
    text (str): The text to be tokenized into words.
    
    Returns:
    list: A list of words and punctuation from the text.
    
    Example:
    >>> sample_text = "Hello, world! This is an example."
    >>> tokenize_words(sample_text)
    ['Hello', ',', 'world', '!', 'This', 'is', 'an', 'example', '.']
    """
    return word_tokenize(text)

def no_of_sentence(text, min_word_length):
    count = 0
    sentences = tokenize_sentences(text)
    for sentence in sentences:
        words = [word for word in tokenize_words(sentence) if word != "."]
        if len(words) < min_word_length:
            continue
        count = count + 1
    return count


def is_title(text, title_max_word_length=12, sentence_min_word_length=5):
    """
    Determines whether the provided text can be classified as a title based on several criteria.
    
    This function assesses the given text to decide if it fits the characteristics commonly
    associated with titles. It evaluates conditions such as text length, numeric content,
    punctuation, and word count to make this determination.

    Parameters:
    - text (str): The text to evaluate.
    - title_max_word_length (int): Optional. The maximum number of words a title can
      have to still be considered a title. Defaults to 12.
    
    Returns:
    - bool: True if the text is likely a title, otherwise False.

    Examples:
    >>> is_title("Chapter 1: An Introduction")
    False
    >>> is_title("Introduction to Programming")
    True
    >>> is_title("12345")
    False
    >>> is_title("This is an excessively long sentence that should not be considered a title")
    False

    Logic:
    - Returns False if the text is empty.
    - Returns False if the text is numeric.
    - Returns False if the text is determined to be numeric using the TextType.numeric_text.
    - Returns False if the text ends with a punctuation mark, which is checked using
      TextType.ends_with_punctuation.
    - Returns False if the text ends with a comma.
    - Returns False if the text contains more words than `title_max_word_length`.
    
    If none of the above conditions are met, the text is likely a title, and True is returned.
    """
    if len(text) == 0:
        return False
    if text.isnumeric() or TextType.numeric_text(text):
        return False
    if TextType.ends_with_punctuation(text):
        return False
    
    try:
        if detect(text) != 'en':
            return False
    except LangDetectException as e:
        logger.info(f"LangDetectException: {e}")
        return False
    
    if text.endswith(","):
        return False
    if len(text.split(" ")) > title_max_word_length:
        return False
    if no_of_sentence(text, sentence_min_word_length) > 1:
        return False
    
    return True


def is_list_item(text):
    return bool(Patterns.LIST_ITEM_REGEX.match(text))

@ensure_nltk_package("taggers", "averaged_perceptron_tagger")
def narrative_features(text, check_pronouns=False, check_temporal=False):
    sentences = tokenize_sentences(text.lower())
    verb_count = 0
    first_person_pronouns_count = 0
    temporal_words_count = 0
    first_person_pronouns = {'i', 'we', 'us', 'our', 'ours', 'myself', 'ourselves'}
    temporal_words = {'then', 'after', 'before', 'finally', 'previously', 'formerly'}

    for sentence in sentences:
        tokens = tokenize_words(sentence)
        tagged_tokens = pos_tag(tokens)

        for word, tag in tagged_tokens:
            if tag.startswith('VB'):  # Any form of verb
                verb_count += 1
            if check_pronouns:
                first_person_pronouns_count += sum(1 for word, _ in tagged_tokens if word.lower() in first_person_pronouns)

            if check_temporal:
                temporal_words_count += sum(1 for word, _ in tagged_tokens if word.lower() in temporal_words)

    is_narrative = verb_count > 0
    if check_pronouns:
        is_narrative = is_narrative and first_person_pronouns_count > 0
    if check_temporal:
        is_narrative = is_narrative and temporal_words_count > 0

    return is_narrative

def is_narrative_text(text):

    if len(text) == 0:
        return False
    
    if text.isnumeric() or TextType.numeric_text(text):
        return False
    try:
        if detect(text) != 'en':
            return False
    except LangDetectException as e:
        logger.info(f"LangDetectException: {e}")
        return False

    if no_of_sentence(text, 3) < 2 and (not narrative_features(text)):
        return False

    return True



class TextType:
    """
    Provides classification of text into predefined categories based on specific characteristics.

    This class is designed to classify texts as titles, list items, or other types based on
    patterns and functions that check for specific attributes in the text. It utilizes regular
    expressions to determine if text ends with punctuation or is numeric, supporting text
    analysis and processing tasks.

    Attributes:
        TITLE_TYPE (str): Represents a text identified as a title.
        LIST_ITEM (str): Represents a text identified as a list item.
        UNKNOWN (str): Default type when text does not match any specific category.

    Methods:
        find_text_type(text): Determines the type of the given text by checking against
                              predefined criteria for list items and titles. Returns 'Unknown'
                              if the text does not meet any specific criteria.
        ends_with_punctuation(text): Checks if the text ends with a punctuation mark.
                                     Returns True if it does, False otherwise.
        numeric_text(text): Determines if the text is numeric. Returns True if it is,
                            False otherwise.

    Example usage:
        >>> TextType.find_text_type("Chapter 1: Introduction")
        'Title'
        >>> TextType.ends_with_punctuation("Hello, world!")
        True
        >>> TextType.numeric_text("1234")
        True
    """

    EMAILL_TYPE = "Email"
    TITLE_TYPE = "Title"
    LIST_ITEM = "ListItem"
    NERATIVE_TEXT = "NerativeText"
    UNKNOWN = "Unknown"

    @staticmethod
    def find_text_type(text):
        """
        Determines the type of the given text by evaluating it against predefined criteria for list items and titles.

        This method classifies text as a list item, title, or unknown based on specific checks performed by
        helper functions (`is_list_item` and `is_title`). It sequentially tests each condition and returns
        the corresponding text type upon the first match.

        Parameters:
        - text (str): The text whose type is to be determined.

        Returns:
        - str: The determined type of the text. It can be 'ListItem' if the text qualifies as a list item,
            'Title' if it qualifies as a title, or 'Unknown' if it does not meet any specific criteria.

        Examples:
        >>> TextType.find_text_type("1. Introduction")
        'ListItem'
        >>> TextType.find_text_type("Introduction to Python")
        'Title'
        >>> TextType.find_text_type("This text does not fit any known category.")
        'Unknown'

        The method uses the following logic:
        - First, it checks if the text is a list item using `is_list_item`. If true, it returns 'ListItem'.
        - If the first check fails, it checks if the text is a title using `is_title`. If true, it returns 'Title'.
        - If all checks fail, it returns 'Unknown'.
        """
        if is_list_item(text):
            return TextType.LIST_ITEM
        elif is_narrative_text(text):
            return TextType.NERATIVE_TEXT
        elif is_title(text):
            return TextType.TITLE_TYPE
        else:
            return TextType.UNKNOWN

        
        
    @staticmethod
    def ends_with_punctuation(text):
        ends_in_punct_pattern = re.compile(Patterns.END_WITH_PUNCTUATION)
        return bool(ends_in_punct_pattern.search(text))

    @staticmethod
    def numeric_text(text):
        numeric_text_pattern = re.compile(Patterns.NUMERIC_REGEX)
        return bool(numeric_text_pattern.search(text))
    