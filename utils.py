"""
Utility functions for the subscription manager.

This module contains helper functions for date formatting, validation,
and other common operations used throughout the application.
"""

import re
from datetime import datetime, date, timedelta
from typing import Optional, List, Tuple


def validate_date(date_string: str) -> bool:
    """
    Validate if a date string is in the correct format (YYYY-MM-DD).
    
    Args:
        date_string: Date string to validate
        
    Returns:
        bool: True if date is valid, False otherwise
    """
    if not date_string:
        return False
    
    # Check format with regex
    date_pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(date_pattern, date_string):
        return False
    
    try:
        # Try to parse the date
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def format_date(date_string: str, input_format: str = '%Y-%m-%d', output_format: str = '%B %d, %Y') -> str:
    """
    Format a date string from one format to another.
    
    Args:
        date_string: Date string to format
        input_format: Format of the input date string
        output_format: Desired output format
        
    Returns:
        str: Formatted date string
        
    Raises:
        ValueError: If date string is invalid
    """
    try:
        date_obj = datetime.strptime(date_string, input_format)
        return date_obj.strftime(output_format)
    except ValueError as e:
        raise ValueError(f"Invalid date format: {e}")


def calculate_days_until_renewal(renewal_date: str) -> int:
    """
    Calculate the number of days until a renewal date.
    
    Args:
        renewal_date: Renewal date in YYYY-MM-DD format
        
    Returns:
        int: Number of days until renewal (negative if past due)
    """
    if not validate_date(renewal_date):
        raise ValueError("Invalid renewal date format")
    
    try:
        renewal = datetime.strptime(renewal_date, '%Y-%m-%d').date()
        today = date.today()
        
        # Calculate the next renewal date
        current_year = today.year
        renewal_this_year = renewal.replace(year=current_year)
        
        # If the renewal date has passed this year, use next year
        if renewal_this_year < today:
            renewal_this_year = renewal.replace(year=current_year + 1)
        
        delta = renewal_this_year - today
        return delta.days
    except ValueError as e:
        raise ValueError(f"Error calculating days until renewal: {e}")


def get_current_date_string() -> str:
    """
    Get current date as a string in YYYY-MM-DD format.
    
    Returns:
        str: Current date string
    """
    return date.today().strftime('%Y-%m-%d')


def parse_cost(cost_string: str) -> float:
    """
    Parse a cost string and return a float value.
    
    Args:
        cost_string: Cost string (e.g., "19.99", "$19.99", "19,99")
        
    Returns:
        float: Parsed cost value
        
    Raises:
        ValueError: If cost string cannot be parsed
    """
    if not cost_string:
        raise ValueError("Cost string cannot be empty")
    
    # Remove currency symbols and spaces
    cleaned = re.sub(r'[$€£¥₹\s]', '', cost_string.strip())
    
    # Handle comma as decimal separator (European format)
    if ',' in cleaned and '.' not in cleaned:
        cleaned = cleaned.replace(',', '.')
    # Handle comma as thousands separator
    elif ',' in cleaned and '.' in cleaned:
        # Remove commas (thousands separators)
        cleaned = cleaned.replace(',', '')
    
    try:
        return float(cleaned)
    except ValueError:
        raise ValueError(f"Invalid cost format: {cost_string}")


def format_currency(amount: float, currency_symbol: str = "$") -> str:
    """
    Format a float amount as currency string.
    
    Args:
        amount: Amount to format
        currency_symbol: Currency symbol to use
        
    Returns:
        str: Formatted currency string
    """
    return f"{currency_symbol}{amount:.2f}"


def validate_subscription_name(name: str) -> bool:
    """
    Validate subscription name.
    
    Args:
        name: Name to validate
        
    Returns:
        bool: True if name is valid, False otherwise
    """
    if not name or not name.strip():
        return False
    
    # Check for reasonable length
    if len(name.strip()) < 2 or len(name.strip()) > 100:
        return False
    
    return True


def validate_category(category: str) -> bool:
    """
    Validate subscription category.
    
    Args:
        category: Category to validate
        
    Returns:
        bool: True if category is valid, False otherwise
    """
    if not category or not category.strip():
        return False
    
    # Check for reasonable length
    if len(category.strip()) < 2 or len(category.strip()) > 50:
        return False
    
    return True


def validate_payment_method(payment_method: str) -> bool:
    """
    Validate payment method.
    
    Args:
        payment_method: Payment method to validate
        
    Returns:
        bool: True if payment method is valid, False otherwise
    """
    if not payment_method or not payment_method.strip():
        return False
    
    # Check for reasonable length
    if len(payment_method.strip()) < 2 or len(payment_method.strip()) > 50:
        return False
    
    return True


def get_common_categories() -> List[str]:
    """
    Get a list of common subscription categories.
    
    Returns:
        List[str]: List of common categories
    """
    return [
        "Streaming",
        "Music",
        "Software",
        "Cloud Storage",
        "News & Media",
        "Gaming",
        "Fitness",
        "Education",
        "Productivity",
        "Security",
        "Communication",
        "Other"
    ]


def get_common_payment_methods() -> List[str]:
    """
    Get a list of common payment methods.
    
    Returns:
        List[str]: List of common payment methods
    """
    return [
        "Credit Card",
        "Debit Card",
        "PayPal",
        "Bank Transfer",
        "Apple Pay",
        "Google Pay",
        "Cryptocurrency",
        "Other"
    ]


def truncate_string(text: str, max_length: int = 30) -> str:
    """
    Truncate a string to a maximum length with ellipsis.
    
    Args:
        text: Text to truncate
        max_length: Maximum length of the result
        
    Returns:
        str: Truncated string with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - 3] + "..."


def format_table_row(data: List[str], widths: List[int]) -> str:
    """
    Format a row of data for table display.
    
    Args:
        data: List of strings to format
        widths: List of column widths
        
    Returns:
        str: Formatted table row
    """
    if len(data) != len(widths):
        raise ValueError("Data and widths lists must have the same length")
    
    formatted_cells = []
    for i, (cell, width) in enumerate(zip(data, widths)):
        # Truncate if too long
        if len(cell) > width:
            cell = truncate_string(cell, width)
        
        # Pad with spaces
        formatted_cells.append(cell.ljust(width))
    
    return " | ".join(formatted_cells)


def get_date_range_days(start_date: str, end_date: str) -> int:
    """
    Calculate the number of days between two dates.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        
    Returns:
        int: Number of days between dates
    """
    if not validate_date(start_date) or not validate_date(end_date):
        raise ValueError("Invalid date format")
    
    start = datetime.strptime(start_date, '%Y-%m-%d').date()
    end = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    return (end - start).days


def is_date_in_range(check_date: str, start_date: str, end_date: str) -> bool:
    """
    Check if a date falls within a given range.
    
    Args:
        check_date: Date to check in YYYY-MM-DD format
        start_date: Start of range in YYYY-MM-DD format
        end_date: End of range in YYYY-MM-DD format
        
    Returns:
        bool: True if date is in range, False otherwise
    """
    if not all(validate_date(d) for d in [check_date, start_date, end_date]):
        raise ValueError("Invalid date format")
    
    check = datetime.strptime(check_date, '%Y-%m-%d').date()
    start = datetime.strptime(start_date, '%Y-%m-%d').date()
    end = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    return start <= check <= end


# TODO: Fix bug: sorting renewals by date sometimes fails if format changes
# TODO: Improve CLI with colored output using rich
# TODO: Add Export to Excel (XLSX) feature
