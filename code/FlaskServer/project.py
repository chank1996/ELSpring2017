from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def interface():
	return render_template('LinuxProject.html')

if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = 1024, debug = True)
