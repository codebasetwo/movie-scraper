import pytest
import datetime
from utils.conversion import money_conversion, parse_date_string, clean_date


def test_standard():
	assert money_conversion("$3 million") == 3000000

def test_standard_double_digit():
	assert money_conversion("$99 million") == 99000000

def test_standard_with_decimal():
	assert money_conversion("$3.5 million") == 3500000

def test_standard_multiple_decimals():
	assert money_conversion("$1.234 million") == 1234000

def test_standard_billion():
	assert money_conversion("$1.25 billion") == 1250000000

def test_standard_thousand():
	assert money_conversion("$900.9 thousand") == 900900

def test_range():
	assert money_conversion("$3.5-4 million") == 3500000

def test_range_with_to():
	assert money_conversion("$3.5 to 4 million") == 3500000

def test_number():
	assert money_conversion("$950000") == 950000

def test_number_with_commas():
	assert money_conversion("$127,850,000") == 127850000

def test_number_with_commas_and_decimals():
	assert money_conversion("$10,000,000.50") == 10000000.5

def test_number_with_commas_middle():
	assert money_conversion("estimated $5,000,000 (USD)") == 5000000

def test_other_currency():
	assert money_conversion("60 million Norwegian Kroner (around $8.7 million in 1989)") == 8700000

def test_list():
	assert money_conversion(['$410.6 million (gross)', '$378.5 million (net)']) == 410600000

def test_unkown():
	assert money_conversion("70 crore") is None

def test_date_dmy():
	assert parse_date_string("24 July 2024") == datetime.datetime.strptime("24 July 2024", '%d %B %Y')

def test_date_mdy():
	assert parse_date_string("July 24, 2024") == datetime.datetime.strptime("July 24, 2024", '%B %d, %Y')

def test_date_year():
	assert parse_date_string("2024") == datetime.datetime.strptime("2024", '%Y')

def test_date_zero_index():
	assert clean_date(['November 13, 1940']) == 'November 13, 1940'

def test_dates():
	assert clean_date(["August 24, 1942 (Rio de Janeiro)",
							"February 6, 1943 (Boston)",
							"February 19, 1943 (United States)"
					]) == "February 6, 1943"
	
def test_date_string_year():
	assert clean_date(["1948"]) == "1948"