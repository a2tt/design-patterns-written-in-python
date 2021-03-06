from typing import Union


class PushNotification:
    def __init__(self, user: Union[int, str], url: str, content: str,
                 extra: dict = None):
        self.user = user
        self.url = url
        self.content = content
        self.extra = extra

    def __repr__(self):
        return f'To {self.user}\nURL: {self.url}\n{self.content}'


class PushBuilder:
    def __init__(self):
        self.user = None
        self.content = None
        self.url = None
        self.extra = {}

    def set_user(self, user: Union[int, str]):
        self.user = user

    def set_content(self, content: str):
        self.content = content

    def set_url(self, url: str):
        self.url = url

    def set_extra(self, extra: dict):
        if type(extra) == dict:
            self.extra.update(extra)
            self.extra = extra

    def build(self) -> PushNotification:
        return PushNotification(self.user, self.url, self.content, self.extra)


def main():
    # There might be more complicate steps
    builder = PushBuilder()
    builder.set_user(456)
    builder.set_url('https://github.com/usera2tt')
    builder.set_content('design pattern in python')

    push = builder.build()
    print(push)


if __name__ == '__main__':
    main()
