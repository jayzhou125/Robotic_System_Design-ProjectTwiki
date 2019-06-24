import cv2

def main():
  color_image = cv2.imread('start_img.jpg', cv2.IMREAD_COLOR)
  cv2.imshow('Image', color_image)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
  
if __name__ == '__main__':
  main()
