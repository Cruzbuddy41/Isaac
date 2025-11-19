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

move_forward(30, 2.75)

time.sleep(2.85)
move_left(10,1.5)
time.sleep(1.6)
move_forward(30,4.5)
time.sleep(4.7)

move_right(50, 0.7175)
time.sleep(0.7175)

move_forward(30,4.88)
time.sleep(4.88)

move_right(45,0.74)
time.sleep(0.7175)
move_forward(30,4)
time.sleep(4.3)

move_left(44,.85)
time.sleep(.85)
move_forward(30, 6)

