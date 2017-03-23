#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import curses
import cv2
import threading
from queue import Queue
import random
import numpy
import sys
import getopt


char_pixel_map = {
    2:  '`',
    4:  '\'.',
    6:  '-',
    7:  '^,',
    8:  '\\/:"',
    9:  '~_!<>',
    11: ';',
    12: '=',
    13: '()+|?',
    14: 'i',
    15: 'j',
    16: 'l17{}',
    17: 'tv[]',
    18: 'crI',
    19: 'fuJ2',
    20: 'oxLO3%',
    21: 'ansyzC*',
    22: 'V',
    23: 'Y4569',
    24: 'ehNTZ0&',
    25: 'bdkwAFP',
    26: 'DX8$',
    27: 'pqGU',
    28: 'gKQS',
    29: 'BE',
    30: 'mRW#',
    31: 'H',
    36: 'M@'
}

show_height = 44
show_width = 160
board = [[]]
file_name = ''
speed = 10


def update_view(gray, y, x, block_height, block_width):
    avg_gray = numpy.mean([row[x:x + block_width] for row in gray[y:y + block_height]])
    keys = list(char_pixel_map.keys())
    candidates = char_pixel_map[keys[int(numpy.power(avg_gray / 256, 1.4) * len(keys))]]
    ch = candidates[int(random.uniform(0, len(candidates)))]
    # print('{0}, {1}'.format(int(i / block_height) + 1, int(j / block_width) + 1))
    return ch


def update_view_callback(r):
    result = r.result()
    if result[0] < show_height - 2 and result[1] < show_width - 2:
        board[result[0]][result[1]] = result[2]


def print_image(stdscr, filename, shared_queue):
    cap = cv2.VideoCapture(filename)

    frame_cnt = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if ret and frame_cnt % speed == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # cv2.imshow('frame', gray)
            frame_height = len(gray)
            frame_width = len(gray[0])
            stdscr.addstr(0, 1, "[{2}] height: {0}, width: {1}".format(frame_height, frame_width, frame_cnt))
            frame_cnt += 1

            # Convert image data to characters
            block_height = int(frame_height / show_height)
            block_width = int(frame_width / show_width)

            for i in range(0, frame_height, block_height):
                for j in range(0, frame_width, block_width):
                    ch = update_view(gray, i, j, block_height, block_width)
                    y, x = int(i / block_height), int(j / block_width)
                    if y < show_height - 2 and x < show_width - 2:
                        stdscr.addch(y + 1, x + 1, ch)

            stdscr.refresh()
        else:
            frame_cnt += 1

        # Check data sent from parent thread
        if shared_queue.qsize() > 0 and shared_queue.get() == -1:
            break

    cap.release()


def paint_ui(stdscr):
    stdscr.resize(show_height, show_width)
    stdscr.border()


def init_scr(stdscr):
    stdscr.clear()
    global show_height, show_width, board
    show_width = stdscr.getmaxyx()[1]
    show_height = int(show_width / 32 * 9)
    if show_height > stdscr.getmaxyx()[0]:
        show_height = stdscr.getmaxyx()[0]
        show_width = int(show_height / 9 * 32)
    board = [[0 for col in range(show_width - 2)] for row in range(show_height - 2)]

    paint_ui(stdscr)
    stdscr.refresh()

    shared_queue = Queue()

    thread = threading.Thread(target=print_image, args=(stdscr, file_name, shared_queue), daemon=True)
    thread.start()

    while True:
        ch = stdscr.getch()
        if ch == ord('q'):
            # Ask child to terminate
            shared_queue.put(-1)
            thread.join(2)
            break


if __name__ == '__main__':
    argv = sys.argv[1:]
    if len(argv) < 1:
        print('ascii_video.py -i <inputfile> [-s <speed>]')
        sys.exit(1)
    try:
        opts, args = getopt.getopt(argv, "hi:s:")
    except getopt.GetoptError:
        print('ascii_video.py -i <inputfile> [-s <speed>]')
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-h':
            print('ascii_video.py -i <inputfile> [-s <speed>]\n-i: 指定输入视频文件\n-s: 播放速度, 与硬件性能有关, 默认为10, 数值越大越快\n运行中按q退出')
            sys.exit()
        elif opt == '-i':
            file_name = arg
        elif opt == '-s':
            speed = int(arg)

    curses.wrapper(init_scr)

