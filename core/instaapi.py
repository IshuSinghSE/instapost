import requests
import json

# Define the username
username = "swiggyindia"

# Define the API endpoint and headers
base_url = "https://i.instagram.com/api/v1/users/web_profile_info/"
headers = {
    "User-Agent": "Instagram 123.0.0.0 Android"
}

# Initialize variables for pagination
all_posts = []
end_cursor = None
has_next_page = True

# Fetch all posts using pagination
while has_next_page:
    params = {"username": username}
    if end_cursor:
        params["after"] = end_cursor

    try:
        response = requests.get(base_url, headers=headers, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            user_data = data["data"]["user"]
            media = user_data["edge_owner_to_timeline_media"]

            # Append posts to the list
            all_posts.extend(media["edges"])

            # Update pagination info
            has_next_page = media["page_info"]["has_next_page"]
            end_cursor = media["page_info"]["end_cursor"]
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            print("Response:", response.text)
            break

    except Exception as e:
        print(f"An error occurred: {e}")
        break

# Save all posts to a JSON file
output_file = f"{username}_all_posts.json"
with open(output_file, "w") as file:
    json.dump(all_posts, file, indent=4)

print(f"All posts saved to {output_file}")