from flask import Flask, render_template
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)
cors = CORS(app)

class Lights(Resource):
    """ 
    @brief Class to handle requests
    """ 
    def get(self, id,rgb):
        ## @brief   Function to handle get requests
        print(rgb)
        r = rgb[0:2]
        g = rgb[2:4]
        b = rgb[4:6]
        str = "Light selected was {} r:{} g:{} b:{} ".format(id,r,g,b)
        print (str)
        return str

## Add route
# api.add_resource(Lights, "/lights/<string:id>/<string:r>/<string:g>/<string:b>/<string:w>")
api.add_resource(Lights, "/lights/<string:id>/<string:rgb>")

@app.route("/")
@cross_origin(origin='*', headers=['access-control-allow-origin', 'Content-Type', 'Authorization'])
def home():
    return render_template("home.html")

@app.route("/color")
def color():
    return render_template("color.html")


if __name__ == '__main__':
    ## Run Flask App
    app.run(host='0.0.0.0')
