from pymongo import MongoClient
from datetime import datetime

class FacebookBotMongoDB:
    def __init__(self):
        # Connect to MongoDB
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["facebook_bot"]
        self.posts = self.db.scheduled_posts
    
    def add_post(self, post_type, scheduled_time, content=None, media_path=None):
        """Add a post to schedule"""
        post = {
            "post_type": post_type,
            "content": content,
            "media_path": media_path,
            "scheduled_time": scheduled_time,
            "status": "pending",
            "created_at": datetime.now()
        }
        
        result = self.posts.insert_one(post)
        return str(result.inserted_id)
    
    def get_pending_posts(self):
        """Get posts ready to post now"""
        posts = self.posts.find({
            "status": "pending",
            "scheduled_time": {"$lte": datetime.now()}
        })
        
        return list(posts)
    
    def mark_as_posted(self, post_id):
        """Mark a post as successfully posted"""
        from bson import ObjectId
        self.posts.update_one(
            {"_id": ObjectId(post_id)},
            {"$set": {"status": "posted", "posted_at": datetime.now()}}
        )
    
    def mark_as_failed(self, post_id, error):
        """Mark a post as failed"""
        from bson import ObjectId
        self.posts.update_one(
            {"_id": ObjectId(post_id)},
            {"$set": {"status": "failed", "error": error}}
        )