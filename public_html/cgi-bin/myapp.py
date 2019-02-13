import os
import sys
sys.path.insert(0, '/home/vc7mi9ics39z/public_html/cgi-bin/myenv/lib/python3.4/site-packages')
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/test')
def test():
    return "new test"

@app.route('/help')
def hello_world():
    return "Hello world"



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=4000)

