#!/usr/bin/python3

import re, asyncio, subprocess as sp, os, random, json, requests, hashlib
import discord
from discord.ext import commands

intents=discord.Intents.default()
intents.message_content=True
bot=commands.Bot(command_prefix="[!]", intents=intents)

with open("lwd_hashes.txt", "a") as _:
	pass

@bot.event
async def on_ready():
	print("[Large Dog voice] I'm wet")

twitter_check=re.compile(r"https?://(?:www\.)?(?:twitter|x)\.com/(\w+/status/\d+)")
gdl_path = "/home/james/.local/bin/gallery-dl"

@bot.event
async def on_message(message):
	if message.author.id==bot.application_id:
		return
	replies=[]
	await asyncio.sleep(3)
	paths = [x[1] for x in twitter_check.finditer(message.content)]
	for embed in message.embeds:
		embed_match = twitter_check.match(embed.url)
		if embed_match is None:
			continue
		embed_path = embed_match[1]
		paths.remove(embed_path)

		embed_path_hash = hashlib.sha256(embed_path.encode()).hexdigest()
		done=False
		with open("lwd_hashes.txt", "r") as f:
			for line in f:
				try:
					[hash, fix] = line.split(":")
					if hash == embed_path_hash and fix == "1":
						paths.append(embed_path)
						done=True
						break
				except:
					pass
		if done:
			continue

		print(f"New embed_path_hash: {embed_path_hash}")

		media_urls = json.loads(requests.get(f"https://api.vxtwitter.com/{embed_path}").content)["mediaURLs"]
		with open("lwd_hashes.txt", "a") as f:
			if len(media_urls) >= 2 or any(map(lambda x: x.endswith(".mp4"), media_urls)):
				paths.append(embed_path)
				f.write(f"\n{embed_path_hash}:1")
			else:
				f.write(f"\n{embed_path_hash}:0")
	for path in paths:
		replies.append(f"https://vxtwitter.com/{path}")
	if replies:
		catchphrase = random.choice(["Discord fail!", "Twitter fail!", "Twitter (incorrectly known as X) fail!", "Embed fail!"])
		if "||" in message.content or "`" in message.content:
			await message.reply(catchphrase+"\nSome of the tweets might be spoiler tagged, so I'm spoiler tagging all of them\n||"+"\n".join(replies)+"||", mention_author=False)
		else:
			await message.reply(catchphrase+"\n"+"\n".join(replies), mention_author=False)

bot.run(os.environ["bot_lwd"])
