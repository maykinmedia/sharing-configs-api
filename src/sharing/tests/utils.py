from .factories import ClientAuthFactory


class TokenAuthMixin:
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.client_auth = ClientAuthFactory(
            organization="testsuite", email="test@letmein.nl"
        )

    def setUp(self):
        super().setUp()

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.client_auth.token}")
