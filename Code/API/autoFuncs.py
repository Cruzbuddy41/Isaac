import tkinter as tk
import requests
import time

base_url = "http://10.25.128.40:8000"

def move_forward(speed: int, ttime: float):
    endpoint = f"{base_url}/move/forward"

    params = {
        "speed": speed,
        "ttime": ttime
    }

    try:
        response = requests.post(endpoint, params=params)
        response.raise_for_status()
        print(f"Request successful: {response.json()}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")

def move_right(speed: int, ttime: float):
    endpoint = f"{base_url}/move/right"

    params = {
        "speed": speed,
        "ttime": ttime
    }
#ddd
    try:
        response = requests.post(endpoint, params=params)
        response.raise_for_status()
        print(f"Request successful: {response.json()}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")

def move_left(speed: int, ttime: float):
    endpoint = f"{base_url}/move/left"

    params = {
        "speed": speed,
        "ttime": ttime
    }

    try:
        response = requests.post(endpoint, params=params)
        response.raise_for_status()
        print(f"Request successful: {response.json()}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")

def move_backward(speed: int, ttime: float):
    endpoint = f"{base_url}/move/backward"

    params = {
        "speed": speed,
        "ttime": ttime
    }

    try:
        response = requests.post(endpoint, params=params)
        response.raise_for_status()
        print(f"Request successful: {response.json()}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")

def stop():
    endpoint = f"{base_url}/stop"
    try:
        response = requests.post(endpoint)
        response.raise_for_status()
        print("Stop Worked")
    except requests.exceptions.RequestException as e:
        print("Error occured while stopping")

move_forward(50, 2.8)
#1 sec = 1 foot
time.sleep(2.9)
move_left(25,1.5)
time.sleep(2.1)
move_forward(50,1)
time.sleep(1.4)
move_right(25, 4)
time.sleep(1.1)
move_forward(50,.7)
time.sleep(.9)
move_forward(50,1.9)
time.sleep(2)
move_right(25,.8)
time.sleep(.9)
move_forward(50,2.2)
time.sleep(2.3)
move_left(25,.9)
time.sleep(1)
move_forward(50, 2.8)

