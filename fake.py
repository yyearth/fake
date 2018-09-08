#!/usr/bin/python3
# -*- coding:utf-8 -*-


import numpy as np
import cv2
import pickle
import threading

data = []
piece = []
squflag = False


def drawafra(fra, data):
    for i in range(len(data)):
        if (i-1) % 2 == 0:
            cv2.rectangle(fra, data[i - 1], data[i], (0, 255, 0), 2)
    cv2.putText(fra, 'People: %d' % (len(data)//4), (80, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
    out.write(fra)


def mouse_action(event, x, y, flags, param):
    global squflag
    # print(event, x, y, flags)
    if event == cv2.EVENT_LBUTTONUP:
        piece.append((x, y))
        if squflag:
            cv2.rectangle(frame, piece[-2], piece[-1], (0, 255, 0), 2)
            squflag = False
        else:
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
            squflag = True
    if event == cv2.EVENT_RBUTTONDOWN:
        pass


if __name__ == '__main__':
    endflag = False
    cap = cv2.VideoCapture('capt20180523_222642.avi')  # 935 frames
    ret, frame = cap.read()
    i = 0
    h, w, c = frame.shape
    print(w, h)
    # cap = cv2.VideoCapture('capt20180515_165348.avi')
    cv2.namedWindow('img', cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback('img', mouse_action)
    out = cv2.VideoWriter('out.avi', -1, 20.0, (w, h))
    out.write(frame)
    while True:
        ret, frame = cap.read()
        outframe = frame.copy()
        if endflag == True: ret = False
        if ret:
            i = i + 1
            cv2.putText(frame, '%d' % i, (80, h - 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
            while True:

                cv2.imshow('img', frame)
                key = cv2.waitKey(1)
                if key == 32:
                    data.append(piece)
                    threading.Thread(target=drawafra, args=(outframe, piece)).start()
                    piece = []
                    break
                elif key == 27:
                    endflag = True
                    print(data)
                    print('data len:', len(data))
                    break
                # elif key == ord('s'):
                #     cv2.imwrite('sample' + str(i) + '.jpg', frame)
                #     # i = i + 1
        else:
            break

    cap.release()
    cv2.destroyAllWindows()
    out.release()

    with open('data.pk', 'wb') as f:
        pickle.dump(data, f, 0)
    print('frame:', i)
