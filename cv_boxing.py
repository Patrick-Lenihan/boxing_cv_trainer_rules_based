import cv2
import mediapipe as mp
import time

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose 
pose = mpPose.Pose()
frame_info_dict = {"left":{"fist":[],"elbow":[]},"right":{"fist":[],"elbow":[]}}
cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('channel:/Users/User/Pictures/Video Projects/anne_birthdaycur.wmv')
pTime = 0
elbowX = 0
elbowY = 0

def main():
	while True:
		img,results = apply_moddle_to_feed_frame()
		use_landmarks(img,results)

		
		cv2.imshow("Image",img)#cv2.waitKey(1)
		if cv2.waitKey(1) & 0xFF ==ord('q'):
			break

	cap.release()
	#print(frame_info_dict["right"]["fist"])


def apply_moddle_to_feed_frame():
	sucess, img = cap.read()
	imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
	results = pose.process(imgRGB)
	return img , results
def draw_circle_on_fist(img,landmark_xPos,landmark_yPos):
	cv2.circle(img,(landmark_xPos,landmark_yPos),10,(255,0,0),cv2.FILLED);
def check_right_hand(img,id,landmark_zPos,landmark_xPos,elbowX,landmark_yPos):
	is_right_hand_punching = (id == 20) and (landmark_zPos < -450)
	if is_right_hand_punching:
		draw_circle_on_fist(img,landmark_xPos,landmark_yPos)
		if (landmark_xPos - elbowX) > 40:
			print("right-hook")

		elif (elbowX - landmark_xPos) > 40:
			print("overhand-right")


def classify_position(elbowX,elbowY,img,id,height,width,channel,landmark_xPos, landmark_yPos, landmark_zPos):
	if id == 14:
		elbowX,elbowY = landmark_xPos,landmark_yPos

	try:
		check_right_hand(img,id,landmark_zPos,landmark_xPos,elbowX,landmark_yPos)
		
		if (id == 19) and (landmark_zPos < -525):
			cv2.circle(img,(landmark_xPos,landmark_yPos),10,(255,0,0),cv2.FILLED);
	except Exception as e:
		print(e)
		pass
	return elbowX,elbowY
def loop_through_landmarks(img,results):
	elbowX = 1000
	elbowY = 1000
	for id, landmark in enumerate(results.pose_landmarks.landmark):
				height,width,channel = img.shape
				landmark_xPos, landmark_yPos, landmark_zPos = int(landmark.x*width), int(landmark.y*height), int(landmark.z*width)
				#cv2.circle(img,(landmark_xPos,landmark_yPos),10,(255,0,0),cv2.FILLED);
				elbowX,elbowY = classify_position(elbowX,elbowY,img,id,height,width,channel,landmark_xPos, landmark_yPos, landmark_zPos)
				
def use_landmarks(img,results):
	if results.pose_landmarks:
			#print(results.pose_landmarks)
			# draw the landmarks
			mpDraw.draw_landmarks(img,results.pose_landmarks,mpPose.POSE_CONNECTIONS) 
			loop_through_landmarks(img,results)

main()
