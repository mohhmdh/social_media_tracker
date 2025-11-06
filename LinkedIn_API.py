import requests
import os
from dotenv import load_dotenv

load_dotenv()
PERSON_ID = "4ee4ERwXA_"
CONNECTION_TYPE = "CONNECTIONS"  # or "PUBLIC"

# REST API endpoint for creating posts (NEW API)
posts_URL = "https://api.linkedin.com/rest/posts"

headers = {
    'Authorization': f"Bearer {os.getenv('LINKEDIN_ACCESS_TOKEN')}",
    'X-RestLi-Protocol-Version': '2.0.0',
    'LinkedIn-Version': '202411',
    'Content-Type': 'application/json'
}

# 1. TEXT POST (Correct structure for /rest/posts)
# 2. ARTICLE/URL POST
# 3. IMAGE POST
# 4. VIDEO POST
video_post = {
    "author": f"urn:li:person:{PERSON_ID}",
    "commentary": "Watch this video!",
    "visibility": CONNECTION_TYPE,
    "distribution": {
        "feedDistribution": "MAIN_FEED",
        "targetEntities": [],
        "thirdPartyDistributionChannels": []
    },
    "content": {
        "media": {
            "title": "Video Title",
            "id": "urn:li:video:ASSET_ID",  # Get from Videos API upload
            "altText": "Video description"  # Optional
        }
    },
    "lifecycleState": "PUBLISHED",
    "isReshareDisabledByAuthor": False
}
# 5. MULTI-IMAGE POST (Organic only)
# Note: For multi-image, use the MultiImage API structur
# 6. MENTIONS - Mention an organization or person
mention_post = {
    "author": f"urn:li:person:{PERSON_ID}",
    "commentary": "Hello @[Company Name](urn:li:organization:123456)",  # Mention format
    "visibility": CONNECTION_TYPE,
    "distribution": {
        "feedDistribution": "MAIN_FEED",
        "targetEntities": [],
        "thirdPartyDistributionChannels": []
    },
    "lifecycleState": "PUBLISHED",
    "isReshareDisabledByAuthor": False
}
# 7. HASHTAGS
hashtag_post = {
    "author": f"urn:li:person:{PERSON_ID}",
    "commentary": "Follow best practices #coding #python",  # Hashtag format
    "visibility": CONNECTION_TYPE,
    "distribution": {
        "feedDistribution": "MAIN_FEED",
        "targetEntities": [],
        "thirdPartyDistributionChannels": []
    },
    "lifecycleState": "PUBLISHED",
    "isReshareDisabledByAuthor": False
}
# 8. TARGETED POST (target specific audience)
targeted_post = {
    "author": f"urn:li:person:{PERSON_ID}",
    "commentary": "Targeted content",
    "visibility": CONNECTION_TYPE,
    "distribution": {
        "feedDistribution": "MAIN_FEED",
        "targetEntities": [{
            "geoLocations": ["urn:li:geo:103644278"],  # Geographic targeting
            "seniorities": ["urn:li:seniority:3"]      # Seniority targeting
        }],
        "thirdPartyDistributionChannels": []
    },
    "lifecycleState": "PUBLISHED",
    "isReshareDisabledByAuthor": False
}
#--------------text post -------------------------------------------------
def text_Post(content):
    text_post = {
        "author": f"urn:li:person:{PERSON_ID}",
        "commentary": content,  # Changed from shareCommentary.text
        "visibility": CONNECTION_TYPE,  # Changed from nested object
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": []
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False
    }
    response = requests.post(posts_URL, headers=headers, json=text_post)

    print(f"Status: {response.status_code}")

    if response.status_code == 201:
        print("✅ Post created successfully!")
        #Get the post ID from headers
        post_id = response.headers.get('x-restli-id')
        print(f"Post ID: {post_id}")
        print(f"Post URL: https://www.linkedin.com/feed/update/{post_id}/")  

    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Response: {response.text}")
        print(f"error : {response.json()}")

