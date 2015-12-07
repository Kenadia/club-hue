from threading import Thread

from flask import Flask, jsonify, render_template, request

from hue import Colors, Context, Dance, Lights, Timer

app = Flask(__name__)
timer = Timer(120.0)
lights = Lights([1, 2, 3])
colors = Colors()
context = Context(timer, lights, colors)
dance = Dance(context)


def main():
    dancer_thread = Thread(target=start_dance)
    dancer_thread.daemon = True
    dancer_thread.start()
    app.run()


def start_dance():
    dance.play()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/bpm/', methods=['PUT'])
def bpm():
    print 'Changing BPM to ', request.form['bpm']
    timer.bpm = float(request.form['bpm'])
    return jsonify({})


if __name__ == "__main__":
    main()
