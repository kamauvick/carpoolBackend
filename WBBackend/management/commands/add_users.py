import csv
from django.core.management.base import BaseCommand
from WBBackend.models import User

class Command(BaseCommand):
    """
    Add wb_users to the app from a spreadsheet.
    """

    def handle(self, *args, **options):
        data = []
        with open("wb_users.csv","r") as infile:
            c = csv.DictReader(infile)
            for r in c:
                data.append(r)

        for i in data:
            u = User.objects.filter(username=i["username"],email=i["email"]).first()
            if not u:
                if User.objects.filter(email=i["email"]).first():
                    raise Exception("User with email %s already exists"%i["email"])
                u = User(email=i["email"],username=i["username"])
            u.first_name = i["first_name"]
            u.last_name = i["last_name"]
            u.phone_number = i["phone_number"]
            u.save()
            


