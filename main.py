import cv2
from ocr import *

# TO GET SOLVED SUDOKU ON IMAGE
def SOLVE_IMAGE() :

    start = cv2.imread("sudoku.jpeg")
    sudoku,image = GET_SUDOKU(start)
    warp,points1,points2,contour = GET_PERSPECTIVE(sudoku,image)
    cells = GET_CELLS(warp)
    unsolved = GET_DIGITS(cells)
    solved = SOLVE(unsolved)
    draw = DRAW_SOLVED(solved,warp)
    image = PUT_PERSPECTIVE(image,draw,points1,points2,contour)
    SHOW(image)

# TO GET SOLVED SUDOKU IN REALTIME AUGMENTED REALITY
def SOLVE_VIDEO() :
    vid = cv2.VideoCapture(0)
    while (True) :
        ret,frame = vid.read()
        sudoku,image = GET_SUDOKU(frame)
        warp,points1,points2,contour = GET_PERSPECTIVE(sudoku,image)
        cells = GET_CELLS(warp)
        unsolved = GET_DIGITS(cells)
        solved = SOLVE(unsolved)
        draw = DRAW_SOLVED(solved,warp)
        frame = PUT_PERSPECTIVE(image,draw,points1,points2,contour)   
        cv2.imshow("frame",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    vid.release()
    cv2.destroyAllWindows()

choice = int(input("1 - SOLVE IMAGE\n2 - SOLVE VIDEO\nENTER CHOICE - "))
if choice == 1 :
    SOLVE_IMAGE()
elif choice == 2 :
    SOLVE_VIDEO()
else :
    print("INVALID CHOICE")