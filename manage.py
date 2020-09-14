#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


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


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_rama.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
