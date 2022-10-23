import cv2
from sklearn.metrics.pairwise import cosine_similarity
from insightface.app import FaceAnalysis
import insightface
import numpy as np
from myDB import DBHelper



db=DBHelper()
embedding_list = db.getEmbed()



def cosSimi(a,b):
    try:
        return cosine_similarity(a.reshape(1,-1), b.reshape(1,-1))
    except Exception as ex:
        print("smilartiyda hato: ",ex)


def myCompare(vek,veks,age,gender):
    global embedding_list

    print("len emb: ",len(embedding_list))


    dist_list = [cosSimi(vek, x) for x in veks]
    # for index, emb_db in enumerate(veks):
    #     dist = cosSimi(vek, emb_db)
    #     dist_list.append(dist[0][0])
    # idx_min = dist_list.index(min(dist_list))
    # print(dist_list)
    if len(dist_list)>0:

        print("oxshashlik: ",min(dist_list))
        if min(dist_list) > 0.7:
            # print("bu odam bazada bor")


            #bu joyi bazada har bir odamning 10tadan rasmni saqlaydi
            inx_max = dist_list.index(max(dist_list))
            # print(inx_max)
            return db.addVisit(inx_max,age,gender,vek)

            # +1 ga oshirish kerak idsini topib
        else:
            # print("bu yangi odam")
            db.addPerson(age,gender,vek)
            # embedding_list = db.getEmbed()
            embedding_list.append(vek)
            return 1
            # +1 ga oshirish kerak idsini topib
    else:
        # print("bu yangi odam")
        db.addPerson(age, gender, vek)
        # embedding_list = db.getEmbed()
        embedding_list.append(vek)
        return 1
        # +1 ga oshirish kerak idsini topib


# detection
app = FaceAnalysis(allowed_modules=['detection','genderage','recognition'])
app.prepare(ctx_id=0, det_size=(640, 640), det_thresh=0.7)


cap = cv2.VideoCapture(0)
cv2.namedWindow("Detected Objects", cv2.WINDOW_NORMAL)
font = cv2.FONT_HERSHEY_SIMPLEX

# org
org = (20, 30)

# fontScale
fontScale = 0.5

# Blue color in BGR
color = (255, 0, 0)

# Line thickness of 2 px
thickness = 1


while cap.isOpened():

    # Press key q to stop
    if cv2.waitKey(1) == ord('q'):
        break

    try:
        ret, frame = cap.read()
        if not ret:
            break
        faces = app.get(frame)
        db.statusIkkiNol()
        for face in faces:
            startX, startY = (int(face.bbox[0]), int(face.bbox[1]))
            endX, endY = (int(face.bbox[2]), int(face.bbox[3]))
            # print(face.sex,face.age)
            soni = myCompare(face.embedding, embedding_list,face.age, face.sex)
            label = f"{soni} ,{face.gender} ,{face.age}"
            yPos = startY - 15
            while yPos < 15:
                yPos += 15
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
            cv2.putText(frame, label, (startX, yPos), cv2.FONT_HERSHEY_SIMPLEX, fontScale, color, 2)
                # print((face.embedding))
                # myem =str(face.embedding)
                # print((myem))
                # myem = np.fromstring(myem[1:-1], dtype=np.float32, sep=' ')
                # print(type(myem))
            # print(face.embedding,face.det_score)
        db.statusIkki()




        # rimg = app.draw_on(frame, faces)
        cv2.imshow("Detected Objects", frame)

    except Exception as e:
        print(e)

#946144040


























# _path = "./rasmlarAll/full.jpg"
# _path = "frame_out.jpg"
#
#
# img = cv2.imread(_path)
#
# faces = app.get(img)
# for face in faces:
#     print(face.bbox)
#     print(face.sex, face.age)
#
#
#
# # recognition
# img1= cv2.imread("myframe.jpg")
# handler = insightface.model_zoo.get_model("buffalo_sc")
# a = handler.get(img, faces[0])
# print(a) # ->> (512,)
# print(a-faces[0].embedding) # ->> (512,)
# yaqinlik = cosSimi(a,faces[0].embedding)
# print(yaqinlik[0][0],type(yaqinlik))
#
