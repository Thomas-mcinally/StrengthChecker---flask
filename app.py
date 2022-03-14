'''
Tutorial series to use: https://www.youtube.com/watch?v=mqhxxeeTbu0&list=PLzMcBGfZo4-n4vJJybUVV3Un_NFS5EOgX
'''


from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/deadlifts")
def deadlifts():
    return render_template('deadlifts.html')


if __name__=='__main__':
    app.run(debug=True)