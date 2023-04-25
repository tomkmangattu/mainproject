import cv2
import numpy as np
from scipy.spatial.distance import cdist

# Load the image
img = cv2.imread('board1.jpg')

# Convert the image from BGR to HSV color space
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Define the lower and upper bounds for the marble blue color
lower_blue = np.array([100, 50, 50])
upper_blue = np.array([140, 255, 255])

# Create a mask using the lower and upper bounds for the marble blue color
mask = cv2.inRange(hsv, lower_blue, upper_blue)

# Apply the mask to the original image
result = cv2.bitwise_and(img, img, mask=mask)

ret, binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

# Find contours in the binary image
contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Sort the contours by area in descending order
contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

# Select the 4 largest contours
largest_contours = contours[:4]

# Draw the selected contours and mark the center on the original image
result_copy = img.copy() # make a copy of the original image to draw contours on
points_map = {}
height = img.shape[0]
width = img.shape[1]
offset = height // 50

for contour in largest_contours:
    M = cv2.moments(contour)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    # cv2.drawContours(result_copy, [contour], -1, (0, 255, 0), 3) # draw the contour in green with thickness 3
    cv2.circle(result_copy, (cx, cy), 5, (0, 0, 255), -1) # draw a red circle at the center of the contour


    if cx < height/ 2:
        if cy < width / 2:
            print("bottom left :", cx, cy)
            points_map["bottom left"] = [cx + offset, cy + offset]
        else:
            print("bottom right :", cx, cy)
            points_map["bottom right"] = [cx + offset, cy - offset]
    elif cy < width /2:
        print("top left :", cx, cy)
        points_map["top left"] = [cx - offset, cy + offset * 4]
    else:
        print("top right :", cx, cy)
        points_map["top right"] = [cx - offset, cy - offset]
    
    # points.append((cx, cy))
points = []
points.append(points_map["top left"])
points.append(points_map["top right"])
points.append(points_map["bottom right"])
points.append(points_map["bottom left"])

# Create a mask for the area inside the polygon defined by the 4 points
mask = np.zeros(img.shape[:2], np.uint8) # create an empty mask with the same size as the image
pts = np.array(points, np.int32) # convert the list of points to a numpy array of integers
pts = pts.reshape((-1,1,2))
cv2.fillPoly(mask,[pts],255) # fill the polygon defined by the points with white color (255)

# Apply the mask to the original image
#masked_image = cv2.bitwise_and(img, img, mask=mask)

# for contour in largest_contours:
#     M = cv2.moments(contour)
#     cx = int(M['m10']/M['m00'])
#     cy = int(M['m01']/M['m00'])
#     # cv2.drawContours(result_copy, [contour], -1, (0, 255, 0), 3) # draw the contour in green with thickness 3
#     cv2.circle(masked_image, (cx, cy), 5, (0, 0, 255), -1) # draw a red circle at the center of the contour

# Display the result

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert to gray
edges = cv2.Canny(gray, 50, 150, apertureSize=3) # find edges using canny edge detection
masked_image = cv2.bitwise_and(edges, edges, mask=mask)
# ret, binary = cv2.threshold(masked_image, 127, 255, cv2.THRESH_BINARY)

# cv2.imshow('edges of image', binary) # display image with edges

_, binary_image = cv2.threshold(masked_image, 0, 255, cv2.THRESH_BINARY)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (35, 35))
dilated_image = cv2.dilate(binary_image, kernel)


# Find contours
contours, _ = cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Find contour with largest area
max_contour = max(contours, key=cv2.contourArea)

# Draw contour on original image
# cv2.drawContours(img, [max_contour], -1, (0, 255, 0), 2)

x, y, w, h = cv2.boundingRect(max_contour)

# Extract the four corners of the rectangle
top_left = (x, y)
top_right = (x + w, y)
bottom_right = (x + w, y + h)
cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)

cv2.imshow('Result', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
