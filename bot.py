import asyncio
import discord
from discord.ext import commands
import random
import json
import io

from fb_post import (
    post_facebook,
    post_image_to_facebook,
    post_video_to_facebook,
    get_page_posts,
    get_page_insights,
    get_post_insights,
    get_post_details,
    get_post_comments,
    reply_to_comment,
    delete_post,
   
)

intents = discord.Intents.all()

import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("discord_token")

client = commands.Bot(command_prefix='.', intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has logged in')


@client.command()
async def ping(ctx):
    await ctx.send(f'pong! {round(client.latency * 1000)}ms')

@client.command()
async def hello(ctx):
    await ctx.send(f'hello {ctx.author.name}!')

@client.command()
async def quote(ctx):
    responses = open('quotes.txt').read().splitlines()
    response = random.choice(responses)
    await ctx.send(response)

@client.command()
async def thnx(ctx):
    await ctx.send(f'no problem {ctx.author.name}!')

@client.command()
async def clear(ctx, amount: int = 5):
    deleted = await ctx.channel.purge(limit=amount)
    await ctx.send(f'deleted {len(deleted)} messages!', delete_after=5)

@client.command()
async def gn(ctx):
    await ctx.send('you too')

def has_social_or_admin():
    async def predicate(ctx):
        role = discord.utils.get(ctx.author.roles, name="Social Media Manager")
        if role:
            return True
        if ctx.author.guild_permissions.administrator:
            return True
        return False
    return commands.check(predicate)

# ---------- post to facebook ----------
@client.command()
@has_social_or_admin()
async def postfb(ctx, *, message: str = None):
    if not message:
        return await ctx.send("❌ format: `.postfb <your message>`")
    
    await ctx.send("📤 posting to facebook...")
    try:
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, post_facebook, message)
        
        if isinstance(result, dict) and "id" in result:
            embed = discord.Embed(
                title="✅ successfully posted to facebook!",
                color=discord.Color.green()
            )
            embed.add_field(name="post id", value=f"`{result['id']}`", inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌ error: {result}")
    except Exception as e:
        await ctx.send(f"❌ unexpected error: {e}")

@client.command()
@has_social_or_admin()
async def postimg(ctx, *, caption: str = ""):
    if len(ctx.message.attachments) == 0:
        return await ctx.send("❌ attach an image with the command!")
    
    await ctx.send("📤 uploading image to facebook...")
    attachment = ctx.message.attachments[0]
    path = f"./{attachment.filename}"
    await attachment.save(path)
    
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, post_image_to_facebook, path, caption)
    
    if isinstance(result, dict) and ("post_id" in result or "id" in result):
        post_id = result.get("post_id") or result.get("id")
        embed = discord.Embed(
            title="✅ image posted successfully!",
            color=discord.Color.green()
        )
        embed.add_field(name="post id", value=f"`{post_id}`", inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"❌ error posting image: {result}")

@client.command()
@has_social_or_admin()
async def postvideo(ctx, *, caption: str = ""):
    if len(ctx.message.attachments) == 0:
        return await ctx.send("❌ attach a video with the command!")
    
    await ctx.send("📤 uploading video to facebook...")
    attachment = ctx.message.attachments[0]
    path = f"./{attachment.filename}"
    await attachment.save(path)
    
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, post_video_to_facebook, path, caption)
    
    if isinstance(result, dict) and "id" in result:
        embed = discord.Embed(
            title="✅ video posted successfully!",
            color=discord.Color.green()
        )
        embed.add_field(name="post id", value=f"`{result['id']}`", inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"❌ error posting video: {result}")

# ---------- get page posts ----------
@client.command()
async def getposts(ctx, limit: int = 5):
    await ctx.send("📋 fetching last posts...")
    try:
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, get_page_posts, limit)
        
        if "data" in result:
            posts = result["data"]
            if not posts:
                await ctx.send("⚠️ no posts found")
            else:
                embed = discord.Embed(
                    title=f"📄 last {len(posts)} posts",
                    color=discord.Color.blue()
                )
                for i, post in enumerate(posts, 1):
                    post_id = post["id"]
                    message = post.get("message", "no message")[:100]
                    created = post.get("created_time", "unknown")
                    url = post.get("permalink_url", "")
                    
                    field_value = f"**message:** {message}\n**created:** {created}"
                    if url:
                        field_value += f"\n**[view post]({url})**"
                    
                    embed.add_field(
                        name=f"#{i} - `{post_id}`",
                        value=field_value,
                        inline=False
                    )
                await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌ error fetching posts: {result}")
    except Exception as e:
        await ctx.send(f"❌ unexpected error: {e}")

# ---------- get page insights ----------
@client.command()
async def pageinfo(ctx):
    await ctx.send("📊 fetching page insights...")
    try:
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, get_page_insights)
        
        if isinstance(result, dict) and result.get("success"):
            embed = discord.Embed(
                title="📊 page insights",
                color=discord.Color.blue()
            )
            
            metrics = result.get("metrics", {})
            for name, data in metrics.items():
                value = data.get("value", 0)
                period = data.get("period", "day")
                embed.add_field(
                    name=name.replace("_", " "),
                    value=f"**{value}** ({period})",
                    inline=True
                )
            
            if not metrics:
                embed.description = "⚠️ no metrics available"
            
            await ctx.send(embed=embed)
        else:
            result_str = json.dumps(result, indent=2)
            if len(result_str) < 1900:
                await ctx.send(f"```json\n{result_str}\n```")
            else:
                file = discord.File(io.BytesIO(result_str.encode()), filename="page_insights.json")
                await ctx.send("📊 page insights (file attached):", file=file)
            
    except Exception as e:
        await ctx.send(f"❌ unexpected error: {e}")

