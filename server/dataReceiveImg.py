import flask
import os
import datetime

SAVE_DIR = "./images"
if not os.path.isdir(SAVE_DIR):
    os.mkdir(SAVE_DIR)

f = open( "config_server.json", "r" )
tmp = f.read()
tmp = json.loads( tmp )
f.close()

app = flask.Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/upload', methods=['POST'])
def upload():
    if flask.request.files['image']:
        img = flask.request.files['image']
        filename = datetime.datetime.now().strftime("%Y_%m_%d%_H_%M_%S_") + ".jpg"
        img.save(os.path.join(SAVE_DIR,filename))
        print("save image!")
    else:
        print(flask.request.files['image'])

if __name__ == "__main__":
	app.run(debug=True, host=tmp["address"], port=tmp["port"])
