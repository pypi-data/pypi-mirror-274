# original faceLandmarks is from: https://pysource.com/blur-faces-in-real-time-with-opencv-mediapipe-and-python
# this is for single person face extraction built by takefuji
import mediapipe as mp
import cv2,sys,re
import numpy as np

mode=127
st=""
rr=""
for i in range(1,len(sys.argv)):
 st=st+' '+str(sys.argv[i])
if re.search('-W',st):
 mode=255
 rr=st.replace('-W','')
elif re.search('-B',st):
 mode=0
 rr=st.replace('-B','')
elif re.search('-G',st):
 mode=127
 rr=st.replace('-G','')
else: rr=st

class FaceLandmarks:
    def __init__(self):
        mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = mp_face_mesh.FaceMesh()

    def get_facial_landmarks(self, frame):
        height, width, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.face_mesh.process(frame_rgb)
        facelandmarks = []
        try:
         for facial_landmarks in result.multi_face_landmarks:
            for i in range(0, 468):
                pt1 = facial_landmarks.landmark[i]
                x = int(pt1.x * width)
                y = int(pt1.y * height)
                facelandmarks.append([x, y])
         return np.array(facelandmarks, np.int32)
        except TypeError:
         return np.array([])
        else: #added by takefuji 
         return np.array([])
cam = cv2.VideoCapture(0)

while True:
 r,img = cam.read()
 height, width, _ = img.shape
 img=cv2.flip(img,1)
 img_copy=img.copy()
 fl = FaceLandmarks()
 landmarks = fl.get_facial_landmarks(img)
 if cv2.waitKey(1) == ord('q'): break
 if len(landmarks)==0:
  img=face
  if mode==255 or mode==127:cv2.putText(img,rr, (24, 54), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)
  if mode==0:cv2.putText(img,rr, (24, 54), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
  cv2.imshow('result',img)
  cv2.waitKey(1)
 else:
  if cv2.waitKey(1) == ord('q'): break
  convexhull = cv2.convexHull(landmarks)
  mask = np.zeros((height, width), np.uint8)
  cv2.polylines(mask, [convexhull], True, 255, 3)
  cv2.fillConvexPoly(mask, convexhull, 255)
  face_ext = cv2.bitwise_and(img_copy, img_copy, mask=mask)
  face_ext[face_ext==0]=mode
  if mode==255 or mode==127:cv2.putText(face_ext, rr, (24, 54), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)
  if mode==0:cv2.putText(face_ext, rr, (24, 54), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
  cv2.moveWindow('result',10,10)
  cv2.imshow('result', face_ext )
  face=face_ext
  cv2.waitKey(1)
cv2.destroyAllWindows()
