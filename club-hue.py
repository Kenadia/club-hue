from threading import Thread

from flask import Flask, render_template

from hue import Colors, Context, Dance, Lights, Timer


app = Flask(__name__)


def main():
    dancer_thread = Thread(target=start_dance)
    dancer_thread.daemon = True
    dancer_thread.start()
    app.run()


def start_dance():
    timer = Timer(120.0)
    lights = Lights([1, 2, 3])
    colors = Colors()
    context = Context(timer, lights, colors)
    Dance(context).play()


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == "__main__":
    main()
