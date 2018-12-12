from flask import Flask, request, jsonify, render_template
from static.py.cube import Cube

app = Flask(__name__)

c = Cube()

@app.route('/')
def index():
    return render_template('rubiks.html', title="Rubik's Solver")

@app.route('/mix', methods=['POST'])
def mixing():
    s = c.randmix(10)
    print(s)
    seq = []
    for move in s:
        if len(move) == 2 and move[1] == '2':
            seq.append(move[0])
            seq.append(move[0])
        else:
            seq.append(move)
    return jsonify(seq)

@app.route('/reset', methods=['POST'])
def reset():
    c.reset()
    return jsonify(True)

@app.route('/move', methods=['POST'])
def move():
    m = request.data.decode()
    c.move(m)
    c.show()
    return jsonify(True)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
