import json

def calc(data):
  from sklearn import linear_model
  from mpl_toolkits.mplot3d import Axes3D
  import matplotlib.pyplot as plt
  import numpy as np
  import json

  d = np.array(data)

  tarR = d[:,3]
  tarG = d[:,4]
  tarB = d[:,5]

  modelR = linear_model.LinearRegression()
  modelG = linear_model.LinearRegression()
  modelB = linear_model.LinearRegression()

  X = d[:,:3]
  modelR.fit(X, tarR)
  modelG.fit(X, tarG)
  modelB.fit(X, tarB)

  arr = []
  size = 16
  for b in range(size):
    for g in range(size):
      for r in range(size):
        arr.append( [r / size,g / size,b / size])

  arr = np.array(arr)
  result = np.array([
    modelR.predict(arr),
    modelG.predict(arr),
    modelB.predict(arr),
  ]).transpose()

  return result.tolist()
  # fig=plt.figure()
  # ax=Axes3D(fig)
  # ax.scatter3D(tarR, tarG, tarB)
  # ax.set_xlabel("r")
  # ax.set_ylabel("g")
  # ax.set_zlabel("b")
  # plt.show()

from flask import Flask, jsonify, request
import flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/calc', methods=['POST'])
def index():
    d = request.data.decode('utf-8')
    d = json.loads(d)
    return jsonify(calc(d["data"]))
 
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
 
app.run(port=8000, debug=True)
