from typing import Type
from abc import ABC, abstractmethod


class OAuthPayload:
    """
    Concrete class to be created.
    """

    def __init__(self, provider: str):
        self.provider = provider


class OAuth(ABC):
    """
    Abstract class creating OAuthPayload.
    It uses `factory pattern` for usability.
    """

    @abstractmethod
    def make_payload(self) -> OAuthPayload:
        raise NotImplementedError


class GoogleOAuth(OAuth):
    def make_payload(self) -> OAuthPayload:
        return OAuthPayload('Google')


class FacebookOAuth(OAuth):
    def make_payload(self) -> OAuthPayload:
        return OAuthPayload('Facebook')


class OAuthManager:
    """
    OAuthManger wants to create OAuthPayload object.
    It does not create OAuthPayload directly, instead
    delegates the responsibility of instantiation via OAuth class
    """

    def __init__(self, oauth_provider: Type[OAuth]):
        """ use Dependency Injection pattern """
        self.oauth_provider = oauth_provider

    def build_payload(self):
        return self.oauth_provider().make_payload()


if __name__ == '__main__':
    payload = OAuthManager(GoogleOAuth).build_payload()
    print(payload.provider)
