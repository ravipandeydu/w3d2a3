"""String tools for the tool-enhanced reasoning script."""

def count_vowels(text):
    """Count the number of vowels in a text.
    
    Args:
        text (str): The text to count vowels in
        
    Returns:
        int: The number of vowels in the text
    """
    vowels = "aeiouAEIOU"
    return sum(1 for char in text if char in vowels)

def count_letters(text):
    """Count the number of letters in a text.
    
    Args:
        text (str): The text to count letters in
        
    Returns:
        int: The number of letters in the text
    """
    return sum(1 for char in text if char.isalpha())

def count_words(text):
    """Count the number of words in a text.
    
    Args:
        text (str): The text to count words in
        
    Returns:
        int: The number of words in the text
    """
    return len(text.split())