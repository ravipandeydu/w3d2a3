"""Math tools for the tool-enhanced reasoning script."""

def calculate_average(numbers):
    """Calculate the average of a list of numbers.
    
    Args:
        numbers (list): A list of numbers
        
    Returns:
        float: The average of the numbers
    """
    return sum(numbers) / len(numbers)

def calculate_square_root(number):
    """Calculate the square root of a number.
    
    Args:
        number (float): The number to calculate the square root of
        
    Returns:
        float: The square root of the number
    """
    return number ** 0.5

def perform_comparison(a, b, operation):
    """Compare two numbers using the specified operation.
    
    Args:
        a (float): First number
        b (float): Second number
        operation (str): The comparison operation ('>', '<', '==', '>=', '<=')
        
    Returns:
        bool: The result of the comparison
    """
    if operation == '>':
        return a > b
    elif operation == '<':
        return a < b
    elif operation == '==':
        return a == b
    elif operation == '>=':
        return a >= b
    elif operation == '<=':
        return a <= b
    else:
        raise ValueError(f"Unsupported operation: {operation}")