######################################################################
# business_card_interface.py
# 
# Abstract classes for the program that parses the results of the
# optical character recognition (OCR) component
# in order to extract the name, phone number, and email address
# from the processed business card image
######################################################################

from abc import ABCMeta, abstractmethod

class IContactInfo(metaclass=ABCMeta):
    @abstractmethod
    def getName(self):
        pass

    @abstractmethod
    def getPhoneNumber(self):
        pass

    @abstractmethod
    def getEmailAddress(self):
        pass

class IBusinessCardParser(metaclass=ABCMeta):
    @abstractmethod
    def getContactInfo(self, document):
        pass
