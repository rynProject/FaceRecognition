import cv2

vidcap = cv2.VideoCapture("grey.mp4")
success = True
success, image = vidcap.read()
Count = 0

while success:
    cv2.imwrite("negatif%d.jpg" % Count, image)
    success, image = vidcap.read()

    print("New Frame = ", success)
    Count += 1
