import base64
import random

from faker import Faker
from pymongo import MongoClient

fake = Faker("en_GB")


class AuthorityContactDetailsHolder:
    def __init__(self):
        fake.address()
        self.line_one = f"{fake.building_number()} {fake.street_name()}"
        self.line_two = fake.secondary_address()
        self.line_3 = ""
        self.city = fake.city()
        self.postcode = fake.postcode()
        self.phone_number = fake.phone_number()
        self.email_address = fake.email()

    def to_json(self):
        return {
            "lineOne": self.line_one,
            "lineTwo": self.line_two,
            "line3": self.line_3,
            "city": self.city,
            "postCode": self.postcode,
            "phoneNumber": self.phone_number,
            "emailAddress": self.email_address,
        }


class Licence:
    def __init__(self):
        self.licence_code = fake.numerify(text="####-#-#")
        self.offered_by_authority = True
        self.using_gov_uk = True
        self.local_authority_url = fake.url()

    def to_json(self):
        return {
            "licenceCode": self.licence_code,
            "offeredByAuthority": self.offered_by_authority,
            "usingGovUk": self.using_gov_uk,
            "localAuthorityUrl": self.local_authority_url,
        }


class LocalAuthority:
    def __init__(
        self,
    ):
        self.agency_id = fake.random_int()
        self.authority_contact_details_holder = AuthorityContactDetailsHolder()
        self.countries = random.choice(["England", "Wales", "NI", "Scotland"])
        self.full_name = fake.county()
        self.image_base_64_encoded = base64.b64encode(fake.binary(length=32)).decode("utf-8")
        self.licence_details = Licence()
        self.snac_codes = fake.hexify(text="^^^^", upper=True)

    def to_json(self):
        return {
            "agencyId": self.agency_id,
            "authorityContactDetailsHolder": self.authority_contact_details_holder.to_json(),
            "countries": [self.countries],
            "fullName": self.full_name,
            "imageBase64encoded": self.image_base_64_encoded,
            "licenceDetails": [self.licence_details.to_json()],
            "name": self.full_name,
            "snacCodes": [self.snac_codes],
            "urlSlug": self.full_name.lower(),
        }


class LocalAuthorityFactory:
    def __init__(self, db_url: str):
        self._client = MongoClient(db_url)
        self._database = self._client.get_default_database()["authorities"]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._client.close()

    def create_x(self, x: int) -> list[LocalAuthority]:
        local_authorities_created = []
        for _ in range(x):
            local_authority = LocalAuthority()
            self._database.insert_one(local_authority.to_json())
            local_authorities_created.append(local_authority)

        return local_authorities_created
