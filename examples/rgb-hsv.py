import cv2

def main():
  color_image = cv2.imread('../start_img.jpg', cv2.IMREAD_COLOR)
  blur_image = cv2.GaussianBlur(color_image, (5, 5), 0)
  yuv_image = cv2.cvtColor(blur_image, cv2.COLOR_BGR2HSV)
  h, s, v = cv2.split(yuv_image)
  cv2.imshow('Image', blur_image)
  cv2.imshow('H', h)
  cv2.imshow('S', s)
  cv2.imshow('V', v)
  while True:
    key = cv2.waitKey(0) & 0xFF
    if key == ord('q'):
      break;
  cv2.destroyAllWindows()
  
if __name__ == '__main__':
  main()
