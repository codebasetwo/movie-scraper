import re
from datetime import datetime


DATE_REGEX = r'\w+\s\d{1,2},\s\d{4}|\d{1,2}\s\w+\s\d{4}|\d{4}'
AMOUNTS = r"thousand|million|billion"
NUMBER = r"\d+(,\d{3})*\.*\d*"
STANDARD = fr"\${NUMBER}(-|\sto\s)?({NUMBER})?\s({AMOUNTS})"

def word_to_value(word):
	value_dict = {"thousand": 1000, "million": 1000000, "billion": 1000000000}
	return value_dict.get(word.lower(), 1)

def parse_word(string):
	word = re.search(NUMBER, string).group()
	value = float(word.replace(",", ""))
	modifier = word_to_value(re.search(AMOUNTS, string, flags=re.I).group())
	return value*modifier

def parse_value(string):
	# Strip commas to pass it to float
	string = re.search(NUMBER, string).group()
	string = float(string.replace(",", ""))
	return float(string)

def money_conversion(money):
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
	formats = ['%d %B %Y', '%B %d, %Y', '%Y']
	for fmt in formats:
		try:
			return datetime.strptime(date_string, fmt)
		except ValueError:
			continue


def clean_date(value):
    if isinstance(value, list) and len(value) > 1:
        # Get release date for US
        value = value[1]
    else:
        value = value[0]

    string = re.search(DATE_REGEX, value).group()
    return string