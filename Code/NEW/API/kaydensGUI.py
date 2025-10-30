import tkinter as tk
import requests

def move_forward(speed: int, ttime: int):
    base_url = "http://10.25.128.40:8000"
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
    base_url = "http://10.25.128.40:8000"
    endpoint = f"{base_url}/move/right"

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
    base_url = "http://10.25.128.40:8000"
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

def move_backward(speed: int, ttime: int):
    base_url = "http://10.25.128.40:8000"
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

# Create the main application window
root = tk.Tk()
root.title("Placeholder GUI")
root.geometry("400x250")

# Create and place the input labels and entry boxes
tk.Label(root, text="Speed:").pack(pady=5)
entry_input1 = tk.Entry(root, width=40)
entry_input1.pack(pady=5)

tk.Label(root, text="Time:").pack(pady=5)
entry_input2 = tk.Entry(root, width=40)
entry_input2.pack(pady=5)

tk.Button(root, text="Forward", command=lambda: move_forward(entry_input1.get(), entry_input2.get())).pack(pady=5)
tk.Button(root, text="Backward", command=lambda: move_backward(entry_input1.get(), entry_input2.get())).pack(pady=5)
tk.Button(root, text="Left", command=lambda: move_left(entry_input1.get(), entry_input2.get())).pack(pady=5)
tk.Button(root, text="Right", command=lambda: move_right(entry_input1.get(), entry_input2.get())).pack(pady=5)

# Start the main event loop
root.mainloop()