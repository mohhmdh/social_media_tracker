import requests #We use it to send HTTP requests to Facebook’s API (like POST, GET)

page_id = "780419848498767" #Page ID of the Facebook Page you want to publish to
page_token = "EAAaqSra2GZCoBP27kviOdsBl6GZAXHQ8rdsIpzCdyZCPidixhWwN9FXkMyCyanBHsA9fHgRbMaN1P6vHIUuPyi9ya4wPFLDUXdwAx1eYx9OwjwLha7hZBd7ZCxxMbRlaiuHJAn6WgdZAFCnbtw1WS0mjZBbjCLV8hqKJLzZAhOiOqI79nfnvRdbQh5nomNw5mpk8V5fjCcaDgYSEJbSXV7SvIXlhjuLYMJg5oxR9DiJwgmIC"
    
def post_facebook(message: str): #post string
  #token of the page , to post 

    #Facebook API  for posting to a Page3
    url = f"https://graph.facebook.com/v24.0/{page_id}/feed"

    data = {
        
        "message": message,
        "access_token": page_token
    }
    response = requests.post(url, data=data) #post request
    return response.json() #JSON id (successful) or error ( wrong)


def post_image_to_facebook(image_path: str, message: str = ""):
    url = f"https://graph.facebook.com/v24.0/{page_id}/photos"
    files = {
        "source": open(image_path, "rb")
    }
    data = {
        "caption": message,
        "access_token": page_token
    }
    response = requests.post(url, files=files, data=data)
    return response.json()


def post_video_to_facebook(video_path: str, message: str = ""):
    url = f"https://graph.facebook.com/v24.0/{page_id}/videos"
    files = {
        "source": open(video_path, "rb")
    }
    data = {
        "description": message,  # Caption
        "access_token": page_token
    }
    response = requests.post(url, files=files, data=data)
    return response.json()
