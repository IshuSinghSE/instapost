import json
import os
from datetime import datetime

with open("swiggyindia.json", "r") as f:
    data = json.load(f)
    user_data = data["data"]["user"]
    username = user_data["username"]
    user_id = user_data["id"]
    media = user_data["edge_owner_to_timeline_media"]
    post_count = media["count"]
    posts = media["edges"]

    print(f"Total posts: {len(posts)}\n {username} has {post_count} posts")

    formatted_posts = []

    for post in posts:
        node = post["node"]
        pid = node["id"]
        shortcode = node["shortcode"]
        taken_at = datetime.fromtimestamp(node["taken_at_timestamp"]).strftime('%Y-%m-%dT%H:%M:%SZ')
        caption = node["edge_media_to_caption"]["edges"][0]["node"]["text"]
        comments = node["edge_media_to_comment"]["count"]
        likes = node["edge_liked_by"]["count"]
        # image_url = node["display_url"]
        # video_url = node.get("video_url", None)

        hashtags = [word for word in caption.split() if word.startswith("#")]

        formatted_post = {
            "id": pid,
            "shortcode": shortcode,
            "likes_count": likes,
            "comments_count": comments,
            "timestamp": taken_at,
            # "caption": caption,
            # "hashtags": hashtags,
            # "image_url": image_url,
            # "video_url": video_url
        }
        formatted_posts.append(formatted_post)

        # print(f"Post taken at: {taken_at}")
        # print(f"Caption: {caption}")
        # print(f"Image URL: {image_url}")
        # print(f"Comments: {comments}")
        # print(f"Likes: {likes}")
        # print(f"Shortcode: {shortcode}")

        # if video_url:
        #     print(f"Video URL: {video_url}")

    output_file = f"post_{username}.json"
    with open(output_file, "w") as out_f:
        json.dump(formatted_posts, out_f, indent=4)

    print(f"Data saved to {output_file}")

