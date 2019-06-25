import cv2
import numpy as np

blur_image = None
mask_image = None
min_color = None
max_color = None
first_color = True

def mouseEvent(event, x, y, flags, param):
  global blur_image, min_color, max_color, first_color, mask_image
  if event == 4:
    blue = blur_image[y][x][0]
    green = blur_image[y][x][1]
    red = blur_image[y][x][2]

  if first_color:
    min_color = [blue, green, red]
    max_color = [blue, green, red]
    lower_bound = np.array(min_color, dtype = 'uint8')
    upper_bound = np.array(max_color, dtype = 'uint8')
    mask_image = cv2.inRange(blur_image, lower_bound, upper_bound)
    first_color = False

  else:
    [min_blue, min_green, min_red] = min_color
    [max_blue, max_green, max_red] = max_color
    if blue < min_blue:
      min_blue = blue
    if green < min_green:
      min_green = green
    if red < min_red:
      min_red = red
    if blue > max_blue:
      max_blue = blue
    if green > max_green:
      max_green = green
    if red > max_red:
      max_red = red
      
    min_color = [min_blue, min_green, min_red]
    max_color = [max_blue, max_green, max_red]
    lower_bound = np.array(min_color, dtype = 'uint8')
    upper_bound = np.array(max_color, dtype = 'uint8')
    mask_image = cv2.inRange(blur_image, lower_bound, upper_bound)
    
  print 'min_color:', min_color, 'max_color:', max_color

def main():
  global blur_image, min_color, max_color, first_color, mask_image
  color_image = cv2.imread('../start_img.jpg', cv2.IMREAD_COLOR)
  blur_image = cv2.GaussianBlur(color_image, (5, 5), 0)
  
  params = cv2.SimpleBlobDetector_Params()
  params.minThreshold = 0
  params.maxThreshold = 255
  params.filterByArea = True
  params.minArea = 50
  params.maxArea = 256 * 256
  params.filterByCircularity = False
  params.minCircularity = 0.1
  params.filterByConvexity = False
  params.minConvexity = 0.9
  params.filterByInertia = False
  params.minInertiaRatio = 0.5
  ver = (cv2.__version__).split('.')
  
  if int(ver[0]) < 3:
    detector = cv2.SimpleBlobDetector(params)
  else:
    detector = cv2.SimpleBlobDetector_create(params)

  cv2.namedWindow('Blur Image')
  cv2.setMouseCallback('Blur Image', mouseEvent)
  cv2.imshow('Blur Image', blur_image)
  while True:
    if not first_color:
      cv2.imshow('Mask', mask_image)
    key = cv2.waitKey(1) & 0xFF
      if key == ord('q'):
        break;
    elif key == ord(' '):
      print 'Detecting blobs'
      keypoints = detector.detect(255 - mask_image)
      print 'length:', len(keypoints)
      for x in keypoints:
        print x.size, x.angle
      kp_image = cv2.drawKeypoints(blur_image, keypoints, np.array([]), (0, 255, 0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
      cv2.imshow('Keypoints', kp_image)
  cv2.destroyAllWindows()

if __name__ == '__main__':
  main()
