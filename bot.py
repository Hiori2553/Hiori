import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")



# Thiết lập intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Cấu hình hệ thống cấp độ
EXP_GAIN = 5             # Kinh nghiệm mỗi lần chat
LEVEL_UP_EVERY = 15       # Bao nhiêu XP thì lên cấp

user_xp = {}       # user_id: XP
user_level = {}    # user_id: cấp

@bot.event
async def on_ready():
    print(f'✅ Bot đã online với tên: {bot.user}')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    user_id = message.author.id

    # Cộng XP
    user_xp[user_id] = user_xp.get(user_id, 0) + EXP_GAIN
    xp = user_xp[user_id]

    # Tính cấp
    new_level = xp // LEVEL_UP_EVERY
    old_level = user_level.get(user_id, 0)

    if new_level > old_level:
        user_level[user_id] = new_level
        await message.channel.send(f"🎉 {message.author.mention} đã lên cấp {new_level}!")

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send("Xin chào! Mình là bot của bạn nè 🤖")

@bot.command()
async def level(ctx, member: discord.Member = None):
    member = member or ctx.author
    user_id = member.id
    xp = user_xp.get(user_id, 0)
    lvl = user_level.get(user_id, 0)
    await ctx.send(f"📊 {member.display_name} đang ở cấp độ {lvl} với {xp} kinh nghiệm.")

bot.run(TOKEN)

