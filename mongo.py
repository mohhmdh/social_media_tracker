from pymongo import MongoClient
from urllib.parse import quote_plus
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class FacebookBotMongoDB:
    def __init__(self):
        # Get MongoDB URI from environment
        mongodb_uri = os.getenv("MONGODB_URI")
        
        if not mongodb_uri:
            raise ValueError("MONGODB_URI not found in environment variables")
        
        # Connect to MongoDB Atlas
        self.client = MongoClient(mongodb_uri)
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


class LinkedInBotMongoDB:
    def __init__(self):
        # Get MongoDB URI from environment
        mongodb_uri = os.getenv("MONGODB_URI")
        
        if not mongodb_uri:
            raise ValueError("MONGODB_URI not found in environment variables")
        
        # Connect to MongoDB Atlas
        self.client = MongoClient(mongodb_uri)
        self.db = self.client["linkedin_bot"]  # Different database for LinkedIn
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
        