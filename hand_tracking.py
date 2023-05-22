import math
import cv2
import numpy as np
import convex_hull

def cv2_contour_to_points(contour):
    points = []
    for i in range(len(contour[0])):
        points.append([contour[0][i][0][0],contour[0][i][0][1]])
    return points

def points_to_cv2_hull(points):
    hull = []
    for i in range(len(points)):
        hull.append([[points[i][0],points[i][1]]])
    return [np.array(hull)]

def points_to_indices(hull,contour):
    indices = []
    for i in range(len(hull)):
        for j in range(len(contour)):
            if np.array_equal(contour[j],hull[i]):
                indices.append([j])
    return np.sort(np.array(indices),axis=0)[::-1]

def skin_segmentation(image):
    # change RGB to YCrCb
    image = cv2.blur(image, (3, 3))
    image_YCrCb = cv2.cvtColor(image,cv2.COLOR_BGR2YCR_CB)

    # range warna kulit
    min_YCrCb = np.array([0,133,77],np.uint8)
    max_YCrCb = np.array([235,173,127],np.uint8)

    # skin segmentation
    skin_region = cv2.inRange(image_YCrCb,min_YCrCb,max_YCrCb)
    skin_image = cv2.bitwise_and(image, image, mask = skin_region)
    skin_image = cv2.erode(skin_image,np.ones((5, 5), np.uint8))

    # convert to black and white
    skin_image = cv2.cvtColor(skin_image, cv2.COLOR_BGR2GRAY)
    skin_image = cv2.threshold(skin_image, 2, 255, cv2.THRESH_BINARY)[1]

    return skin_image

def hand_tracking(image):
    # hand detection
    skin_image = skin_segmentation(image)
 
    # find contours and change to points
    contours, _ = cv2.findContours(skin_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours,key=cv2.contourArea,reverse=True)
    points = cv2_contour_to_points(contours)

    # find convex hull
    hull = convex_hull.convex_hull(points)
    hull = points_to_cv2_hull(hull)

    # find convexity defects
    contour0 = contours[0]
    hull_indices = points_to_indices(hull[0],contour0)
    defects = cv2.convexityDefects(contour0, hull_indices)

    # draw contours, convex hull, and convexity defects
    green_color = (0, 255, 0) # green_color for contours
    blue_color = (255, 0, 0) # bluee_color for convex hull
    red_color = (0, 0, 255) # red_color for convexity defects

    cv2.drawContours(image, contours, 0, green_color, 5, 8)
    cv2.drawContours(image, hull, 0, blue_color, 5, 8)

    finger_count = 1
    for i in range(defects.shape[0]):
        start_id,end_id,far_id,d = defects[i,0]
        start = tuple(contour0[start_id][0])
        end = tuple(contour0[end_id][0])
        far = tuple(contour0[far_id][0])

        # length of triangle sidesss
        a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
        c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)

        # calculate distance and angle
        s = (a+b+c)/2
        ar = math.sqrt(s*(s-a)*(s-b)*(s-c))
        d=(2*ar)/a
        angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 180 / math.pi

        # ignore defects that are not between two fingers
        if (angle <=90 and d>30):
            cv2.circle(image,far,8,red_color,-1)
            finger_count+=1

    # put text
    cv2.putText(image,str(finger_count),(0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2,5)

    return image