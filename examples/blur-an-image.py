import cv2

def main():
  color_image = cv2.imread('start_img.jpg', cv2.IMREAD_COLOR)
  blur_image = cv2.GaussianBlur(color_image, (5, 5), 0)
  cv2.imshow('Image', color_image)
  cv2.imshow('Blur Image', blur_image)
  while True:
    key = cv2.waitKey(0) & 0xFF
    if key == ord('q'):
      break;
  cv2.destroyAllWindows()
  
if __name__ == '__main__':
  main()
