from flask import Flask, jsonify, request
from flask_cors import CORS
from string import Template
from mpl_toolkits.mplot3d import Axes3D
from sklearn import linear_model
from sklearn.linear_model import Ridge 
from sklearn.preprocessing import PolynomialFeatures 
from sklearn.pipeline import make_pipeline 
import flask
import json
import matplotlib.pyplot as plt
import numpy as np

def calc(data, size):
  d = np.array(data)
  np.random.shuffle(d)
  X = d[:,:3]
  Y = d[:,3:]

  poly = PolynomialFeatures(degree=3)
  model = make_pipeline(poly, Ridge())
  model.fit(X, Y)

  arr = []
  size_range = range(size)
  size_minus1 = size - 1
  for b in size_range:
    for g in size_range:
      for r in size_range:
        arr.append([r / size_minus1, g / size_minus1, b / size_minus1])

  arr = np.array(arr)
  result = np.array(model.predict(arr))

  return result.tolist()

def to_file_str(data, size, title, created_by):
  tpl = Template('#Created by: $created_by\nTITLE "$title"\nLUT_3D_SIZE $size\nDOMAIN_MIN 0.0 0.0 0.0\nDOMAIN_MAX 1.0 1.0 1.0\n$lut_data')
  lut_data = ''
  for rgb in data:
    lut_data = lut_data + "\n" + ' '.join(map(str, rgb))
  return tpl.substitute(created_by=created_by, title=title, size=size, lut_data=lut_data)

app = Flask(__name__)
CORS(app)

@app.route('/calc', methods=['POST'])
def index():
    d = request.data.decode('utf-8')
    d = json.loads(d)
    size = 17
    data = calc(d["data"], size)
    return to_file_str(
      data,
      size,
      "mino",
      "mino",
    )
 
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
 
app.run(port=8000, debug=True)
