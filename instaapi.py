import requests
import json

# Define the username
username = "swiggyindia"

# Define the API endpoint and headers
url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
headers = {
    "User-Agent": "Instagram 123.0.0.0 Android"
}

# Make the GET request
try:
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        
        # Save the response data to a JSON file
        filename = f"{username}.json"
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        
        print(f"Data saved to {filename}")
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        print("Response:", response.text)

except Exception as e:
    print(f"An error occurred: {e}")

# Note: This code is for educational purposes only. Always respect the terms of service of any website you interact with.   