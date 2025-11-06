imageURN = image_upload_request.json()["image"]

# with open("R.jpg", "rb") as f:
#     resp = requests.put(upload_url, data=f, headers={"Content-Type": "image/jpeg"})
# print(resp.status_code)   

# image_post = {
#     "author": f"urn:li:person:{PERSON_ID}",
#     "commentary": "Check out this image!",
#     "visibility": CONNECTION_TYPE,
#     "distribution": {
#         "feedDistribution": "MAIN_FEED",
#         "targetEntities": [],
#         "thirdPartyDistributionChannels": []
#     },
#     "content": {
#         "media": {
#             "title": "Image Title",
#             "id": imageURN,  # Get from Images API upload
#             "altText": "Image description"  # Optional
#         }
#     },
#     "lifecycleState": "PUBLISHED",
#     "isReshareDisabledByAuthor": False
# } 

# response = requests.post(posts_URL, headers=headers, json=image_post)
    
# print(f"Status: {response.status_code}")
    
# if response.status_code == 201:
#     print("✅ Post created successfully!")
#     #Get the post ID from headers
#     post_id = response.headers.get('x-restli-id')
#     print(f"Post ID: {post_id}")
#     print(f"Post URL: https://www.linkedin.com/feed/update/{post_id}/")
        
# else:
#     print(f"❌ Error: {response.status_code}")
#     print(f"Response: {response.text}")
#     print(f"error : {response.json()}")
