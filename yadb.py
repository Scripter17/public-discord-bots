import sys, random, os, hashlib, dice, discord
from discord.ext import commands

intents=discord.Intents.default()
intents.message_content=True
bot=commands.Bot(command_prefix="?", intents=intents)
bot.remove_command("help")

@bot.event
async def on_ready():
	print("[Dice voice] I'm in")

@bot.command(aliases=["help", "what", "wat", "wot", "huh"])
async def cmdHelp(ctx):
	try:
		await ctx.channel.send(
			"""
				Hello! I'm YetAnotherDiceBot, and I'm yet another dice bot!

				`?roll`/`?r` is fairly simple:
					`?roll 2d6+1d4+d2-8` = Roll 2 d6's, add a d4 and a d2, then subtract 8
				Using the state of the art 	`?roll2`/`?r2` command, you can do the following:
					`?r2 (2d4)d4`  = Roll 2d4 then roll that many d4's
					`?r2 4d20k  `  = Roll 4 d20's and keep the highest
					`?r2 4d20kl `  = Above but keep the lowest
					Replace `k` with `d` to drop instead
					Keep/drop amount can be changed (4d4k3 keeps the higest 3)
					`?r2 d1,10,20` = Roll a 1, 10, or 20
					`?r2 d10..20`  = Basically just `?r2 d10+10`

				roll2 supports most Python operators as well as parenthesis, lists, and dicts:
					`+`, `-`, `*`, `/`,
					`**` (exponent), `%` (modulo), `//` (floor(x/y)),
					`>`, `>=`, `==`, `<=`, `<`, `!=` (not eaquals),
					Binary/bitwise: `&` (AND), `|` (OR), `^` (XOR), `<<` (x\*(2\*\*y)), `>>` (x//(2\*\*y))

					Single letters can be used as variables via `(a:=stuff)`

					Some named Python things can be used as well
						Lists: `min`, `max`, `sum`, `any`, `all`
						Types: `bool`, `int`, `float`, `str`, `list`
						Consts: `True`, `False`, `None`
						Bases: `hex`, `oct`, `bin`
						Strings: `len`, `lower`, `upper`
						Numbers: `round`,`floor`, `ceil`, `abs`, `real`, `imag`
						Logic: `and`, `or`, `not`
						Control: `if`, `else`, `in`
						Functions: `lambda`
						Modules: `math`, `cmath`
					Note: `min(1d4,1d8)` throws an error but `min(1d4, 1d8)` works as intended
					This ia parsing bug that I'm too lazy to fix

				`?choose` can be used like `?choose cats "cats and dogs"`
				You can also use `?ask` to ask me questions

				Bot built and maintained by Github@Scripter17

				This bot is licensed under the Don't Be a Dick public license.
				Type `?source` for this bot's source code
				""".replace("\n\t\t\t\t", "\n"), reference=ctx.message, mention_author=False)
	except discord.errors.HTTPException:
		await ctx.channel.send("Welp. the help message is more than 2000 chars", reference=ctx.message, mention_author=False)

@bot.command(aliases=["source", "sourcecode",  "source-code", "source_code"])
async def cmdSource(ctx):
	await ctx.channel.send("""
			Source code:
			Bot's source code: `https://github.com/Scripter17/public-discord-bots/blob/master/yadb.py`
			Dice algorithms: `https://github.com/Scripter17/public-discord-bots/blob/master/dice.py`
			License: AGPL-V3
			""".replace("\n\t\t\t", "\n")[1:], reference=ctx.message, mention_author=False)

@bot.command(aliases=["roll", "dice", "r", "r1"])
async def cmdDice(ctx):
	try:
		diceString=ctx.message.content.removeprefix(bot.command_prefix+ctx.invoked_with)
		diceString=diceString.removeprefix("`").removesuffix("`")
		if diceString.count("d") == 0:
			result = dice.rollDice(diceString) + "\nYou didn't actually roll any dice. 20 is always 20, 1d20 rolls a d20."
		else:
			result=dice.rollDice(diceString)
		await ctx.channel.send(result, reference=ctx.message, mention_author=False)
	except discord.errors.HTTPException as e:
		print(e)
		try:
			await ctx.channel.send(f"Can't send the whole calculation but your answer is {result.split(' = ')[1]}", reference=ctx.message, mention_author=False)
		except discord.errors.HTTPException as e:
			print(e)
			await ctx.channel.send(f"Result too big to send (>2000 chars)", reference=ctx.message, mention_author=False)
	except Exception as e:
		print(e)
		await ctx.channel.send(f"`{str(type(e))}: {str(e)}`", reference=ctx.message, mention_author=False)

@bot.command(aliases=["roll2", "dice2", "r2", "roll_advanced"])
async def cmdAdvDice(ctx):
	try:
		diceString=ctx.message.content.removeprefix(bot.command_prefix+ctx.invoked_with)
		diceString=diceString.removeprefix("`").removesuffix("`")
		result=dice.advancedRollDice(diceString)
		if "\"" in diceString or "'" in diceString:
			result+="\nString literals are a bit buggy. Sorry"
		await ctx.channel.send(result, reference=ctx.message, mention_author=False)
	except Exception as e:
		print(e)
		await ctx.channel.send(f"`{str(type(e))}: {str(e)}`", reference=ctx.message, mention_author=False)

@bot.command(aliases=["ask", "8ball", "8b", "16ball", "16b", "question"])
async def cmdAsk(ctx):
	answers={
		"0":"Yes",
		"1":"No",
		"2":"Eat hot coals",
		"3":"Maybe",
		"4":"Yeah sure",
		"5":"God I wish",
		"6":"Go ask santa",
		"7":"(0161) 496 0314",
		"8":"What are you, a cop?",
		"9":"Buy me a pizza first",
		"a":"What if the world was made of pudding?",
		"b":"Meow",
		"c":"Oh absolutely",
		"d":"Maybe? Hang on I need to make a few phone calls",
		"e":"@\u0307FBI",
		"f":"uwu"
	}
	msgBin=(str(ctx.message.author.id)+ctx.message.content).lower().encode("UTF-8")
	ret=hashlib.sha256(msgBin).hexdigest()
	if ret[1] in "01234567":
		ret=str(int(f"0x{ret[0]}", 16)%2)
	await ctx.channel.send(answers[ret[0]], reference=ctx.message, mention_author=False)

@bot.command(aliases=["choice", "choise", "choose", "chose", "pick"])
async def cmdChoose(ctx, *args):
	await ctx.channel.send(random.choice(args), reference=ctx.message, mention_author=False)

bot.run(os.environ["bot_yadb"])
