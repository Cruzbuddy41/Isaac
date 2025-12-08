import tkinter as tk
import requests
base_url = "http://10.25.128.40:8000"
entry_input1 = 50
entry_input2 = 1000

def move_forward(speed: int, ttime: int):
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

def move_right(speed: int, ttime: int):
    endpoint = f"{base_url}/move/right"

    #speed = speed / 2
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

def move_left(speed: int, ttime: int):
    endpoint = f"{base_url}/move/left"

    #speed = speed / 2

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

def move_backward(speed: int, ttime: int):
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

def boom(entry_input1):
    temp = entry_input1
    if(temp < 90):
        temp = temp + 10
        entry_input1 = temp
        print("did something")
    else:
        print("Can't go faster sadly")

root = tk.Tk()
root.title("Placeholder GUI")
root.geometry("500x400")

tk.Label(root, text=f"Speed: {entry_input1}").pack(pady=5)
#entry_input1 = tk.Entry(root, width=40)
#entry_input1.pack(pady=5)

tk.Label(root, text=f"Time: {entry_input2}").pack(pady=5)
#entry_input2 = tk.Entry(root, width=40)
#entry_input2.pack(pady=5)

tk.Button(root, text="Forward \"W\"", command=lambda: move_forward(entry_input1, entry_input2)).pack(pady=5)
tk.Button(root, text="Backward \"S\"", command=lambda: move_backward(entry_input1, entry_input2)).pack(pady=5)
tk.Button(root, text="Left \"A\"", command=lambda: move_left(entry_input1, entry_input2)).pack(pady=5)
tk.Button(root, text="Right \"D\"", command=lambda: move_right(entry_input1, entry_input2)).pack(pady=5)
tk.Button(root, text="FASTER!!!!!!!!!!!! \"F\"", command=lambda: boom(entry_input1)).pack(pady=5)

tk.Button(root, text="STOP \"SPACE\"", command=stop, height=40, width=40, bg="red").pack(pady=20)

root.bind("<w>", lambda e: move_backward(entry_input1, entry_input2))
root.bind("<s>", lambda e: move_forward(entry_input1, entry_input2))
root.bind("<a>", lambda e: move_left(entry_input1, entry_input2))
root.bind("<d>", lambda e: move_right(entry_input1, entry_input2))
root.bind("<f>", lambda e: boom(entry_input1))
root.bind("<space>", lambda e: stop())

root.mainloop()
