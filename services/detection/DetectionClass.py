import dlib
from skimage import io
import cv2
import detection.faceApi.face as f

# You can download the required pre-trained face detection model here:
# http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
predictor_model = "detection/shape_predictor_68_face_landmarks.dat"


class DetectionFace():
    """An object used to split and detect faces:
    """

    def __init__(self):
        """
        initialize the object
        """
        self.face_detector = dlib.get_frontal_face_detector()
        self.face_pose_predictor = dlib.shape_predictor(predictor_model)

    def detection(self, path, s):
        """
        Returning the object Face from an image filepath
        """
        # win = dlib.image_window()
        # Load the image
        image = cv2.imread(path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Run the HOG face detector on the image data
        detected_faces = self.face_detector(gray, 2)

        # Show the desktop window with the image
        # win.set_image(image)

        try:
            # Detecting just the first img
            face_rect = detected_faces[0]
            i = 0

            # Detected faces are returned as an object with the coordinates
            # of the top, left, right and bottom edges
            # print("- Face #{} found at Left: {} Top: {} Right: {} Bottom: {}".format(i, face_rect.left(), face_rect.top(), face_rect.right(), face_rect.bottom()))

            # Draw a box around each face we found
            # win.add_overlay(face_rect)

            # Get the the face's pose
            # pose_landmarks = self.face_pose_predictor(image, face_rect)

            # Draw the face landmarks on the screen.
            # win.add_overlay(pose_landmarks)

            # Saving just face images
            # print("Saving: chiquis/chiqui_{}.jpg".format(i))
            top = int(face_rect.top())
            bottom = int(face_rect.bottom())
            left = int(face_rect.left())
            right = int(face_rect.right())

            new_top = int(top * 0.9)
            new_bottom = int(bottom * 1.1)
            new_left = int(left * 0.9)
            new_right = int(right * 1.1)

            print(str(top)+","+str(bottom)+","+str(left)+","+str(right))

            gray = gray[new_top:new_bottom, new_left:new_right]
            flag = cv2.imwrite("thumbs/th_" + s + ".jpg", gray)
            c = (0, 255, 0)
            test = cv2.rectangle(image, (left, top), (right, bottom), c, 5)
            # print("F:" + str(flag))
            if(flag):
                face = f.Face(open("thumbs/th_" + s + ".jpg", 'rb'))
                print("azureId:" + str(face.azureFaceId))
                cv2.imwrite("processed/p_" + s + ".jpg", test)
            # dlib.hit_enter_to_continue()
            else:
                return None
        except IndexError:
            print("No se detecto ningun rostro")
            return None

        return face
