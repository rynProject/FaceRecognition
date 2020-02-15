import cv2

vidcap = cv2.VideoCapture("video.mp4")
success = True
success, image = vidcap.read()
Count = 0

while success:
    cv2.imwrite("eno%d.jpg" % Count, image)
    success, image = vidcap.read()

    print("New Frame = ", success)
    Count += 1
