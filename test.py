import requests
import os
from dotenv import load_dotenv

load_dotenv()
PERSON_ID = "4ee4ERwXA_"
CONNECTION_TYPE = "CONNECTIONS"

# REST API endpoint for creating posts
posts_URL = "https://api.linkedin.com/rest/posts"

headers = {
    'Authorization': f"Bearer {os.getenv('LINKEDIN_ACCESS_TOKEN')}",
    'X-RestLi-Protocol-Version': '2.0.0',
    'LinkedIn-Version': '202411',
    'Content-Type': 'application/json'
}


# 1. TEXT POST (Minimum Required Fields)
text_post = {
    "author": f"urn:li:person:{PERSON_ID}",  # Required: Your LinkedIn person URN
    "lifecycleState": "PUBLISHED",  # Required: PUBLISHED or DRAFT
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": "Your post content here"  # Required: The actual text
            },
            "shareMediaCategory": "NONE"  # Required: NONE, ARTICLE, IMAGE, or VIDEO
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": f"{CONNECTION_TYPE}"  # Required: PUBLIC or CONNECTIONS
    }
}

# 2. ARTICLE/URL SHARE
article_post = {
    "author": f"urn:li:person:{PERSON_ID}",
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": "Check out this article!"
            },
            "shareMediaCategory": "ARTICLE",
            "media": [  # Required for ARTICLE
                {
                    "status": "READY",  # Required
                    "originalUrl": "https://example.com/article",  # Required: URL to share
                    "title": {  # Optional but recommended
                        "text": "Article Title"
                    },
                    "description": {  # Optional
                        "text": "Article description"
                    }
                }
            ]
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": f"{CONNECTION_TYPE}"
    }
}

# 3. IMAGE SHARE
image_post = {
    "author": f"urn:li:person:{PERSON_ID}",
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": "Check out this image!"
            },
            "shareMediaCategory": "IMAGE",
            "media": [  # Required for IMAGE
                {
                    "status": "READY",  # Required
                    "media": "urn:li:digitalmediaAsset:ASSET_ID",  # Required: From upload
                    "title": {  # Optional
                        "text": "Image Title"
                    },
                    "description": {  # Optional
                        "text": "Image description"
                    }
                }
            ]
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": f"{CONNECTION_TYPE}"
    }
}

# 4. VIDEO SHARE
video_post = {
    "author": f"urn:li:person:{PERSON_ID}",
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": "Watch this video!"
            },
            "shareMediaCategory": "VIDEO",
            "media": [  # Required for VIDEO
                {
                    "status": "READY",  # Required
                    "media": "urn:li:digitalmediaAsset:ASSET_ID",  # Required: From upload
                    "title": {  # Optional
                        "text": "Video Title"
                    },
                    "description": {  # Optional
                        "text": "Video description"
                    }
                }
            ]
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": f"{CONNECTION_TYPE}"
    }
}

# REGISTER IMAGE/VIDEO UPLOAD (Before creating IMAGE/VIDEO post)
register_upload_body = {
    "registerUploadRequest": {
        "recipes": [
            "urn:li:digitalmediaRecipe:feedshare-image"  # or feedshare-video
        ],
        "owner": f"urn:li:person:{PERSON_ID}",
        "serviceRelationships": [
            {
                "relationshipType": "OWNER",
                "identifier": "urn:li:userGeneratedContent"
            }
        ]
    }
}



# Use POST method and json parameter
response = requests.post(posts_URL, headers=headers, json=article_post)

print(f"Status: {response.status_code}")
print(f"Response Text: {response.text}")

if response.status_code == 201:
    print("Post created successfully!")
    # Get the post ID from the Location header
    post_id = response.headers.get('x-restli-id') or response.headers.get('Location')
    print(f"Post ID: {post_id}")
    print(f"Response headers: {dict(response.headers)}")
elif response.text:  # Only try to parse JSON if there's content
    try:
        print("Error response:", response.json())
    except:
        print("Could not parse error response")
else:
    print("Empty response body")
    
