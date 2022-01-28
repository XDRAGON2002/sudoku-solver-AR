import time
from flask import Flask
from flask_socketio import SocketIO, emit
import io
import cv2
import numpy as np
import pybase64 as base64
from PIL import Image
from solver.ocr import *

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/', methods=['GET'])
def index():
    return "Works"

@socketio.on('image')
def image(data_image):
    sbuf = io.StringIO()
    sbuf.write(data_image)

    # decode and convert into image
    b = io.BytesIO(base64.b64decode(data_image))
    pimg = Image.open(b)

    ## converting RGB to BGR, as opencv standards
    frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)
    sudoku,image = GET_SUDOKU(frame)
    warp,points1,points2,contour = GET_PERSPECTIVE(sudoku,image)
    cells = GET_CELLS(warp)
    unsolved = GET_DIGITS(cells)
    solved = SOLVE(unsolved)
    draw = DRAW_SOLVED(solved,warp)
    image = PUT_PERSPECTIVE(image,draw,points1,points2,contour)
    imgencode = cv2.imencode('.jpg', image)[1]

    # base64 encode
    stringData = base64.b64encode(imgencode).decode('utf-8')
    b64_src = 'data:image/jpg;base64,'
    stringData = b64_src + stringData

    # emit the frame back
    emit('response_back', stringData)
    if solved:
        time.sleep(10)


if __name__ == '__main__':
    socketio.run(app)