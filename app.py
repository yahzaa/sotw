import os
from flask import Flask
from flask import render_template
from flask import url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def root():
    styles_url = url_for('static', filename='style.css')
    return render_template('root.html', styles_url=styles_url)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
