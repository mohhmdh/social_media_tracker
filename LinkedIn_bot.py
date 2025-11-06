import os
import discord
from discord import app_commands
from discord.ext import commands 
import logging
import validators
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('bot')

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

client = commands.Bot(command_prefix="!", intents=intents)
tree = client.tree  # Command tree for slash commands


@client.event
async def on_ready():
    logging.info(f'Logged in as {client.user}')


# Check function for slash commands
def has_social_or_admin():
    async def predicate(interaction: discord.Interaction) -> bool:
        # Check if user has "Social Media Manager" role
        role = discord.utils.get(interaction.user.roles, name="Social Media Manager")
        if role:
            return True
        # Check if user has administrator permission
        if interaction.user.guild_permissions.administrator:
            return True
        return False
    return app_commands.check(predicate)


# ========== MODALS ==========
# ==========texPostModal==================
class TextPostModal(discord.ui.Modal, title="Create Text Post"):
    content = discord.ui.TextInput(
        label="Post Text",
        style=discord.TextStyle.paragraph,
        placeholder="Write your post here...",
        required=True,
        max_length=2000
    ) 
    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="✅ Text Post Created",
            description=self.content.value,
            color=discord.Color.green()
        )
        embed.set_footer(text=f"Posted by {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed)

#=========== ArticlePostModal ====================
class ArticlePostModal(discord.ui.Modal, title="Create Article Post"):
    url = discord.ui.TextInput(
        label="Article URL",
        style=discord.TextStyle.short,
        placeholder="https://example.com/article",
        required=True,
        max_length=500
    )
    
    comment = discord.ui.TextInput(
        label="Your Commentary",
        style=discord.TextStyle.paragraph,
        placeholder="Share your thoughts about this article...",
        required=True,
        max_length=1000
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        # Validate URL
        if not validators.url(str(self.url.value)):
            await interaction.response.send_message("❌ Invalid URL provided!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="📰 Article Post Created",
            description=self.comment.value,
            color=discord.Color.blue()
        )
        embed.add_field(name="Article Link", value=self.url.value, inline=False)
        embed.set_footer(text=f"Posted by {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed)

#===========ImagePost===============================
class ImageCaptionModal(discord.ui.Modal, title="Add Image Caption"):
    caption = discord.ui.TextInput(
        label="Image Caption",
        style=discord.TextStyle.paragraph,
        placeholder="Write a caption for your image...",
        required=False,
        max_length=500
    )
    
    def __init__(self, image_url: str):
        super().__init__()
        self.image_url = image_url
    
    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📸 Image Post Created",
            description=self.caption.value if self.caption.value else "No caption provided",
            color=discord.Color.green()
        )
        embed.set_image(url=self.image_url)
        embed.set_footer(text=f"Posted by {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed)


# ==================== COMMANDS ===================================

@tree.command(name="post_text", description="Create a text post")
@has_social_or_admin()
async def post_text(interaction: discord.Interaction):
    await interaction.response.send_modal(TextPostModal())


@tree.command(name="post_article", description="Share an article with commentary")
@has_social_or_admin()
async def post_article(interaction: discord.Interaction):
    await interaction.response.send_modal(ArticlePostModal())


@tree.command(name="post_image", description="Upload an image with caption")
@has_social_or_admin()
@app_commands.describe(image="The image file to upload")
async def post_image(interaction: discord.Interaction, image: discord.Attachment):
    # Validate it's an image
    if not image.content_type or not image.content_type.startswith('image/'):
        await interaction.response.send_message("❌ Please provide a valid image file!", ephemeral=True)
        return
    
    # Show modal for caption
    await interaction.response.send_modal(ImageCaptionModal(image.url))


# ========== BUTTONS EXAMPLE ==========

class PostTypeView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)
    
    @discord.ui.button(label="Text Post", style=discord.ButtonStyle.primary, emoji="📝")
    async def text_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(TextPostModal())
    
    @discord.ui.button(label="Article Post", style=discord.ButtonStyle.primary, emoji="📰")
    async def article_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ArticlePostModal())


# Error handler for slash commands
@tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CheckFailure):
        await interaction.response.send_message(
            "❌ You don't have permission to use this command!", 
            ephemeral=True
        )
    else:
        await interaction.response.send_message(
            f"❌ An error occurred: {str(error)}", 
            ephemeral=True
        )


client.run(os.getenv("BOT_TOKEN"))