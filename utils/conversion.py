import re
from datetime import datetime


DATE_REGEX = r'\w+\s\d{1,2},\s\d{4}|\d{1,2}\s\w+\s\d{4}|\d{4}'
AMOUNTS = r"thousand|million|billion"
NUMBER = r"\d+(,\d{3})*\.*\d*"
STANDARD = fr"\${NUMBER}(-|\sto\s)?({NUMBER})?\s({AMOUNTS})"

def word_to_value(word):
	"""
    Convert a word representing a large number to its corresponding numeric value.

    Parameters:
    	word (str): The word to convert.

    Returns:
    	int: The numeric value corresponding to the word.
    """
	value_dict = {"thousand": 1000, "million": 1000000, "billion": 1000000000}
	return value_dict.get(word.lower(), 1)

def parse_word(string):
	"""
    Parse a string containing a number and a word modifier (like 'million').

    Parameters:
    	string (str): The string to parse.

    Returns:
    	float: The numeric value after applying the modifier.
    """
	word = re.search(NUMBER, string).group()
	value = float(word.replace(",", ""))
	modifier = word_to_value(re.search(AMOUNTS, string, flags=re.I).group())
	return value*modifier

def parse_value(string):
	"""
    Parse a string containing a numeric value.

    Parameters:
    	string (str): The string to parse.

    Returns:
    	float: The parsed numeric value.
    """
	# Strip commas to pass it to float
	string = re.search(NUMBER, string).group()
	string = float(string.replace(",", ""))
	return float(string)

def money_conversion(money):
	"""
    Convert a money string to a numeric value.

    Parameters:
    	money (str): The money string to convert.

    Returns:
    	float: The converted numeric value, or None if conversion fails.
    """
	if money == "N/A":
		return None
	
	if isinstance(money, list):
		money = money[0]

	word = re.search(STANDARD, money, flags=re.I)
	value= re.search(fr"\${NUMBER}", money)

	if word:
		return parse_word(word.group())
	elif value:
		return parse_value(value.group())
	else:
		return None

def parse_date_string(date_string):
	"""
    Parse a date string and convert it to a datetime object.

    Parameters:
		date_string (str): The date string to parse.

    Returns:
    	datetime: The parsed datetime object, or None if parsing fails.
    """    
	formats = ['%d %B %Y', '%B %d, %Y', '%Y']
	for fmt in formats:
		try:
			return datetime.strptime(date_string, fmt)
		except ValueError:
			print(f'error occured for {date_string}')
			continue


def clean_date(value):
    """
    Clean a list of date strings to extract the release date.

    Parameters:
    	value (list): The list of date strings.

    Returns:
    	str: The cleaned date string.
    """
    if isinstance(value, list) and len(value) > 1:
        # Get release date for US
        value = value[1]
    else:
        value = value[0]

    string = re.search(DATE_REGEX, value).group()

    return string