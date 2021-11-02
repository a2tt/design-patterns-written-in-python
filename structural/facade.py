class Camera:
    @staticmethod
    def take_a_picture():
        print('take a picture of the view')


class Wheel:
    @staticmethod
    def rotate(deg):
        print(f'rotate {deg}°')

    @staticmethod
    def move():
        print('move forward')


class CuriosityFacade:
    """ https://en.wikipedia.org/wiki/Curiosity_(rover) """

    def __init__(self):
        self.wheel = Wheel()
        self.camera = Camera()

    def move(self, deg: int = 0):
        self.wheel.rotate(deg)
        self.camera.take_a_picture()
        self.wheel.move()
        self.camera.take_a_picture()


if __name__ == '__main__':
    curiosity = CuriosityFacade()
    curiosity.move(30)
