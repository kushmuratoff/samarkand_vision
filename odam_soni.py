import cv2
from sklearn.metrics.pairwise import cosine_similarity
from insightface.app import FaceAnalysis
import insightface
import numpy as np

# detection
app = FaceAnalysis(allowed_modules=['detection','genderage'], name="buffalo_sc")
app.prepare(ctx_id=0, det_size=(640, 640), det_thresh=0.4)


cap = cv2.VideoCapture(0)
cv2.namedWindow("Detected Objects", cv2.WINDOW_NORMAL)

# font
font = cv2.FONT_HERSHEY_SIMPLEX

# org
org = (20, 30)

# fontScale
fontScale = 0.5

# Blue color in BGR
color = (255, 0, 0)

# Line thickness of 2 px
thickness = 1

# The gender model architecture
# https://drive.google.com/open?id=1W_moLzMlGiELyPxWiYQJ9KFaXroQ_NFQ
GENDER_MODEL = 'model/deploy_gender.prototxt'
# The gender model pre-trained weights
# https://drive.google.com/open?id=1AW3WduLk1haTVAxHOkVS_BEzel1WXQHP
GENDER_PROTO = 'model/gender_net.caffemodel'
# Each Caffe Model impose the shape of the input image also image preprocessing is required like mean
# substraction to eliminate the effect of illunination changes
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
# Represent the gender classes
GENDER_LIST = ['Male', 'Female']
# The model architecture
# download from: https://drive.google.com/open?id=1kiusFljZc9QfcIYdU2s7xrtWHTraHwmW
AGE_MODEL = 'model/deploy_age.prototxt'
# The model pre-trained weights
# download from: https://drive.google.com/open?id=1kWv0AjxGSN0g31OeJa02eBGM0R_jcjIl
AGE_PROTO = 'model/age_net.caffemodel'
# Represent the 8 age classes of this CNN probability layer
AGE_INTERVALS = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)',
                 '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']

# Load age prediction model
age_net = cv2.dnn.readNetFromCaffe(AGE_MODEL, AGE_PROTO)
# Load gender prediction model
gender_net = cv2.dnn.readNetFromCaffe(GENDER_MODEL, GENDER_PROTO)


def get_gender_predictions(face_img):
    blob = cv2.dnn.blobFromImage(
        image=face_img, scalefactor=1.0, size=(227, 227),
        mean=MODEL_MEAN_VALUES, swapRB=False, crop=False
    )
    gender_net.setInput(blob)
    return gender_net.forward()


def get_age_predictions(face_img):
    blob = cv2.dnn.blobFromImage(
        image=face_img, scalefactor=1.0, size=(227, 227),
        mean=MODEL_MEAN_VALUES, swapRB=False
    )
    age_net.setInput(blob)
    return age_net.forward()

def get_age_gender1(img):
    age_preds = get_age_predictions(img)
    gender_preds = get_gender_predictions(img)
    i = gender_preds[0].argmax()
    gender = GENDER_LIST[i]
    gender_confidence_score = gender_preds[0][i]
    i = age_preds[0].argmax()
    age = AGE_INTERVALS[i]
    age_confidence_score = age_preds[0][i]
    # Draw the box
    label = f"gender: {gender}-{gender_confidence_score * 100:.1f}%, age: {age}-{age_confidence_score * 100:.1f}%"
    return label

def get_age_gender(img):
    age_preds = get_age_predictions(img)
    gender_preds = get_gender_predictions(img)
    i = gender_preds[0].argmax()
    gender = GENDER_LIST[i]
    gender_confidence_score = gender_preds[0][i]
    i = age_preds[0].argmax()
    age = AGE_INTERVALS[i]
    age_confidence_score = age_preds[0][i]
    # Draw the box
    # label = f"{gender}-{gender_confidence_score * 100:.1f}%, {age}-{age_confidence_score * 100:.1f}%"
    return gender, age


while cap.isOpened():

    # Press key q to stop
    if cv2.waitKey(1) == ord('q'):
        break

    try:
        ret, frame = cap.read()
        if not ret:
            break
        faces = app.get(frame)
        for face in faces:
            startX, startY = (int(face.bbox[0]),int(face.bbox[1]))
            endX, endY = (int(face.bbox[2]),int(face.bbox[3]))
            img=frame[startY:endY, startX:endX]
            gender, age = get_age_gender(img)
            # age_text = get_age_gender1(img)
            label = f"{gender}, {age}"
            yPos = startY - 15
            while yPos < 15:
                yPos += 15
            cv2.rectangle(frame, (startX,startY), (endX,endY), color, 2)
            cv2.putText(frame, label, (startX, yPos), cv2.FONT_HERSHEY_SIMPLEX, fontScale, color, 2)

            # print(face.sex,face.age)
                # myCompare(face.embedding, embedding_list,face.age, face.sex)
                # print((face.embedding))
                # myem =str(face.embedding)
                # print((myem))
                # myem = np.fromstring(myem[1:-1], dtype=np.float32, sep=' ')
                # print(type(myem))
            # print(face.embedding,face.det_score)

        # Using cv2.putText() method
        frame = cv2.putText(frame, 'Odamlar soni: '+str(len(faces)), org, font,
                            fontScale, color, thickness, cv2.LINE_AA)
        # rimg = app.draw_on(frame, faces)
        cv2.imshow("Detected Objects", frame)

    except Exception as e:
        print(e)
        continue

#946144040
