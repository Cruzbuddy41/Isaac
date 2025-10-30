import tkinter as tk
import requests

# Define API URL
api_url = "http://10.25.128.40:8000"

def button_click(direction_id):
    """
    Handles the button click event by sending a GET request to the API with the
    specified direction as a query parameter.
    """
    direction_map = {
        1: "forward",
        2: "backward",
        3: "right",
        4: "left"
    }
    command = direction_map.get(direction_id)
    if not command:
        print(f"Invalid direction ID: {direction_id}")
        return

    # Get values from entry fields
    speed = speedentry.get()
    ttime = ttimeentry.get()

    # Set up the parameters for the GET request
    params = {"command": command, "speed": speed, "ttime": ttime}

    print(f"Sending command: {command} with params: {params}...")

    try:
        response = requests.get(api_url, params=params, timeout=5)
        if response.status_code == 200:
            print(f"Successfully sent command: {command}")
            print(f"Server Response: {response.text}")
        else:
            print(f"Failed to send command: {command}.")
            print(f"Status code: {response.status_code}")
            print(f"Response: {response.text}")
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to API at {api_url}.")
        print("Please ensure the server is running.")
    except requests.exceptions.Timeout:
        print(f"Error: The request to {api_url} timed out.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- GUI Setup ---
root = tk.Tk()
root.title("API Controller")
root.geometry("300x200")

# --- Widgets ---
# Entry for speed, placed in row 0, column 1
speedentrylabel = tk.Label(root, text="Speed:")
speedentrylabel.grid(row=0, column=0, padx=5, pady=5, sticky="e")

speedentry = tk.Entry(root, width=10)
speedentry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
speedentry.insert(0, "100") # Default value

# Entry for travel time, placed in row 1, column 1
ttimeentrylabel = tk.Label(root, text="Time:")
ttimeentrylabel.grid(row=1, column=0, padx=5, pady=5, sticky="e")

ttimeentry = tk.Entry(root, width=10)
ttimeentry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
ttimeentry.insert(0, "1") # Default value

# Define and place buttons, starting from row 2
# Note: Buttons must be placed in a separate grid area from the entry widgets
button1 = tk.Button(root, text="Forward", command=lambda: button_click(1), width=12, height=2)
button1.grid(row=2, column=0, columnspan=1, padx=10, pady=10)

button2 = tk.Button(root, text="Backward", command=lambda: button_click(2), width=12, height=2)
button2.grid(row=3, column=0, columnspan=1, padx=10, pady=10)

button3 = tk.Button(root, text="Right", command=lambda: button_click(3), width=12, height=2)
button3.grid(row=4, column=1, columnspan=1, padx=10, pady=10)

button4 = tk.Button(root, text="Left", command=lambda: button_click(4), width=12, height=2)
button4.grid(row=4, column=0, columnspan=1, padx=10, pady=10)

# Configure rows to expand and center widgets
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Start the main GUI loop
root.mainloop()
