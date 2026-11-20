import random
from enum import StrEnum

import bson
from faker import Faker

from models.base_factory import BaseFactory

fake = Faker("en_GB")


class PaymentProviders(StrEnum):
    WORLDPAY = "WorldPay"
    ACCESS_PAYSUITE = "Access PaySuite"
    CIVICA = "Civica"
    NORTHGATE = "Northgate"


class AccessPaySuiteAcceptedPaymentType:
    def __init__(self):
        self.visa = fake.boolean()
        self.debit = fake.boolean()
        self.mastercard = fake.boolean()
        self.maestro = fake.boolean()
        self.electron = fake.boolean()
        self.mail_or_telephone_order = fake.boolean()

    def to_json(self):
        return {
            "visa": self.visa,
            "delt": self.debit,
            "mcrd": self.mastercard,
            "msto": self.maestro,
            "elec": self.electron,
            "moto": self.mail_or_telephone_order,
        }


class PaymentAccount:
    def __init__(self):
        self.account_id = bson.ObjectId()
        self.name = f"{fake.word().capitalize()} Licensing Account"
        self.provider_specific_code_a = fake.bothify(text="CODE-A-####")
        self.provider_specific_code_b = fake.bothify(text="CODE-B-####")
        self.provider_specific_code_c = fake.bothify(text="CODE-C-####")
        self.provider_specific_code_d = fake.bothify(text="CODE-D-####")

    def to_json(self):
        return {
            "acc_id": self.account_id,
            "name": self.name,
            "codeA": self.provider_specific_code_a,
            "codeB": self.provider_specific_code_b,
            "codeC": self.provider_specific_code_c,
            "codeD": self.provider_specific_code_d,
        }


class AuthorityPaymentAccount:
    def __init__(self, authority_url_slug: str | None = None):
        self.authority_url_slug = authority_url_slug or fake.slug()
        self.payment_provider = random.choice(list(PaymentProviders)).value
        self.accounts = [PaymentAccount() for _ in range(random.randint(1, 3))]
        self.merchant_id = fake.bothify(text="MERCH-######")
        self.provider_shared_secret = fake.sha256()[:32]
        self.provider_shared_post_salt = fake.sha256()[:16]
        self.civica_payment_form_url = fake.url()
        self.civica_payment_verify_url = fake.url()
        self.use_icon_security = fake.boolean()
        self.icon_security_auth_username = fake.user_name()
        self.icon_security_auth_password = fake.password()
        self.payment_security_domain = fake.domain_name()
        self.basic_auth_username = fake.user_name()
        self.basic_auth_password = fake.password()
        self.mac_secret_key = fake.sha256()[:32]
        self.callback_override_url = fake.url()
        self.send_test_payment = fake.boolean()
        self.access_pay_suite_accepted_cards = AccessPaySuiteAcceptedPaymentType()
        self.worldpay_md5_shared_secret = fake.md5()

    def to_json(self):
        return {
            "authorityUrlSlug": self.authority_url_slug,
            "paymentProvider": self.payment_provider,
            "accounts": [account.to_json() for account in self.accounts],
            "merchantId": self.merchant_id,
            "providerSharedSecret": self.provider_shared_secret,
            "providerSharedPostSalt": self.provider_shared_post_salt,
            "paymentUrl": self.civica_payment_form_url,
            "paymentVerifyUrl": self.civica_payment_verify_url,
            "useIconSecurity": self.use_icon_security,
            "paymentUserName": self.icon_security_auth_username,
            "paymentPassword": self.icon_security_auth_password,
            "paymentSecurityDomain": self.payment_security_domain,
            "username2": self.basic_auth_username,
            "password2": self.basic_auth_password,
            "macSecretKey": self.mac_secret_key,
            "callbackOverride": self.callback_override_url,
            "sendTestPayment": self.send_test_payment,
            "accessPaySuiteAcceptedCards": self.access_pay_suite_accepted_cards.to_json(),
            "worldpayMd5SharedSecret": self.worldpay_md5_shared_secret,
        }


class AuthorityPaymentAccountFactory(BaseFactory):
    collection_name = "paymentAccounts"
    model = AuthorityPaymentAccount
