#!/usr/bin/python3

import re, asyncio, subprocess as sp, os, random
import discord
from discord.ext import commands

intents=discord.Intents.default()
intents.message_content=True
bot=commands.Bot(command_prefix="[!]", intents=intents)

@bot.event
async def on_ready():
	print("[Large Dog voice] I'm wet")

twitter_check=re.compile(r"https?://(?:www\.)?(?:twitter|x)\.com(/\w+/status/\d+)")
# gdl_path = sp.check_output(["/usr/bin/which", "gallery-dl"]).decode().strip()
# assert gdl_path != ""
gdl_path = "/home/james/.local/bin/gallery-dl"

@bot.event
async def on_message(message):
	if message.author.id==bot.application_id:
		return
	replies=[]
	await asyncio.sleep(3)
	paths = [x[1] for x in twitter_check.finditer(message.content)]
	for embed in map(lambda x: x.to_dict(), message.embeds):
		print(embed)
		embed_match = twitter_check.match(embed["url"])
		if embed_match is None:
			continue
		embed_url = embed_match[0]
		embed_path = embed_match[1]
		if embed_path not in paths:
			continue
		if embed["title"] == "X":
			continue
		gdl_stdout = metadata=sp.run([gdl_path, embed_url, "--simulate", "--range", "0-1"], stdout=sp.PIPE, stderr=sp.DEVNULL).stdout
		if not any(map(lambda line: line.endswith(b".mp4"), gdl_stdout.splitlines())):
			try:
				paths.remove(embed_path)
			except:
				pass
	for path in paths:
		replies.append(f"https://vxtwitter.com{path}")
	if replies:
		if "||" in message.content or "`" in message.content:
			await message.reply("It looks like there might be an embed fail but it might be behind a spoiler tag. I can't tell. You're on your own!", mention_author=False)
		else:
			await message.reply(random.choice(["Discord fail!", "Twitter fail!", "Twitter (incorrectly known as X) fail!", "Embed fail!"])+"\n"+"\n".join(replies), mention_author=False)

bot.run(os.environ["bot_lwd"])
