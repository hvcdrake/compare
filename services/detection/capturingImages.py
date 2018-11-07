import cv2
import datetime
import DetectionClass as det

KEY_CODE_ENTER = 13
KEY_CODE_ESC = 27


def captureImage(vid, prefix):
    # video = cv2.VideoCapture(0)
    a = 0
    success = True
    filename = ""
    save_flag = False

    while success:
        a = a + 1
        success, frame = vid.read()

        cv2.imshow("Capturing " + prefix, frame)
        key = cv2.waitKey(1)

        if key == KEY_CODE_ENTER:
            now = datetime.datetime.now()
            filename = prefix + "_{}.jpg".format(now.strftime('_%Y%m%dT%H%M%S'))
            save_flag = cv2.imwrite("captures/" + filename, frame)
            if save_flag:
                print("Saved: " + filename)
            break
        if key == KEY_CODE_ESC:
            print("Cancela a petición del usuario")
            break
    # print (str(a)+" milliseconds")
    # vid.release()
    # cv2.destroyAllWindows()
    return (save_flag, filename)


def Main():
    # Initialize objects
    d = det.DetectionFace()
    video = cv2.VideoCapture(0)

    # Obteining and detecting the first capture DNI
    print("Presione ENTER cuando tenga el DNI enfocado")
    result1 = captureImage(video, "cap_dni")
    # print(str(result1[1]))

    print("Presione ENTER cuando tenga su rostro enfocado")
    result2 = captureImage(video, "cap_face")
    # print(str(result1[1]))

    video.release()
    cv2.destroyAllWindows()

    print("Detectando rostro en DNI ...")
    face1 = d.detection("captures/" + result1[1], "dni")

    print("Detectando rostro en foto frontal ...")
    face2 = d.detection("captures/" + result2[1], "face")

    if (face1 is not None and face2 is not None):
        comp_result = face1.verify(face2.getAzureId())
        print(comp_result)


def Test():
    # Initialize objects
    d = det.DetectionFace()
    # video = cv2.VideoCapture(0)

    print("Detectando rostro en DNI ...")
    face1 = d.detection("mayorCalidad/dni_iv.jpg", "dni")

    # print("Presione ENTER cuando tenga su rostro enfocado")
    # result2 = captureImage(video, "cap_face")

    print("Detectando rostro en foto frontal ...")
    face2 = d.detection("mayorCalidad/face_iv (2).jpg", "face")

    if (face1 is not None and face2 is not None):
        comp_result = face1.verify(face2.getAzureId())
        print(comp_result)

    # video.release()
    # cv2.destroyAllWindows()


Test()
