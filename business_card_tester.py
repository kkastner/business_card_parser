######################################################################
# business_card_tester.py
# 
# Program that tests the ContactInfo and BusinessCardParser classes
# from business_card_filter.py
#
# usage: python business_card_tester.py <inputfile1> <inputfile2> ...
######################################################################

import sys
from business_card_filter import ContactInfo, BusinessCardParser

def main():
    if len(sys.argv) < 2:
        print("usage: python "+sys.argv[0]+" <inputfile1> <inputfile2> ...")
        sys.exit()
    bcp = BusinessCardParser()
    for i in range(1,len(sys.argv)):
        filename = sys.argv[i]
        print("------------------------")
        print(filename)
        with open(filename, 'r') as myfile:
            data=myfile.read()
            ci = bcp.getContactInfo(data)
            print("Name: " + ci.getName())
            print("Phone: " + ci.getPhoneNumber())
            print("Email: " + ci.getEmailAddress())

if __name__ == "__main__":
    main()