# ---------- get post insights ----------
@client.command()
async def postinfo(ctx, post_id: str):
    await ctx.send("📊 fetching post insights...")
    try:
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, get_post_insights, post_id)
        
        if isinstance(result, dict) and result.get("success"):
            embed = discord.Embed(
                title="📊 post insights",
                description=f"**post id:** `{post_id}`",
                color=discord.Color.blue()
            )
            
            metrics = result.get("metrics", {})
            
            # engagement metrics
            impressions = metrics.get("post_impressions", 0)
            engaged_users = metrics.get("post_engaged_users", 0)
            clicks = metrics.get("post_clicks", 0)
            
            embed.add_field(name="👁️ impressions", value=f"**{impressions}**", inline=True)
            embed.add_field(name="👥 engaged users", value=f"**{engaged_users}**", inline=True)
            embed.add_field(name="🖱️ clicks", value=f"**{clicks}**", inline=True)
            
            # reactions breakdown
            reactions = metrics.get("reactions", {})
            total_reactions = metrics.get("total_reactions", 0)
            
            if reactions:
                reactions_str = "\n".join([f"{k}: {v}" for k, v in reactions.items()])
                embed.add_field(
                    name=f"💙 reactions (total: {total_reactions})",
                    value=reactions_str or "none",
                    inline=False
                )
            
            await ctx.send(embed=embed)
        else:
            result_str = json.dumps(result, indent=2)
            if len(result_str) < 1900:
                await ctx.send(f"```json\n{result_str}\n```")
            else:
                file = discord.File(io.BytesIO(result_str.encode()), filename="post_insights.json")
                await ctx.send("📊 post insights (file attached):", file=file)
    except Exception as e:
        await ctx.send(f"❌ unexpected error: {e}")

# ---------- get post details ----------
@client.command()
async def postdetails(ctx, post_id: str):
    await ctx.send("📄 fetching post details...")
    try:
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, get_post_details, post_id)
        
        if isinstance(result, dict) and result.get("success"):
            embed = discord.Embed(
                title="📄 post details",
                description=result.get("message", "no message")[:500],
                color=discord.Color.gold()
            )
            
            embed.add_field(name="post id", value=f"`{result['post_id']}`", inline=False)
            embed.add_field(name="created", value=result.get("created_time", "unknown"), inline=False)
            
            engagement = result.get("engagement", {})
            embed.add_field(name="👍 likes", value=str(engagement.get("likes", 0)), inline=True)
            embed.add_field(name="💬 comments", value=str(engagement.get("comments", 0)), inline=True)
            embed.add_field(name="🔄 shares", value=str(engagement.get("shares", 0)), inline=True)
            
            url = result.get("url", "")
            if url:
                embed.add_field(name="link", value=f"[view on facebook]({url})", inline=False)
            
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌ error: {result}")
    except Exception as e:
        await ctx.send(f"❌ unexpected error: {e}")

# ---------- get post comments ----------
@client.command()
async def comments(ctx, post_id: str):
    await ctx.send("💬 fetching comments...")
    try:
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, get_post_comments, post_id)
        
        if "data" in result:
            comments = result["data"]
            if not comments:
                await ctx.send("⚠️ no comments found")
            else:
                embed = discord.Embed(
                    title=f"💬 comments ({len(comments)} total)",
                    color=discord.Color.purple()
                )
                for i, comment in enumerate(comments[:10], 1):
                    comment_id = comment["id"]
                    message = comment.get("message", "no message")[:150]
                    from_user = comment.get("from", {}).get("name", "unknown")
                    likes = comment.get("like_count", 0)
                    
                    embed.add_field(
                        name=f"#{i} - {from_user}",
                        value=f"**id:** `{comment_id}`\n💙 {likes} likes\n{message}",
                        inline=False
                    )
                
                if len(comments) > 10:
                    embed.set_footer(text=f"showing 10 of {len(comments)} comments")
                
                await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌ error fetching comments: {result}")
    except Exception as e:
        await ctx.send(f"❌ unexpected error: {e}")

# ---------- reply to comment ----------
@client.command()
@has_social_or_admin()
async def reply(ctx, comment_id: str, *, message: str):
    await ctx.send("💬 replying to comment...")
    try:
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, reply_to_comment, comment_id, message)
        
        if isinstance(result, dict) and "id" in result:
            embed = discord.Embed(
                title="✅ reply posted successfully!",
                color=discord.Color.green()
            )
            embed.add_field(name="comment id", value=f"`{comment_id}`", inline=False)
            embed.add_field(name="reply id", value=f"`{result['id']}`", inline=False)
            embed.add_field(name="message", value=message[:200], inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌ error: {result}")
    except Exception as e:
        await ctx.send(f"❌ unexpected error: {e}")

# ---------- delete post ----------
@client.command()
@has_social_or_admin()
async def deletepost(ctx, post_id: str):
    await ctx.send("🗑️ deleting post...")
    try:
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, delete_post, post_id)
        
        if isinstance(result, dict) and result.get("success"):
            embed = discord.Embed(
                title="✅ post deleted successfully!",
                color=discord.Color.green()
            )
            embed.add_field(name="post id", value=f"`{post_id}`", inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌ error: {result}")
    except Exception as e:
        await ctx.send(f"❌ unexpected error: {e}")





client.run(TOKEN)