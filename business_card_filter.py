######################################################################
# business_card_filter.py
# 
# Classes that parse the results of the
# optical character recognition (OCR) component
# in order to extract the name, phone number, and email address
# from the processed business card image
######################################################################

import re, sys
import pandas as pd
from business_card_interface import IContactInfo, IBusinessCardParser

class ContactInfo(IContactInfo):
    # regex patterns used for finding the email and phone numbers
    email_pattern = re.compile(r'([_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4}))')
    phone_pattern = re.compile(r'((\d{1,3}\D*)?\d{3}\D*\d{3}\D*\d{4})\D*(\d*)') # Last part is for the extension
    
    # Constructor for the ContactInfo class
    #  Extracts the name, email, and phone information from a given business card
    #
    # Argument 1: document: a String containing the parsed business card to extract the contact info,
    #                 separated into multiple lines
    # Argument 2: firstname_series: pandas Series containing the list of firstnames and their penalties
    # Argument 3: nonname_count: pandas Series containing the list of companies and occupations
    #                 and their penalties
    # Argument 4: stripCh: a regex string containing the characters that should be removed from the
    #                 beginning and ending of each word for each line
    def __init__(self,document,firstname_series,nonname_count,stripCh):
        self.name = ''
        self.email = ''
        self.phone = ''
        if not document:
            return  # business card info must be provided

        # Office emails/phone #s are not always given first nor last, so set a variable
        # that when one is found, then stop looking for (the respective) emails/phone #s.
        office_email = False
        office_phone = False

        possible_names = []  # List of possible lines that contain the employee's name
        for line in document.split('\n'):
            line = line.strip()
            lowercaseLine = line.lower()
            # Ignore fax numbers
            if lowercaseLine.startswith("fax"):
                continue

            # Check if line contains email address
            email_match = self.email_pattern.search(line)
            if email_match:
                if not office_email: # only add email if an office email has not yet been given
                    self.email = email_match.group(1)
                    if lowercaseLine.startswith("office") or lowercaseLine.startswith("work") or lowercaseLine.startswith("main"):
                        office_email = True
                continue   # Line contains email, so should not contain other useful info

            # Check if line contains phone number
            phone_match = self.phone_pattern.search(line)
            if phone_match:
                if not office_phone: # only add phone # if an office phone has not yet been given
                    self.phone = re.sub(r'[^0-9]','',phone_match.group(1)) # Remove all non-digit characters
                    if lowercaseLine.startswith("office") or lowercaseLine.startswith("work") or lowercaseLine.startswith("main"):
                        office_phone = True
                continue   # Line contains phone #, so should not contain other useful info

            # Valid names do not have numbers
            if bool(re.search(r'\d', line)):
                continue
            possible_names.append(line)

        minPenalty = sys.maxsize
        for possible_name in possible_names:
            penalty = 0
            for word in possible_name.split():
                word = word.strip(stripCh).lower()
                if len(word)<=1:
                    continue
                if word in nonname_count.index:  # line contains company/occupation name
                    penalty += nonname_count[word]
                if word in firstname_series.index: # line contains first name
                    penalty += firstname_series[word]
            if penalty < minPenalty:
                self.name = possible_name
                minPenalty = penalty
    
    # Returns: a String of the Employee's Full Name    
    def getName(self):
        return self.name
    
    # Returns: a String of the Employee's phone number
    def getPhoneNumber(self):
        return self.phone
    
    # Returns: a String of the Employee's email address
    def getEmailAddress(self):
        return self.email
    
class BusinessCardParser(IBusinessCardParser):
    stripCh = ',.(){}[]'
    splitPattern = r' |/'

    # Constructor for the BusinessCardParser class
    #  Prepares the pandas Series of firstnames and the pandas Series of companies/occupations to be used
    # with the ContactInfo class
    def __init__(self):
        #Prepare pandas Series of first names
        firstname_df = pd.read_csv('CSV_Database_of_First_Names.csv',header=0)
        firstname_df.drop_duplicates(inplace=True)
        firstname_df['firstname'] = firstname_df['firstname'].str.lower()
        firstname_df['penalty'] = -50
        self.firstname_series = pd.Series(firstname_df['penalty'].values,index=firstname_df['firstname'].values)
        
        #Prepare pandas Series of company and occupation information
        company_df = pd.read_csv('List_of_US_companies.csv',header=None)
        company_df.drop_duplicates(inplace=True)
        occupation_df = pd.read_csv('List_of_occupations.csv',header=None)
        occupation_df.drop_duplicates(inplace=True)
        company_list = company_df[0].values.tolist()
        occupation_list = occupation_df[0].values.tolist()
        #Combine the company and occupation lists into one list of nonnames
        nonname_list = [company_part.strip(self.stripCh).lower() for company in company_list\
                        for company_part in re.split(self.splitPattern,company)\
                        if len(company_part.strip(self.stripCh))>1]
        nonname_list += [occupation_part.strip(self.stripCh).lower() for occupation in occupation_list\
                           for occupation_part in re.split(self.splitPattern,occupation)\
                           if len(occupation_part.strip(self.stripCh))>1]
        nonname_series = pd.Series(nonname_list, name='nonname')
        self.nonname_count = nonname_series.value_counts()
        
    # Returns: an instance of the ContactInfo class
    def getContactInfo(self,document):
        return ContactInfo(document,self.firstname_series,self.nonname_count,self.stripCh)
