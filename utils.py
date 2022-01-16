import cv2 as cv
import numpy as np
from scipy.ndimage import gaussian_filter1d
import base64

def save_base64_img(image_64_encode, loc):
  image_64_decode = base64.decodebytes(image_64_encode) 
  image_result = open(loc, 'wb')
  image_result.write(image_64_decode)

def preprocess_image(img_path):
  """takes the path of the image and outputs the original image and preprocessed image"""
  orig_img = cv.imread(img_path)
  height, width = orig_img.shape[:2]
  img_bnw = cv.cvtColor(orig_img,cv.COLOR_BGR2GRAY)
  img_bnw = cv.fastNlMeansDenoising(img_bnw, h=5)


  # Auto Outsu Thresholding
  img_bin = cv.threshold(img_bnw, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]

  return orig_img, img_bin, height, width 


def align_image_stage1(orig_img, img_bin, height, width, threshold = 200, variance = 10):
  lines = cv.HoughLinesP(img_bin, 1, np.pi / 720, threshold, minLineLength=img_bin.shape[1] / 12, maxLineGap=img_bin.shape[1] / 160)

  angles = []
  for line in lines:
    x1, y1, x2, y2 = line[0]
    angles.append(np.arctan2(y2 - y1, x2 - x1))
  erect = np.sum([abs(angle) < np.pi / 4 for angle in angles]) > len(angles) / 2

  if erect:
    filtered_angles = [angle for angle in angles if abs(angle) < np.deg2rad(variance)]
  else:
    filtered_angles = [angle for angle in angles 
                       if np.deg2rad(90 - variance) < abs(angle) < np.deg2rad(90 + variance)]
  
  if len(filtered_angles) < 5:
    return None, orig_img
  rotation_angle = np.rad2deg(np.median(filtered_angles))

  if not erect:
    if rotation_angle < 0:
      orig_img = cv.rotate(orig_img, cv.ROTATE_90_CLOCKWISE)
      rotation_angle += 90
    elif rotation_angle > 0:
      orig_img = cv.rotate(orig_img, cv.ROTATE_90_COUNTERCLOCKWISE)
      rotation_angle -= 90
  M = cv.getRotationMatrix2D((orig_img.shape[1] // 2, orig_img.shape[0] // 2), rotation_angle, 1)
  img = cv.warpAffine(orig_img, M, (orig_img.shape[1], orig_img.shape[0]), borderMode=cv.BORDER_REPLICATE)
  return 1, img

def align_image_stage2(s1,guss_sigma = 7):
  s1_bw = cv.cvtColor(s1, cv.COLOR_BGR2GRAY)
  s1_bin = cv.threshold(s1_bw, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]

  projection = np.sum(s1_bin, 1)
  smooth_projection = gaussian_filter1d(projection,guss_sigma)


  mask = smooth_projection > np.average(smooth_projection)
  edges = np.convolve(mask, [1, -1])
  
  line_starts = np.where(edges == 1)[0]
  line_endings = np.where(edges == -1)[0]

  if len(line_starts) == 0:
    return None, s1

  lower_peaks = 0
  for start, end in zip(line_starts, line_endings):
    line = smooth_projection[start:end]
    if np.argmax(line) < len(line)/2:
        lower_peaks += 1

  # print(lower_peaks / len(line_starts))
  s1_bin_top_heavy_index = np.sum(s1_bin[:s1_bin.shape[0]//2,:])/np.sum(s1_bin)
  s1_bin_projection_confidence = (lower_peaks / len(line_starts))

  comb_metric = 0.7*s1_bin_top_heavy_index + 0.3*s1_bin_projection_confidence

  if (comb_metric) < 0.5:
    return 1, cv.rotate(s1, cv.ROTATE_180)
  return 1, s1

def align_image(img_path):
  s0 = preprocess_image(img_path)
  _s1, s1 = align_image_stage1(*s0, threshold = 200)
  _s2, s2 = align_image_stage2(s1)

  retval, buffer = cv.imencode('.jpg', s2)
  jpg_as_text = base64.b64encode(buffer)
  return jpg_as_text
