import requests
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

page_id=780419848498767
page_token="EAAaqSra2GZCoBP92koiZB8zyDuqmzWaIUPkRhskpDO3tYKmM5M2jkR6bBMlLixErJAcMjpRsdSbsE53AKDa3nHegpZCefsiGlcai32h1WcEcxIsWxg2NQTbRybG2qESHY5HSL7kj4tKatgvAhvjoaVpsdb02qiXZCOdFolqKtC78bzKqlnTfUBqTTA9LtTNIlincGoblQCNkklH90FWZC2ZA2YgiZCU8lOKFxRa3V8ZD"




def post_facebook(message: str):
    url = f"https://graph.facebook.com/v24.0/{page_id}/feed"
    data = {"message": message, "access_token": page_token}
    response = requests.post(url, data=data)
    return response.json()

def post_image_to_facebook(image_path: str, message: str = ""):
    url = f"https://graph.facebook.com/v24.0/{page_id}/photos"
    files = {"source": open(image_path, "rb")}
    data = {"caption": message, "access_token": page_token}
    response = requests.post(url, files=files, data=data)
    return response.json()

def post_video_to_facebook(video_path: str, message: str = ""):
    url = f"https://graph.facebook.com/v24.0/{page_id}/videos"
    files = {"source": open(video_path, "rb")}
    data = {"description": message, "access_token": page_token}
    response = requests.post(url, files=files, data=data)
    return response.json()

def get_page_posts(limit: int = 5):
    url = f"https://graph.facebook.com/v24.0/{page_id}/posts"
    params = {"access_token": page_token, "limit": limit, "fields": "id,message,created_time,permalink_url"}
    response = requests.get(url, params=params)
    return response.json()

def get_page_insights():
    url = f"https://graph.facebook.com/v24.0/{page_id}/insights"
    params = {"metric": "page_impressions,page_engaged_users,page_post_engagements,page_fans", "period": "day", "access_token": page_token}
    response = requests.get(url, params=params)
    data = response.json()
    if "data" in data and data["data"]:
        formatted = {"success": True, "metrics": {}}
        for metric in data["data"]:
            name = metric["name"]
            values = metric.get("values", [])
            if values:
                formatted["metrics"][name] = {"value": values[-1].get("value", 0), "period": metric.get("period", "unknown"), "description": metric.get("description", "")}
        return formatted
    return data

def get_post_insights(post_id: str):
    url = f"https://graph.facebook.com/v24.0/{post_id}/insights"
    params = {"metric": "post_impressions,post_engaged_users,post_reactions_by_type_total,post_clicks", "access_token": page_token}
    response = requests.get(url, params=params)
    data = response.json()
    if "data" in data and data["data"]:
        formatted = {"success": True, "post_id": post_id, "metrics": {}}
        for metric in data["data"]:
            name = metric["name"]
            values = metric.get("values", [])
            if name == "post_reactions_by_type_total" and values:
                reactions = values[0].get("value", {})
                formatted["metrics"]["reactions"] = reactions
                formatted["metrics"]["total_reactions"] = sum(reactions.values())
            elif values:
                formatted["metrics"][name] = values[0].get("value", 0)
        return formatted
    return data

def get_post_details(post_id: str):
    url = f"https://graph.facebook.com/v24.0/{post_id}"
    params = {"fields": "id,message,created_time,shares,likes.summary(true),comments.summary(true),permalink_url", "access_token": page_token}
    response = requests.get(url, params=params)
    data = response.json()
    if "id" in data:
        formatted = {"success": True, "post_id": data["id"], "message": data.get("message", "no message"), "created_time": data.get("created_time", "unknown"), "url": data.get("permalink_url", ""), "engagement": {"likes": data.get("likes", {}).get("summary", {}).get("total_count", 0), "comments": data.get("comments", {}).get("summary", {}).get("total_count", 0), "shares": data.get("shares", {}).get("count", 0)}}
        return formatted
    return data

def get_post_comments(post_id: str):
    url = f"https://graph.facebook.com/v24.0/{post_id}/comments"
    params = {"access_token": page_token, "fields": "id,from,message,created_time,like_count"}
    response = requests.get(url, params=params)
    return response.json()

def reply_to_comment(comment_id: str, reply: str):
    url = f"https://graph.facebook.com/v24.0/{comment_id}/comments"
    data = {"message": reply, "access_token": page_token}
    response = requests.post(url, data=data)
    return response.json()

def delete_post(post_id: str):
    url = f"https://graph.facebook.com/v24.0/{post_id}"
    params = {"access_token": page_token}
    response = requests.delete(url, params=params)
    result = response.json()
    if result.get("success"):
        return {"success": True}
    return result