#-------------- article post ------------------------------------------------- 
def article_Post(content):
    article_post = {
        "author": f"urn:li:person:{PERSON_ID}",
        "commentary": content,
        "visibility": CONNECTION_TYPE,
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": []
        },
        "content": {
            "article": {
                "source": "https://example.com/article",  # Changed from originalUrl
                "title": "tester",
                "description": "pseudo lem",
                # Optional: "thumbnail": "urn:li:image:IMAGE_URN"  # If you want a thumbnail
            }
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False
    }
    response = requests.post(posts_URL, headers=headers, json=article_post)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        print("✅the second article to check the link created")
        #Get the post ID from headers
        post_id = response.headers.get('x-restli-id')
        print(f"Post ID: {post_id}")
        print(f"Post URL: https://www.linkedin.com/feed/update/{post_id}/")    
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Response: {response.text}")
        print(f"error : {response.json()}") 
     
#---------------------- image post -----------------------------------------------
#initialize image upload
image_upload_URL = "https://api.linkedin.com/rest/images?action=initializeUpload"
image_upload_header ={
  "initializeUploadRequest": {
    "owner": "urn:li:person:4ee4ERwXA_"
  }
}
def image_Post(image_path,comment_content,altext,imageTitle,CONNECTION_TYPE):
    image_upload_request = requests.post(image_upload_URL,headers=headers,json=image_upload_header)

    print(image_upload_request.json())

    response_json = image_upload_request.json()

    upload_url = response_json["value"]["uploadUrl"]  

    imageURN = response_json["value"]["image"] 

    with open(image_path, "rb") as f:
        resp = requests.put(upload_url, data=f, headers={"Content-Type": "image/jpeg"})
        print(resp.status_code)   

    image_post = {
        "author": f"urn:li:person:{PERSON_ID}",
        "commentary": comment_content,
        "visibility": CONNECTION_TYPE,
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": []
        },
        "content": {
            "media": {
                "title": imageTitle,
                "id": imageURN,  # Get from Images API upload
                "altText": altext  # Optional
            }
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False
    } 
    response = requests.post(posts_URL, headers=headers, json=image_post)  

    print(f"Status: {response.status_code}")  

    if response.status_code == 201:
        print("✅ Post created successfully!")
        #Get the post ID from headers
        post_id = response.headers.get('x-restli-id')
        print(f"Post ID: {post_id}")
        print(f"Post URL: https://www.linkedin.com/feed/update/{post_id}/")  

    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Response: {response.text}")
        print(f"error : {response.json()}")

#-------- multiimage post----------------------------------

def Multi_images_post(*images_array,CONNECTION_TYPE):
    upload_url = []
    imageURN = []
    i = 0
    for imageS in images_array:
        
        image_upload_request = requests.post(image_upload_URL,headers=headers,json=image_upload_header)
        print(image_upload_request.json())
        response_json = image_upload_request.json()
        upload_url.append(response_json["value"]["uploadUrl"])  
        imageURN.append(response_json["value"]["image"])
        i = i + 1
    
    multiimage_post = {
        "author": f"urn:li:person:{PERSON_ID}",
        "commentary": "Multiple images!",
        "visibility": CONNECTION_TYPE,
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": []
        },
        "content": {
            "multiImage": {
                "images": [{"id": urn} for urn in imageURN]
            }
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False
    }
    i = 0
    for imageS in images_array:
        with open(imageS, "rb") as f:
            resp = requests.put(upload_url[i], data=f, headers={"Content-Type": "image/jpeg"})
            print(resp.status_code) 
            i = i + 1 
    
    response = requests.post(posts_URL, headers=headers, json=multiimage_post)  
    print(f"Status: {response.status_code}")  
    if response.status_code == 201:
        print("✅ Post created successfully!")
        #Get the post ID from headers
        post_id = response.headers.get('x-restli-id')
        print(f"Post ID: {post_id}")
        print(f"Post URL: https://www.linkedin.com/feed/update/{post_id}/")      
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Response: {response.text}")
        print(f"error : {response.json()}")   
        
Multi_images_post("green.jpg","blue.jpg","R.jpg")        