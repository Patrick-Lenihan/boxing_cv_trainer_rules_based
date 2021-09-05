import cv2
import mediapipe as mp
import time

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose 
pose = mpPose.Pose()
frame_info_dict = {"left":{"fist":[],"elbow":[]},"right":{"fist":[],"elbow":[]}}
cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('C:/Users/User/Pictures/Video Projects/anne_birthdaycur.wmv')
pTime = 0
elbowX = 0
elbowY = 0

def main():
	while True:
		sucess, img = cap.read()
		imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
		results = pose.process(imgRGB)
		if results.pose_landmarks:
			#print(results.pose_landmarks)
			mpDraw.draw_landmarks(img,results.pose_landmarks,mpPose.POSE_CONNECTIONS)
			for id, landmark in enumerate(results.pose_landmarks.landmark):
				h,w,c = img.shape
				cx, cy, cz = int(landmark.x*w), int(landmark.y*h), int(landmark.z*w)
				#cv2.circle(img,(cx,cy),10,(255,0,0),cv2.FILLED);
				if (id == 20) and (cz < -450):
					#print("id:", id);
					#print("x: ",cx);
					#print("y: ",cy);
					#print("z",cz);
					cv2.circle(img,(cx,cy),10,(255,0,0),cv2.FILLED);
					#frame_info_dict["right"]["fist"].append([cx,cy,cz])
					#print("elbowX",elbowX)
					#print("elbowY",elbowY)
					if (cx - elbowX) > 40:
						print("right-hook")

					elif (elbowX - cx) > 40:
						print("overhand-right")

				if (id == 19) and (cz < -525):
					#print("id:", id);
					#print("x: ",cx);
					#print("y: ",cy);
					#print("z",cz);
					cv2.circle(img,(cx,cy),10,(255,0,0),cv2.FILLED);
					#frame_info_dict["left"]["fist"].append([cx,cy,cz])

				if id == 14:
					elbowX,elbowY = cx,cy

		cv2.imshow("Image",img)
		#cv2.waitKey(1)
		if cv2.waitKey(1) & 0xFF ==ord('q'):
			break

	cap.release()
	print(frame_info_dict["right"]["fist"])
main()