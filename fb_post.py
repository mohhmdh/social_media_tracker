import requests #We use it to send HTTP requests to Facebook’s API (like POST, GET)

def post_facebook(message: str): #post string
    page_id = "813845588484228" #Page ID of the Facebook Page you want to publish to
    page_token = "EAAaqSra2GZCoBP5ZAlFVFplPHgke1lKynnrmBf2UXPlXbv0kjZAYPp4PLfb2HhYCRZAXwmOPymqoaqgd26xsMEih664vSryAI8XA8LSASDiFDWUsBZBUk9wBAJ90hTjr3hUR7DpjpLJPN7V2qWGeeRDUubhMSZAGDAhEBDqhTEyh6HsYhu0TMDztt9hr1xNmtnvZBRUKEWLqjCsfVSFxpsBGF18qReXejHvOeazuZAYZD"
    #token of the page , to post 

    #Facebook API  for posting to a Page3
    url = f"https://graph.facebook.com/v24.0/{page_id}/feed"

    data = {
        "message": message,
        "access_token": page_token
    }
    response = requests.post(url, data=data) #post request
    return response.json() #JSON id (successful) or error ( wrong)