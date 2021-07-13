from flask import Flask

app = Flask('__main__')

@app.route('/')
def hello():
	return 'Hello !'
