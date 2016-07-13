This package contains a program that parses the results of the
optical character recognition (OCR) component
in order to extract the name, phone number, and email address
from the processed business card image.

Prerequisites:

  Python2.6+ to allow use of the Abstract Base Classes (abc) module


There are three python files, three example business card input files, and three .csv files included,
and what they each contain are given:

  business_card_interface.py - abstract classes that are used by business_card_filter.py
  business_card_filter.py - defined classes for the business card parser
  business_card_tester.py - main function to run the program with the business card files given as input
  business_card_input1.txt - example business card 1
  business_card_input2.txt - example business card 2
  business_card_input3.txt - example business card 3
  CSV_Database_of_First_Names.csv - List of first names of people in the US
  List_of_US_companies.csv - List of US company names
  List_of_occupations.csv - List of occupations worldwide

In order to run the program, the following should be run on the command line:

  python business_card_tester.py <inputfile1> <inputfile2> ...

where the inputfiles each contain a business card to be parsed. 

For example, to run the program with all three example business cards, use the following line:

  python business_card_tester.py business_card_input1.txt business_card_input2.txt business_card_input3.txt

Program highlights/restrictions:

  The business cards are assumed to be in a line-by-line layout where each line represents some basic info,
for example one line will have the name and another will have the email. It should be noted that these
lines can be in any order.
  Multiple phone numbers and email addresses can be given on a single line with anything before and after each,
but only the first one (of each) will be returned. If multiple phone numbers and email addresses are given
on multiple lines, then the program will take the first one (of each) given with the tag "office", "work",
or "main" as this program is intended for business purposes. Currently, the program will return a 1-3 digit
international code, if given, but it assumes a US-style phone number which contains a 3 digit area code,
followed by a 3, then a 4 digit phone number, with any or no separators in between. It also can accept an extension of any length, though this number is not returned.
  Names are assumed to not have any numbers, so any lines that contain numbers are ignored
to improve efficiency and performance. All possible name lines are searched and the line with the lowest
penalty is given as the employee's name. Lines that have words
that are found in companies or occupations are penalized based on the frequency that the word is found
(e.g. "corporation" and "company" are very common parts of company names and lines containing these words
are thus heavily penalized). Lines that contain first names are given a reduced penalty of -50 to help
promote the line as being the name of the employee. Last names were not used to reduce penalty as this dataset
was significantly larger. All company and name lists used are located in the US.
  BusinessCardParser when first created reads in the three provided .csv files and prepares them to be used
for the name portion of the program. This is done so that this process only needs to be done once, even when
processing multiple business cards.
