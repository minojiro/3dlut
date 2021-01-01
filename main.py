from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ExpSineSquared, RBF,ConstantKernel
from sklearn.linear_model import LinearRegression
from string import Template
import colorsys
import cv2
import datetime
import matplotlib.pyplot as plt
import numpy as np

def load_image(path):
  print("loading image: " + path)
  img = cv2.imread(path)
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  arr = np.asarray(img)
  arr = arr.reshape(-1,3)
  result = np.array([[rgb[0]/255, rgb[1]/255, rgb[2]/255] for rgb in arr]) 
  return result

def load_images(image_count):
  result = np.array([]).reshape(0,6)
  for num in range(1, image_count + 1):
    rgb_x = load_image('./images/'+str(num).zfill(2)+'_x.jpg')
    rgb_y = load_image('./images/'+str(num).zfill(2)+'_y.jpg')
    result = np.vstack([result, np.block([rgb_x, rgb_y])])
  return result

def get_lut_hsv_list(size):
  steps = np.linspace(0.0, 1.0, size)
  rgb_list = [[r, g, b] for r in steps for g in steps for b in steps]
  return np.array([colorsys.rgb_to_hsv(*rgb) for rgb in rgb_list])

def generate_cube_file(data, size, title):
  tpl = Template("\n".join([
    'TITLE "$title"',
    'LUT_3D_SIZE $size',
    'DOMAIN_MIN 0.0 0.0 0.0',
    'DOMAIN_MAX 1.0 1.0 1.0',
    '$lut_data'
  ]))
  lut_data = "\n".join([' '.join(map(str, rgb)) for rgb in data])
  return tpl.substitute(title=title, size=size, lut_data=lut_data)

def main():
  # [[xR, xG, xB, yR, yG, yB] ...]
  rgb_xy_all = load_images(17)

  # 全部処理すると重いので、適当な数に間引く
  np.random.shuffle(rgb_xy_all)
  rgb_xy = rgb_xy_all[:100,:]

  rgb_x = rgb_xy[:,:3]
  rgb_y = rgb_xy[:,3:]

  hsv_x = np.array([colorsys.rgb_to_hsv(*rgb) for rgb in rgb_x])
  hsv_y = np.array([colorsys.rgb_to_hsv(*rgb) for rgb in rgb_y])

  h_delta = hsv_x[:,0] - hsv_y[:,0]
  s_delta = hsv_x[:,1] - hsv_y[:,1]
  v_delta = hsv_x[:,2] - hsv_y[:,2]

  print("building model: H")
  h_kernel = RBF(length_scale=1)
  h_model = GaussianProcessRegressor(kernel=h_kernel).fit(hsv_x, h_delta)

  print("building model: S")
  s_kernel = RBF(length_scale=1)
  s_model = GaussianProcessRegressor(kernel=s_kernel).fit(hsv_x, s_delta)

  print("building model: V")
  v_kernel = RBF(length_scale=1)
  v_model = GaussianProcessRegressor(kernel=v_kernel).fit(hsv_x, v_delta)

  def predict(hsv_list):
    print("predicting")
    return np.array([
      h_model.predict(hsv_list) + hsv_list[:,0],
      s_model.predict(hsv_list) + hsv_list[:,1],
      v_model.predict(hsv_list) + hsv_list[:,2],
    ]).T

  test_image = load_image('./images/01_x.jpg')
  test_image_hsv = predict(np.array([colorsys.rgb_to_hsv(*rgb) for rgb in test_image]))
  print("imshow")
  plt.imshow(np.array([colorsys.hsv_to_rgb(*hsv) for hsv in test_image_hsv]).reshape(-1,60,3))
  plt.show()

  # LUTの格子の数
  size = 33
  lut_hsv_list = get_lut_hsv_list(size)
  lut_predicted_hsv_list = predict(lut_hsv_list)
  lut_predicted_rgb_list = np.array([colorsys.hsv_to_rgb(*hsv) for hsv in lut_predicted_hsv_list])

  title = "ILCE-7RM3_SEL55F18Z_TO_AI-NIKKOR-50"
  file_str = generate_cube_file(
    size=size, data=lut_predicted_rgb_list, title=titles
  )
  now = datetime.datetime.now()
  file_name = now.strftime(title + "_%Y%m%d%H%M%S.CUBE")
  print("saving file: " + file_name)
  file = open("./luts/" + file_name, 'w')
  file.write(file_str)

main()
