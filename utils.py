import dateutil.parser as parser
from datetime import datetime

def datetime_handler(iso_date):
    """
    Convert ISO date format to human-readable format.
    
    Args:
        iso_date (datetime): The ISO date to be formatted.
    
    Returns:
        str: The formatted date and time.
    
    Raises:
        TypeError: If the input is not a datetime object.
    """
    try:
        if isinstance(iso_date, datetime):
            # Convert datetime object to string in the desired format
            formatted_time = iso_date.strftime("%Y-%m-%d %H:%M:%S")
            # Parse the formatted string to handle timezones
            parsed_time = parser.parse(formatted_time)
            return str(parsed_time)
        else:
            raise TypeError("Input is not a datetime object")
    except Exception as e:
        print(f"An error occurred while formatting the datetime: {str(e)}")
        raise

