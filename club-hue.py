from flask import Flask

from hue import Colors, Context, Dance, Lights, Timer


class Dancer(object):

    def __init__(self):
        timer = Timer(120.0)
        lights = Lights([1, 2, 3])
        colors = Colors()
        self.context = Context(timer, lights, colors)
        self.dance = Dance(self.context)

    def start(self):
        self.dance.play()


app = Flask(__name__)


def main():
    dancer = Dancer()
    dancer.start()
    app.run()


@app.route('/')
def home():
    return 'It works'


if __name__ == "__main__":
    main()
