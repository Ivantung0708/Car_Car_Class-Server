import argparse
import logging
import threading
import os
import sys
import time

import numpy as np
import pandas

from BTinterface import BTInterface
from maze import Action, Maze
from score import ScoreboardServer, ScoreboardFake

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

log = logging.getLogger(__name__)

# TODO : Fill in the following information
TEAM_NAME = "YOUR_TEAM_NAME"
SERVER_URL = "http://140.112.175.18:5000/"
MAZE_FILE = "data/maze.csv"
BT_PORT = "COM10"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="0: treasure-hunting, 1: self-testing", type=str)
    parser.add_argument("--maze-file", default=MAZE_FILE, help="Maze file", type=str)
    parser.add_argument("--bt-port", default=BT_PORT, help="Bluetooth port", type=str)
    parser.add_argument(
        "--team-name", default=TEAM_NAME, help="Your team name", type=str
    )
    parser.add_argument("--server-url", default=SERVER_URL, help="Server URL", type=str)
    return parser.parse_args()


def main(mode: int, bt_port: str, team_name: str, server_url: str, maze_file: str):
    maze = Maze(maze_file)
    interface = BTInterface(port=bt_port)

    if mode == "0":
        log.info("Mode 0: For treasure-hunting")
        # TODO : for treasure-hunting, which encourages you to hunt as many scores as possible

    elif mode == "1":
        log.info("Mode 1: Self-testing mode.")
        node1 = maze.get_node_dict()[3]
        visited = []
        visited = maze.BFS(node1)
        moves = maze.getActions(visited)
        command = ''
        for move in moves:
            if move == 1:
                command += 'f'
            if move == 2:
                command += 'b'
            if move == 3:
                command += 'r'
            if move == 4:
                command += 'l'
        command += 's'
        print(command)
        point = ScoreboardServer(team_name, server_url)
        time.sleep(5)
        interface.bt.serial_write_string(command)
        while True:
            uid = interface.get_UID()
            if uid != 0:
                uid = uid.upper()
                print(uid[2:])
                score, time_remaining = point.add_UID(uid[2:])
                current_score = point.get_current_score()
                log.info(f"Current score: {current_score}")


    else:
        log.error("Invalid mode")
        sys.exit(1)


if __name__ == "__main__":
    args = parse_args()
    main(**vars(args))
