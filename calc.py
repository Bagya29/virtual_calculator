import cv2
import os
import math
from cvzone.HandTrackingModule import HandDetector
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'


class Button:
    def __init__(self, position, width, height, value):
        self.position = position
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        cv2.rectangle(img, self.position, (self.position[0] + self.width, self.position[1] + self.height),
                      (225, 225, 225), cv2.FILLED)
        cv2.rectangle(img, self.position, (self.position[0] + self.width, self.position[1] + self.height),
                      (50, 50, 50), 3)
        cv2.putText(img, str(self.value), (self.position[0] + 35, self.position[1] + 70), cv2.FONT_HERSHEY_COMPLEX, 2,
                    (50, 50, 50), 2)

    def checkclick(self, x, y):
        if self.position[0] < x < self.position[0] + self.width and self.position[1] < y < self.position[1] + self.height:
            cv2.rectangle(img, self.position, (self.position[0] + self.width, self.position[1] + self.height),
                          (255, 255, 255), cv2.FILLED)
            cv2.rectangle(img, self.position, (self.position[0] + self.width, self.position[1] + self.height),
                          (50, 50, 50), 3)
            cv2.putText(img, str(self.value), (self.position[0] + 25, self.position[1] + 80),
                        cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 0), 3)
            return True
        else:
            return False



#web cam
cap=cv2.VideoCapture(0)
cap.set(3,1280) #width
cap.set(4,720) #height
detector=HandDetector(detectionCon=0.8,maxHands=1)


#creating Buttons
buttonlistvalues=[["7" ,"8" ,"9" ,"*"],
                  ["4" ,"5" ,"6" ,"-"],
                  ["1" ,"2" ,"3" ,"+"],
                  ["0" ,"/" ,"." ,"="]]




buttonlist=[]
for x in range(4):
    for y in range(4):
        xpos=x*100+800
        ypos=y*100+150
        buttonlist.append(Button((xpos,ypos),100,100,buttonlistvalues[y][x]))



#variables
# ... (previous code)

#variables
# ... (previous code)

# Variables
# ... (previous code)

# Variables
myequation = ""
length = 0
delay_counter = 0  # Introduce a delay counter for visual feedback

while True:
    # to get image from web cam
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # detection of hand
    hands, img = detector.findHands(img, flipType=False)

    # draw all buttons
    cv2.rectangle(img, (800, 50), (800 + 400, 70 + 100), (225, 225, 225), cv2.FILLED)
    cv2.rectangle(img, (800, 50), (800 + 400, 70 + 100), (50, 50, 50), 3)
    for button in buttonlist:
        button.draw(img)

    # Check for hand
    if hands:
        lmList = hands[0]['lmList']
        point1 = (lmList[8][0], lmList[8][1])
        point2 = (lmList[12][0], lmList[12][1])
        length = math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)
        img_with_line = cv2.line(img.copy(), point1, point2, (0, 255, 0), 2)
        x, y, _ = lmList[8] = lmList[8]

        # Click handling
        if length < 60 and delay_counter == 0:
            for i, button in enumerate(buttonlist):
                if button.checkclick(x, y):
                    myvalue = buttonlistvalues[int(i % 4)][int(i / 4)]
                    if myvalue == "=":
                        try:
                            myequation = str(eval(myequation))
                        except Exception as e:
                            myequation = "Error: " + str(e)
                    else:
                        myequation += str(myvalue)
                    delay_counter = 10
                

    # Visual feedback delay
    if delay_counter > 0:
        delay_counter -= 1

    # Processing

    # Display the result
    cv2.putText(img, myequation, (810, 120), cv2.FONT_HERSHEY_COMPLEX, 2, (50, 50, 50), 2)

    # Display image
    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()