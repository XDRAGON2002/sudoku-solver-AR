import cv2
import numpy as np
from tensorflow import keras
from solver.sudoku_solver_bfs import *

def CENTER(length,size) :
        
    if length % 2 == 0 :
        side1 = int((size - length) / 2)
        side2 = side1
    else :
        side1 = int((size - length) / 2)
        side2 = side1 + 1
    return (side1,side2)

def SCALE(r, x) :

    return int(r * x)

def CENTER_SCALE(image,size,margin = 20,background = 0) :
    
    img = image
    height,width = img.shape[:2]
    if height > width :
        toppad = int(margin / 2)
        bottompad = toppad
        ratio = (size - margin) / height
        width = SCALE(ratio,width)
        height = SCALE(ratio,height)
        leftpad,rightpad = CENTER(width,size)
    else :
        leftpad = int(margin / 2)
        rightpad = leftpad
        ratio = (size - margin) / width
        width = SCALE(ratio,width)
        height = SCALE(ratio,height)
        toppad, bottompad = CENTER(height,size)
    img = cv2.resize(img,(width,height))
    img = cv2.copyMakeBorder(img,toppad,bottompad,leftpad,rightpad,cv2.BORDER_CONSTANT,None,background)
    img = cv2.resize(img,(size,size))
    return img

def SHOW(image) :

    cv2.imshow("pic",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def GET_SUDOKU(image) :

    img = image
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(9,9),0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    thresh = cv2.bitwise_not(thresh)
    kernel = np.array([[0.,1.,0.],[1.,1.,1.,],[0.,1.,0.]],np.uint8)
    thresh = cv2.dilate(thresh,kernel)
    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours,key = cv2.contourArea,reverse = True)
    sudoku = None
    for contour in contours :
        perimeter = cv2.arcLength(contour,True)
        approx = cv2.approxPolyDP(contour,0.02 * perimeter,True)
        if (len(approx) == 4) :
            sudoku = approx
            break
    return (sudoku,img)

def GET_PERSPECTIVE(sudoku,image) :

    orderedpoints = np.zeros((4,2),dtype = np.int32)
    unorderedpoints = sudoku.reshape((4,2))
    summation = unorderedpoints.sum(1)
    orderedpoints[0] = unorderedpoints[np.argmin(summation)]
    orderedpoints[3] = unorderedpoints[np.argmax(summation)]
    difference = np.diff(unorderedpoints,axis = 1)
    orderedpoints[1] = unorderedpoints[np.argmin(difference)]
    orderedpoints[2] = unorderedpoints[np.argmax(difference)]
    width = 28 * 9
    height = 28 * 9
    points1 = np.float32(orderedpoints)
    points2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
    m = cv2.getPerspectiveTransform(points1,points2)
    warp = cv2.warpPerspective(image,m,(width,height))
    return (warp,points1,points2,unorderedpoints)

def GET_CELLS(warp) :

    sudoku = warp
    gray = cv2.cvtColor(sudoku,cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,101,1)
    thresh = cv2.bitwise_not(thresh)
    cellheight = thresh.shape[0] // 9
    cellwidth = thresh.shape[1] // 9
    cells = [[0 for i in range(9)] for j in range(9)]
    for i in range(9) :
        for j in range(9) :
            cells[i][j] = thresh[(i) * cellheight:(i + 1) * cellheight,(j) * cellwidth:(j + 1) * cellwidth]
    return cells

def GET_DIGITS(cells) :

    cnn_model = keras.models.load_model("solver/ocr_model.h5")
    unsolved = [[0 for i in range(9)] for j in range(9)]
    for i in range(9) :
        for j in range(9) :
            cell = cells[i][j]
            cell = cv2.resize(cell,(32,32))
            thresh = cv2.threshold(cell,128,255,cv2.THRESH_BINARY)[1]
            contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 
            for contour in contours :
                x,y,w,h = cv2.boundingRect(contour)
                if (x < 3 or y < 3 or w < 3 or h < 3) :
                    continue
                else :
                    digit = thresh[y:y + h,x:x + w]
                    digit = CENTER_SCALE(digit,120)
                    digit = cv2.resize(digit,(32,32))
                    digit = digit.astype("float32")
                    digit = digit.reshape(1,32,32,1)
                    digit /= 255
                    prediction = cnn_model.predict(digit.reshape(1,32,32,1),batch_size = 1)
                    unsolved[i][j] = prediction.argmax()
    return unsolved

def DRAW_SOLVED(solved,image) :

    draw = image
    if not solved:
        draw = cv2.putText(draw,str("UNSOLVED"),(draw.shape[0] // 4,draw.shape[1] // 2),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)
        return draw
    cellheight = draw.shape[0] // 9
    cellwidth = draw.shape[1] // 9
    for i in range(9) :
        for j in range(9) :
            draw = cv2.putText(draw,str(solved[i][j]),((i) * cellheight + 5,(j + 1) * cellwidth - 5),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)
    return draw

def PUT_PERSPECTIVE(image,draw,points1,points2,contour) :

    width = image.shape[1]
    height = image.shape[0]
    m = cv2.getPerspectiveTransform(points2,points1)
    final = cv2.warpPerspective(draw,m,(width,height))
    img = cv2.fillPoly(image,[contour],(0,0,0))
    final = cv2.bitwise_or(final,img)
    cv2.drawContours(final,[contour],-1,(0,255,0),2) # BORDER
    return final