import cv2

# event
# 0 - mouse move
# 1 - left button down
# 2 - right button down
# 3 - middle button down
# 4 - left button up
# 5 - right button up
# 6 - middle button up

def mouseEvent(event, x, y, flags, param):
  if event == 4:
    print (x, y)

def main():
  color_image = cv2.imread('start_img.jpg', cv2.IMREAD_COLOR)
  blur_image = cv2.GaussianBlur(color_image, (5, 5), 0)
  cv2.namedWindow('Blur Image')
  cv2.setMouseCallback('Blur Image', mouseEvent)
  cv2.imshow('Blur Image', blur_image)
  while True:
    key = cv2.waitKey(0) & 0xFF
    if key == ord('q'):
      break;
  cv2.destroyAllWindows()
  
if __name__ == '__main__':
  main()
