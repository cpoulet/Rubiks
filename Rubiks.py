from flask import Flask, request, jsonify
from static.py.rubik import BFS, State, Cube, RubikSolver

app = Flask(__name__)

R = RubikSolver()

@app.route('/mix', methods=['POST'])
def user():
    print('PYTHON')
   # print(request.form['moves'])
    return jsonify('200')

@app.route('/cross', methods=['POST'])
def foo():
    print(request.form['toto'])
    return jsonify('processed data :' + request.form['test'] + '/' + request.form['toto'])

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
