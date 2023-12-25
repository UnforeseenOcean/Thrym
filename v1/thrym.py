from vidgear.gears import ScreenGear
import cv2
import pyautogui
import pygetwindow as gw
import numpy as np
from decimal import Decimal
import sys
import platform
import time

# Check if we are running lower version of Python and exit, as we need Python 3.10 or higher
if sys.version_info[0] <= 3 and sys.version_info[1] < 10:
    print("FATAL ERROR: SHIT'S FUCKED")
    raise EnvironmentError("ERROR: Please use Python 3.10 and above!")
    sys.exit(0)

pyautogui.PAUSE = 0.05
# It's stupid, just ignore the names and use x1, y1, x2, y2
options = {"left": 500, "top": 500, "width": 1920, "height": 1080}
# Rune detection area: 120W 40H

# Viewing area setup
# area1 = (40, 200, 160, 250)
# area2 = (280, 200, 400, 250)
# area3 = (514, 200, 634, 250)
# area4 = (750, 200, 870, 250)

area1 = (40, 190, 160, 250)
area2 = (280, 200, 400, 250)
area3 = (514, 200, 634, 250)
area4 = (750, 190, 870, 250)
shield = (1285, 410, 1385, 555)

# Overlay text position
text1 = (75, 180)
text2 = (315, 180)
text3 = (550, 180)
text4 = (800, 180)
text5 = (1320, 390)
overlayFontScale = 2

# Key status text position
# S
keyText1 = (30, 445)
# Q
keyText2 = (78, 445)
# W
keyText3 = (128, 445)
# E
keyText4 = (180, 445)
# I
keyText5 = (225, 445)
# O
keyText6 = (245, 445)
# P
keyText7 = (290, 445)
# Space
keyText8 = (330, 445)
keyDispFontScale = 2

# OpenCV misc settings
font=cv2.FONT_HERSHEY_SIMPLEX
idleColor = (255, 0, 0)
seenColor = (0, 255, 0)
hitColor = (0, 0, 255)
keyIdleColor = (0, 255, 0)
drumLvl0 = (128, 128, 128)
drumLvl1 = (255, 255, 0)
drumLvl2 = (0, 255, 255)
lineWidth = 4

# Window title detection
targetWin = "Ragnarock "

# State machine global variable
sm_Shield = 0
sm_Keys = 0

stream = ScreenGear(logging=True, **options).start()
stream.color_space = cv2.COLOR_BGR2RGB

