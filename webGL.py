from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('cube.html', title='Rubiks')
   
@app.route('/data', methods=['POST'])
def foo():
    print(request.form['toto'])
    return 'processed data :' + request.form['test'] + '/' + request.form['toto']

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
