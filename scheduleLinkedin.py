import time
from datetime import datetime
from linkedIn_bot import post_linkedin, post_image_to_linkedin, post_video_to_linkedin
from mongoDB_manager import LinkedInBotMongoDB  # Fixed import

# Connect to database
db = LinkedInBotMongoDB()

def check_and_post():
    """Check for posts and post them"""
    print(f"\n🔍 Checking LinkedIn at {datetime.now().strftime('%H:%M:%S')}")
    
    # Get posts ready to post
    pending = db.get_pending_posts()
    
    if not pending:
        print("   Nothing to post")
        return
    
    print(f"   Found {len(pending)} posts to post!")
    
    # Post each one
    for post in pending:
        post_id = str(post["_id"])
        
        try:
            # Post to LinkedIn
            if post["post_type"] == "text":
                result = post_linkedin(post["content"])
            
            elif post["post_type"] == "image":
                result = post_image_to_linkedin(post["media_path"], post.get("content", ""))
            
            elif post["post_type"] == "video":
                result = post_video_to_linkedin(post["media_path"], post.get("content", ""))
            
            # Check if success
            if "id" in result or "post_id" in result:
                db.mark_as_posted(post_id)
                print(f"   ✅ Posted successfully!")
            else:
                db.mark_as_failed(post_id, str(result))
                print(f"   ❌ Failed to post")
        
        except Exception as e:
            db.mark_as_failed(post_id, str(e))
            print(f"   ⚠️ Error: {e}")

# Keep checking every minute
print("🚀 LinkedIn Scheduler started - checking every 60 seconds")
print("Press Ctrl+C to stop\n")

while True:
    check_and_post()
    time.sleep(60)  # Wait 60 seconds
    