from flask import *

app = Flask(__name__)

f = open( "config_server.json", "r" )
tmp = f.read()
tmp = json.loads( tmp )
f.close()

@app.route("/data", methods=["POST"])
def data():
        print( request )
        return "POST OK.\n"


if __name__ == "__main__":
    app.run(debug=True, host=tmp["address"], port=tmp["port"], threaded=True)
