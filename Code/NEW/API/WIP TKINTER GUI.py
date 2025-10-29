import tkinter as tk
import requests

api_url = "http://127.0.0.1:8000"



def button_click(direction_id):
    """
    Handles the button click event by sending a GET request to the API
    with the specified direction as a query parameter.
    """

    # Map direction IDs to command strings
    direction_map = {
        1: "forward",
        2: "backward",
        3: "right",
        4: "left"
    }

    # Get the command string from the map
    command = direction_map.get(direction_id)

    if not command:
        print(f"Invalid direction ID: {direction_id}")
        return

    # Set up the parameters for the GET request
    # This will result in a URL like: http://127.0.0.1:8000/?command=forward
    params = {'command': command}

    print(f"Sending command: {command}...")

    try:
        # Make the GET request
        response = requests.get(api_url, params=params, timeout=5)

        # Check if the request was successful
        if response.status_code == 200:
            print(f"Successfully sent command: {command}")
            # Print the response from the server
            print(f"Server Response: {response.text}")
        else:
            print(f"Failed to send command: {command}.")
            print(f"Status code: {response.status_code}")
            print(f"Response: {response.text}")

    except requests.exceptions.ConnectionError:
        # This error happens if the server isn't running or is unreachable
        print(f"Error: Could not connect to API at {api_url}.")
        print("Please ensure the server is running.")
    except requests.exceptions.Timeout:
        # This error happens if the server takes too long to respond
        print(f"Error: The request to {api_url} timed out.")
    except Exception as e:
        # Catch any other unexpected errors
        print(f"An unexpected error occurred: {e}")


# --- GUI Setup ---
root = tk.Tk()
root.title("API Controller")
root.geometry("300x200")

# Configure grid to expand and center buttons
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Define buttons with lambda functions calling button_click
button1 = tk.Button(root, text="Forward", command=lambda: button_click(1), width=12, height=4)
button2 = tk.Button(root, text="Backward", command=lambda: button_click(2), width=12, height=4)
button3 = tk.Button(root, text="Right", command=lambda: button_click(3), width=12, height=4)
button4 = tk.Button(root, text="Left", command=lambda: button_click(4), width=12, height=4)

# Place buttons in the grid
button1.grid(row=0, column=0, padx=10, pady=10)
button2.grid(row=0, column=1, padx=10, pady=10)
button3.grid(row=1, column=0, padx=10, pady=10)
button4.grid(row=1, column=1, padx=10, pady=10)

# Start the main GUI loop
root.mainloop()
