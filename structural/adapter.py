class FaceBookOpenGraph:
    @staticmethod
    def print_sample():
        print('<meta property="og:url" content="https://github.com/usera2tt">')


class TwitterOpenGraph:
    @staticmethod
    def print_sample_card():
        print('<meta name="twitter:card" content="summary">')


class TwitterToFaceBookAdapter(TwitterOpenGraph):
    def print_sample(self):
        self.print_sample_card()


if __name__ == '__main__':
    FaceBookOpenGraph.print_sample()
    TwitterToFaceBookAdapter().print_sample()