def isNotePresent(frame):
    # Hack: Flip "RGB" image to "BGR"
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    # Create subframes
    nv1 = frame[area1[1]:area1[3], area1[0]:area1[2]]
    nv2 = frame[area2[1]:area2[3], area2[0]:area2[2]]
    nv3 = frame[area3[1]:area3[3], area3[0]:area3[2]]
    nv4 = frame[area4[1]:area4[3], area4[0]:area4[2]]
    # Convert subframes to grayscale for the brightness comparison
    # This is a very inefficient way to do this, but at this point who cares
    noteROI1 = cv2.cvtColor(nv1, cv2.COLOR_BGR2GRAY)
    noteROI2 = cv2.cvtColor(nv2, cv2.COLOR_BGR2GRAY)
    noteROI3 = cv2.cvtColor(nv3, cv2.COLOR_BGR2GRAY)
    noteROI4 = cv2.cvtColor(nv4, cv2.COLOR_BGR2GRAY)
    # Convert subframes to HSV colorspace for color comparison later
    # This is also not recommended way to do it
    nvA = cv2.cvtColor(nv1, cv2.COLOR_BGR2HSV_FULL)
    nvB = cv2.cvtColor(nv2, cv2.COLOR_BGR2HSV_FULL)
    nvC = cv2.cvtColor(nv3, cv2.COLOR_BGR2HSV_FULL)
    nvD = cv2.cvtColor(nv4, cv2.COLOR_BGR2HSV_FULL)
    # Tune this part to avoid triggering on hammer and camera shakes as well as ship
    # Please do not do this 
    (xnvv, thres1) = cv2.threshold(noteROI1, 64, 255, 0)
    (vfnd, thres2) = cv2.threshold(noteROI2, 64, 255, 0)
    (mzmc, thres3) = cv2.threshold(noteROI3, 64, 255, 0)
    (eiak, thres4) = cv2.threshold(noteROI4, 64, 255, 0)
    # Blur subframes to reduce noise
    # Inefficiency etc.
    blur1 = cv2.GaussianBlur(thres1, (3, 3), 0)
    blur2 = cv2.GaussianBlur(thres2, (3, 3), 0)
    blur3 = cv2.GaussianBlur(thres3, (3, 3), 0)
    blur4 = cv2.GaussianBlur(thres4, (3, 3), 0)
    # Finally apply Otsu's Threshold to clean up image
    vnmds, final1 = cv2.threshold(blur1, -1, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    ozdck, final2 = cv2.threshold(blur2, -1, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    kakde, final3 = cv2.threshold(blur3, -1, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    lglfe, final4 = cv2.threshold(blur4, -1, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # Look for white things in image
    mean_V1 = np.mean(final1[:, :])
    mean_V2 = np.mean(final2[:, :])
    mean_V3 = np.mean(final3[:, :])
    mean_V4 = np.mean(final4[:, :])
    # What is the color closest to?
    mean_H1 = np.mean(nv1[:, :, 0])
    mean_H2 = np.mean(nv2[:, :, 0])
    mean_H3 = np.mean(nv3[:, :, 0])
    mean_H4 = np.mean(nv4[:, :, 0])
    # Put the results in an array so they're easy to use
    v_list = [mean_V1, mean_V2, mean_V3, mean_V4]
    h_list = [mean_H1, mean_H2, mean_H3, mean_H4]
    # Set color upper and lower bounds
    blueBound = [100,160]
    blueBoundLR=[90,160]
    lumaBound = [60,254]
    lumaBoundLR=[40,254]
    # Initialize result array
    result = [False, False, False, False]
    # Do maths
    # for x in range(len(result)):
        # if blueBound[0] <= h_list[x] <= blueBound[1] and lumaBound[0] <= v_list[x] <= lumaBound[1]:
            # result[x] = True
        # else:
            # result[x] = False
    # Incredibly stupid way to do this
    if blueBoundLR[0] <= h_list[0] <= blueBoundLR[1] and lumaBoundLR[0] <= v_list[0] <= lumaBoundLR[1]:
        result[0] = True
    if blueBound[0] <= h_list[1] <= blueBound[1] and lumaBound[0] <= v_list[1] <= lumaBound[1]:
        result[1] = True
    if blueBound[0] <= h_list[2] <= blueBound[1] and lumaBound[0] <= v_list[2] <= lumaBound[1]:
        result[2] = True
    if blueBoundLR[0] <= h_list[3] <= blueBoundLR[1] and lumaBoundLR[0] <= v_list[3] <= lumaBoundLR[1]:
        result[3] = True
    
    #cv2.imshow("Note View", frame)
    cv2.imshow("First Note", final1)
    cv2.imshow("Second Note", final2)
    cv2.imshow("Third Note", final3)
    cv2.imshow("Fourth Note", final4)
    
    print("H1:",Decimal(mean_H1).quantize(Decimal("1.0000")),"H2:",Decimal(mean_H2).quantize(Decimal("1.0000")),"H3:",Decimal(mean_H3).quantize(Decimal("1.0000")),"H4:",Decimal(mean_H4).quantize(Decimal("1.0000")),"V1:",Decimal(mean_V1).quantize(Decimal("1.0000")),"V2:",Decimal(mean_V2).quantize(Decimal("1.0000")),"V3:",Decimal(mean_V3).quantize(Decimal("1.0000")),"V4:",Decimal(mean_V4).quantize(Decimal("1.0000")))
    return result

def isShieldActive(frame, x1, y1, x2, y2):
    # Trim input frame to size
    frame = frame[y1:y2, x1:x2]
    # Hack: Flip "RGB" image to "BGR"
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    # Convert input frame to HSV colorspace
    colorbug = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
    # Convert this one to grayscale for the brightness comparison
    shieldROI = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Tune this part to avoid triggering on hammer and camera shakes
    (asdf, thres) = cv2.threshold(shieldROI, 127, 255, 0)
    # Blur image to reduce noise
    blur = cv2.GaussianBlur(thres, (3, 3), 0)
    # Finally apply Otsu's Threshold to clean up image
    aaaaa, final = cv2.threshold(blur, -1, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # Look for white things in image
    mean_V = np.mean(final[:, :])
    # What is the color closest to?
    mean_H = np.mean(colorbug[:, :, 0])
    # Set color upper and lower bounds
    yellowBound = [26,44]
    cyanBound = [100,145]
    lumaBound = [25, 40]
    # lumaBound = [25, 140]
    # Initialize variables
    isActive = False
    comboLevel = 0
    # Apply logic to prevent most of the false positives
    if lumaBound[0] <= mean_V <= lumaBound[1]:
        isActive = True
    else:
        isActive = False
    # Do maths
    if cyanBound[0] <= mean_H <= cyanBound[1]:
    # if isBlue == True and isYellow == False:
        comboLevel = 1
    elif yellowBound[0] <= mean_H <= yellowBound[1]:
    # elif isBlue == False and isYellow == True:
        comboLevel = 2
    else:
        isActive = False
        comboLevel = 0
    # print("Hue:", Decimal(mean_H).quantize(Decimal("1.0000")), "Brightness:", Decimal(mean_V).quantize(Decimal("1.0000")), "isActive:", isActive, "Level:", comboLevel)
    return (isActive, comboLevel)
    
def updateNotesColor(value):
    if value == 0:
        return idleColor
    elif value == 1:
        return seenColor
    elif value == 2:
        return hitColor
    else:
        return idleColor

def updateShieldColor(value):
    if value == 0:
        return drumLvl0
    elif value == 1:
        return drumLvl1
    elif value == 2:
        return drumLvl2
    else:
        return drumLvl0

def updateKeyColor(status):
    if status == True:
        return hitColor
    else:
        return keyIdleColor

def toTuple(data):
    return tuple(data)

def createKeys(inputList):
    # List valid key combinations
    in_valid = [(False, False, False, False), (True, False, False, False), (False, True, False, False), (False, False, True, False), (False, False, False, True), (True, True, False, False), (True, False, True, False), (True, False, False, True), (False, True, False, True), (False, True, True, False), (False, False, True, True)]
    #int_valid = [[False, False, False, False], [True, False, False, False], [False, True, False, False], [False, False, True, False], [False, False, False, True], [True, True, False, False], [True, False, True, False], [True, False, False, True], [False, True, False, True], [False, True, True, False], [False, False, True, True]]
    
    # If input is all False, do not do anything and send empty list
    if not any(inputList):
        return []
    # If input is all True, then send empty list
    if all(inputList):
        return []
    # Catch malformed list with less than 4 or more than 4 values
    if len(inputList) != 4:
        raise ValueError("Something went wrong!! Input length incorrect!!")
    # Catch malformed list with non-Boolean values
    if not all(isinstance(value, bool) for value in inputList):
        raise ValueError("ERROR: Incorrect list content, acceptable type: Bool.")
        
    # If input has 3 True values...
    if inputList.count(True) == 3:
        # Change the rightmost True value to False
        # inputList[inputList.index(True, 0, 3)] = False
        # Even dumber approach
        if inputList == [True, True, True, False]:
            inputList = [True, True, False, False]
        elif inputList == [False, True, True, True]:
            inputList = [False, False, True, True]
        
    # Lookup table for output
    keystrokes = { 
        (False, False, False, False): [],
        (True, False, False, False): ["q"], 
        (False, True, False, False): ["w"], 
        (False, False, True, False): ["o"], 
        (False, False, False, True): ["p"], 
        (True, True, False, False): ["q", "i"], 
        (True, False, True, False): ["q", "o"], 
        (True, False, False, True): ["q", "p"], 
        (False, True, False, True): ["w", "p"], 
        (False, True, True, False): ["w", "o"], 
        (False, False, True, True): ["e", "p"]
        }
    
    keyResult = keystrokes.get(tuple(inputList), [])
    
    return keyResult

while True:
    
    # Try to get the frame
    frame = stream.read()
    # Kill thread if frame cannot be retrieved
    if frame is None:
	    break
	# Image processing code goes here and here only
    shieldStatus = isShieldActive(frame, *shield)
    noteStats = isNotePresent(frame)
    # if any(noteStats):
        # print("Notes:", noteStats, "Shield:", shieldStatus)
    # Hack to convert "RGB" colors back to true colors as it is flipped in the source
    # Note that any image processing commands placed after this line will have corrupted color
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    color1 = updateNotesColor(noteStats[0])
    color2 = updateNotesColor(noteStats[1])
    color3 = updateNotesColor(noteStats[2])
    color4 = updateNotesColor(noteStats[3])
    if shieldStatus[0] == True:
        color5 = updateShieldColor(shieldStatus[1])
    else:
        color5 = updateShieldColor(0)
    
    # S, Q, W, E, I, O, P, Space
    keyState = (False, False, False, False, False, False, False, False)
    cwin = gw.getWindowsWithTitle(targetWin)
    if cwin is not None:
        isSafe = cwin[0].isActive
    # print(isSafe)
    # Only send the keystrokes to game window
    if isSafe == True:
        # Do things to ensure only two keys are pressed at the same time
        
        safeKeys = createKeys(noteStats)
        
        ts0 = safeKeys.count("q")
        ts1 = safeKeys.count("w")
        ts2 = safeKeys.count("e")
        ts3 = safeKeys.count("i")
        ts4 = safeKeys.count("o")
        ts5 = safeKeys.count("p")        
        
        keyState = (False, bool(ts0), bool(ts1), bool(ts2), bool(ts3), bool(ts4), bool(ts5), False);
        # Time to send the keys
        if len(safeKeys) > 0:
            # print(safeKeys)
            # Adjust delay
            # time.sleep(0.02)
            pyautogui.press(safeKeys)
        # If it manages to build up enough combos, try to use it
        if shieldStatus[0] == True:
            sm_Shield += 1
            if sm_Shield > 8:
                pyautogui.press("s")
                pyautogui.press("space")
                # Reset state machine to 0
                sm_Shield = 0
    #else:
        # print("WARN: Window not in focus! No keystrokes will be sent.")
        
    colorS = updateKeyColor(keyState[0])
    colorQ = updateKeyColor(keyState[1])
    colorW = updateKeyColor(keyState[2])
    colorE = updateKeyColor(keyState[3])
    colorI = updateKeyColor(keyState[4])
    colorO = updateKeyColor(keyState[5])
    colorP = updateKeyColor(keyState[6])
    colorSP = updateKeyColor(keyState[7])
    
    # Draw OSD
    cv2.rectangle(frame, (int(area1[0]), int(area1[1])), (int(area1[2]), int(area1[3])), color=color1, thickness=lineWidth)
    cv2.rectangle(frame, (int(area2[0]), int(area2[1])), (int(area2[2]), int(area2[3])), color=color2, thickness=lineWidth)
    cv2.rectangle(frame, (int(area3[0]), int(area3[1])), (int(area3[2]), int(area3[3])), color=color3, thickness=lineWidth)
    cv2.rectangle(frame, (int(area4[0]), int(area4[1])), (int(area4[2]), int(area4[3])), color=color4, thickness=lineWidth)
    cv2.rectangle(frame, (int(shield[0]), int(shield[1])), (int(shield[2]), int(shield[3])), color=color5, thickness=lineWidth)
    
    cv2.putText(frame, "1", text1, font, overlayFontScale, color1, 6)
    cv2.putText(frame, "2", text2, font, overlayFontScale, color2, 6)
    cv2.putText(frame, "3", text3, font, overlayFontScale, color3, 6)
    cv2.putText(frame, "4", text4, font, overlayFontScale, color4, 6)
    cv2.putText(frame, "S", text5, font, overlayFontScale, color5, 6)
    
    cv2.putText(frame, "S", keyText1, font, keyDispFontScale, colorS, 6)
    cv2.putText(frame, "Q", keyText2, font, keyDispFontScale, colorQ, 6)
    cv2.putText(frame, "W", keyText3, font, keyDispFontScale, colorW, 6)
    cv2.putText(frame, "E", keyText4, font, keyDispFontScale, colorE, 6)
    cv2.putText(frame, "I", keyText5, font, keyDispFontScale, colorI, 6)
    cv2.putText(frame, "O", keyText6, font, keyDispFontScale, colorO, 6)
    cv2.putText(frame, "P", keyText7, font, keyDispFontScale, colorP, 6)
    cv2.putText(frame, "_", keyText8, font, keyDispFontScale, colorSP, 6)
    
    cv2.putText(frame, "Played by Thrym - Automated Playthrough", (20, 530), font, 1, (0, 0, 255), 2)
    
    
    cv2.imshow("Thrym", frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord("z"):
        break

cv2.destroyAllWindows()
