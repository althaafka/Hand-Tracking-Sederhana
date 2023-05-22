import cv2
import hand_tracking as ht

# setup camera
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 350)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 350)

while True:
    _, frame = camera.read()
    frame = cv2.flip(frame, 1)

    # hand tracking
    try :
        frame = ht.hand_tracking(frame)
    except :
        pass

    cv2.imshow('WebCam', frame)

    if cv2.waitKey(1) == ord('q'):
        break
    if cv2.waitKey(1) == ord('s'):
        cv2.imwrite("image/image.jpg",frame)
        break

camera.release()
cv2.destroyAllWindows()