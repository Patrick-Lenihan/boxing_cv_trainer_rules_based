# importing open cv for image processing and mediapipe for pose detection
import cv2
import mediapipe as mp
import time


# setting up the pose variable which contains the moddle used for pose detection
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose 
pose = mpPose.Pose()
#storeing the info about body landmarks in the previos frames
frame_info_dict = {"left":{"fist":[],"elbow":[]},"right":{"fist":[],"elbow":[]}}
#initialising some more global variables 
# cap contains the opencv webcame
cap = cv2.VideoCapture(0)
pTime = 0
# elbowX and Y contain the current coordenates of the elbow
elbowX = 0
elbowY = 0
elbowX2 = 0
elbowY2 = 0

def main():
	'''
	this the main fuction 
	it consists of a loop that executes shows and processes each frame
	'''
	while True:
		# first web cam input stored in numpy ndarray in img
		# results contain the coordenates of all the coordenates once found through the moddle
		img,results = apply_moddle_to_feed_frame()
		use_landmarks(img,results)

		#showing the webcam image on the users screen
		cv2.imshow("Image",img)

		# the rest is stopping the program if you press q
		if cv2.waitKey(1) & 0xFF ==ord('q'):
			break

	cap.release()
	#print(frame_info_dict["right"]["fist"])

def apply_moddle_to_feed_frame():
	'''
	that reads in the webcame image and applys the pose detection moddle to them returning
	web cam input stored in numpy ndarray in img
	results contain the coordenates of all the coordenates once found through the moddle

	'''
	sucess, img = cap.read()
	# image needs to be changed from bgr to rgb for the moddle to work
	imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
	# aplying the moddle
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
		else:
			print("right-jab")

def check_left_hand(img,id,landmark_zPos,landmark_xPos, landmark_yPos,elbowX2):
	if (id == 19) and (landmark_zPos < -450):
			cv2.circle(img,(landmark_xPos,landmark_yPos),10,(255,0,0),cv2.FILLED);
			#print(elbowX2)
			if (landmark_xPos - elbowX2) > 0:
				print("left-overhand")
			if (landmark_zPos < -525):
				print("left- jab")

def classify_position(elbowX,elbowY,img,id,height,width,channel,landmark_xPos, landmark_yPos, landmark_zPos):
	'''
	trying to classify the punch based on landmarks
	'''
	# if it is the right elbow then use set elbowX and Y to the x and y of the landmark
	elbowX2 = 0
	if id == 14:
		elbowX,elbowY = landmark_xPos,landmark_yPos
	if id == 13:
		elbowX2, elbowY2 = landmark_xPos,landmark_yPos
	#print(elbowX2)
	try:
		check_right_hand(img,id,landmark_zPos,landmark_xPos,elbowX,landmark_yPos)
		
	except Exception as e:
		#print(e)
		pass
	try:
		check_left_hand(img,id,landmark_zPos,landmark_xPos, landmark_yPos,elbowX2)
	except Exception as e:
		#print(e)
		pass
	return elbowX,elbowY
def loop_through_landmarks(img,results):
	'''
	this is a fuction that loops through
	each landmark and then runs the classify possition fuction which
	anyilys each landmark for classifycation
	'''
	elbowX = 1000
	elbowY = 1000
	for id, landmark in enumerate(results.pose_landmarks.landmark):
				height,width,channel = img.shape
				landmark_xPos, landmark_yPos, landmark_zPos = int(landmark.x*width), int(landmark.y*height), int(landmark.z*width)
				#cv2.circle(img,(landmark_xPos,landmark_yPos),10,(255,0,0),cv2.FILLED);
				elbowX,elbowY = classify_position(elbowX,elbowY,img,id,height,width,channel,landmark_xPos, landmark_yPos, landmark_zPos)
				
def use_landmarks(img,results):
	'''
	this function checks if the landmarks are found and then draws
	the landmarks on the top of the image stored in the img variable
	it then runs the loop_through landmarks function which gets info on each landmark
	'''
	if results.pose_landmarks:
			# draw the landmarks
			mpDraw.draw_landmarks(img,results.pose_landmarks,mpPose.POSE_CONNECTIONS) 
			loop_through_landmarks(img,results)

if __name__ == "__main__":
	main()
