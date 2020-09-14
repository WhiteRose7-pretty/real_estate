import pickle
from dashboard.models import RealEstate


class Property:
    def __init__(self, photo, type, pets, beds, baths, price, address, zip_code, link):
        self.photo = photo
        self.type = type
        self.pets = pets
        self.beds = beds
        self.baths = baths
        self.price = price
        self.address = address
        self.zip_code = zip_code
        self.link = link


with open('property_CA_1.txt', "rb+") as fp:
    aa = pickle.load(fp)

    for item in aa:
        pass

