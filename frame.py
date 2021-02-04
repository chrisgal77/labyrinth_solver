import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

# img = cv.imread('lab2.png',0)
# laplacian = cv.Laplacian(img,cv.CV_64F)
# sobelx = cv.Sobel(img,cv.CV_64F,1,0,ksize=5)
# sobely = cv.Sobel(img,cv.CV_64F,0,1,ksize=5)
# plt.subplot(2,2,1),plt.imshow(img,cmap = 'gray')
# plt.title('Original'), plt.xticks([]), plt.yticks([])
# plt.subplot(2,2,2),plt.imshow(laplacian,cmap = 'gray')
# plt.title('Laplacian'), plt.xticks([]), plt.yticks([])
# plt.subplot(2,2,3),plt.imshow(sobelx,cmap = 'gray')
# plt.title('Sobel X'), plt.xticks([]), plt.yticks([])
# plt.subplot(2,2,4),plt.imshow(sobely,cmap = 'gray')
# plt.title('Sobel Y'), plt.xticks([]), plt.yticks([])
# plt.show()

# img = cv.imread('lab2.png',0)
# # Output dtype = cv.CV_8U
# sobelx8u = cv.Sobel(img,cv.CV_8U,1,0,ksize=5)
# # Output dtype = cv.CV_64F. Then take its absolute and convert to cv.CV_8U
# sobelx64f = cv.Sobel(img,cv.CV_64F,1,0,ksize=5)
# abs_sobel64f = np.absolute(sobelx64f)
# sobel_8u = np.uint8(abs_sobel64f)
# plt.subplot(1,3,1),plt.imshow(img,cmap = 'gray')
# plt.title('Original'), plt.xticks([]), plt.yticks([])
# plt.subplot(1,3,2),plt.imshow(sobelx8u,cmap = 'gray')
# plt.title('Sobel CV_8U'), plt.xticks([]), plt.yticks([])
# plt.subplot(1,3,3),plt.imshow(sobel_8u,cmap = 'gray')
# plt.title('Sobel abs(CV_64F)'), plt.xticks([]), plt.yticks([])
# plt.show()

# img = cv.imread('lab2.png',0)
# edges = cv.Canny(img,100,200)
# plt.subplot(121),plt.imshow(img,cmap = 'gray')
# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122),plt.imshow(edges,cmap = 'gray')
# plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
# plt.show()

# img = cv.imread('lab2.png')
# img_gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
# ret,thresh = cv.threshold(img_gray, 127, 255,0)
# contours,hierarchy = cv.findContours(thresh,2,1)
# cnt = contours[0]
# hull = cv.convexHull(cnt,returnPoints = False)
# defects = cv.convexityDefects(cnt,hull)
# for i in range(defects.shape[0]):
#     s,e,f,d = defects[i,0]
#     start = tuple(cnt[s][0])
#     end = tuple(cnt[e][0])
#     far = tuple(cnt[f][0])
#     cv.line(img,start,end,[0,255,0],2)
#     cv.circle(img,far,5,[0,0,255],-1)
# cv.imshow('img',img)
# cv.waitKey(0)
# cv.destroyAllWindows()

# # Load an image
# image = cv.imread('lab2.png')
# # Changing the colour-space
# LUV = cv.cvtColor(image, cv.COLOR_BGR2LUV)
# # Find edges
# edges = cv.Canny(LUV, 10, 100)
# # Find Contours
# contours, hierarchy = cv.findContours(edges,cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
# # Find Number of contours
# print("Number of Contours is: " + str(len(contours)))
# # Draw yellow border around two contours
# cv.drawContours(image, contours, 0, (0, 230, 255), 6)
# cv.drawContours(image, contours, 2, (0, 230, 255), 6)
# # Show the image with contours
# cv.imshow('Contours', image)
# cv.waitKey(0)


# if __debug__ and __name__ == "__main__":
    # pass