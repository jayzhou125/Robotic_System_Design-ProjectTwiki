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

###################################Need to fix after this
def main():
global blur_image, min_color, max_color, first_color, mask_image
color_image = cv2.imread(
../start_img.jpg
, cv2.IMREAD_COLOR)
blur_image = cv2.GaussianBlur(color_image, (5, 5), 0)
cv2.namedWindow(
Blur Image
)
cv2.setMouseCallback(
Blur Image
, mouseEvent)
cv2.imshow(
Blur Image
, blur_image)
while True:
if not first_color:
cv2.imshow(
Mask
, mask_image)
key = cv2.waitKey(1) & 0xFF
if key == ord(
q
):
break;
elif key == ord(
 
):
(cnts, hierarchy) = cv2.findContours(mask_image.copy(), cv2.RETR_TREE,
cv2.CHAIN_APPROX_SIMPLE)
print 
number of contours:
, len(cnts)
print 
len(heirarchy):
, len(hierarchy), len(hierarchy[0])
print hierarchy
for i in range(0, len(cnts)):
c = cnts[i]
if cv2.contourArea(c) < 100:
continue
if not hierarchy[0][i][3] == -1:
continue
x,y,w,h = cv2.boundingRect(c)
print hierarchy[0][i], cv2.contourArea(c)
cv2.rectangle(blur_image, (x,y), (x + w, y + h), (0, 255, 0), 3);
cv2.imshow(
Bounding
, blur_image)
cv2.destroyAllWindows()
if __name__ == 
__main__
:
main()
