import  face_recognition
import cv2


def face_detect(img):

    inputimage = cv2.imread(img)

    image = face_recognition.load_image_file(img)

    face_locations = face_recognition.face_locations(image)

    for face_location in face_locations:
        top, right, bottom, left = face_location
        face_image = image[top:bottom, left:right]
        cv2.rectangle(inputimage, (left, top), (right, bottom), (0, 0, 255), 2)

    cv2.imshow('Face Detection', inputimage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


face_detect('test1.jpg')
