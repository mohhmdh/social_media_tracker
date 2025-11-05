from datetime import datetime
from mongoDB_manager import FacebookBotMongoDB

# Connect to database
db = FacebookBotMongoDB()

print("📝 Scheduling posts...\n")

# Schedule a text post
post_id = db.add_post(
    post_type="text",
    scheduled_time=datetime(2025, 11, 6, 15, 30),  # Year, Month, Day, Hour, Minute
    content="Hello from my bot!"
)
print(f"✅ Text post scheduled - ID: {post_id}")

# Schedule an image post
post_id = db.add_post(
    post_type="image",
    scheduled_time=datetime(2025, 11, 6, 18, 0),
    content="Check this image!",
    media_path="./my_image.jpg"  # Your image file
)
print(f"✅ Image post scheduled - ID: {post_id}")

# Schedule a video post
post_id = db.add_post(
    post_type="video",
    scheduled_time=datetime(2025, 11, 7, 10, 0),
    content="New video!",
    media_path="./my_video.mp4"  # Your video file
)
print(f"✅ Video post scheduled - ID: {post_id}")

print("\n✅ All posts scheduled! Now run bot_scheduler.py to start posting")