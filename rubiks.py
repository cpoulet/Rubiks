from flask import Flask, request, jsonify, render_template
from static.py.cube import Cube
from static.py.unfolded import Unfolded

app = Flask(__name__)

#R = RubikSolver()
c = Cube()

@app.route('/')
def index():
    return render_template('rubiks.html', title="Rubik's Solver")

@app.route('/mix', methods=['POST'])
def user():
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

@app.route('/cross', methods=['POST'])
def foo():
    print(request.form['toto'])
    return jsonify('processed data :' + request.form['test'] + '/' + request.form['toto'])

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
