import safeNum, re, random
import math, cmath

def rollDice(dice):
	dice=re.findall(r"([+-]?(?:\d*d)?\d+)", dice.lower())
	rolls=[]
	for die in dice:
		if "d" in die:
			dieSign=-1 if die[0]=="-" else 1
			dieSize=int(die.split("d")[1])
			dieNum=abs(int(re.search(r"(\d*)d", die)[1] or "1")) # Jank to handle d6 as 1d6
			if dieNum>65535:
				raise ValueError(f"Too many dice ({count})")
			for i in range(dieNum):
				rolls.append(dieSign*random.randint(1, dieSize))
		else:
			rolls.append(int(die))
	return " + ".join(map(str, rolls))+" = "+str(sum(rolls))

r""" CLEAN VERSION
def rollDice(dice):
	dice=re.findall(r"([+-]?(?:\d*d)?\d+)", dice.lower())
	total=0
	for die in dice:
		if "d" in die:
			dieSign=-1 if die[0]=="-" else 1
			dieSize=int(die.split("d")[1])
			dieNum=abs(int(re.search(r"(\d*)d", die)[1] or "1")) # Jank to handle d6 as 1d6
			for i in range(dieNum):
				total+=dieSign*random.randint(1, dieSize)
		else:
			total+=int(die)
	return total
"""

def keep(arr, n, f):
	ret=0
	for _ in range(min(n, len(arr))):
		ret+=arr.pop(arr.index(f(arr)))
	return ret

def drop(arr, n, f):
	for _ in range(min(n, len(arr))):
		arr.pop(arr.index(f(arr)))
	return sum(arr)

def keepHigh(arr, n): return keep(arr, n, max)
def keepLow (arr, n): return keep(arr, n, min)
def dropHigh(arr, n): return drop(arr, n, max)
def dropLow (arr, n): return drop(arr, n, min)

def _sum(arr, n):
	return sum(arr)

def _rollDice(parsedDice):
	"""
		Process individual dice rolls including ranges, sides, and keeps
	"""
	count, sides, minimum, size, keep, keepn=parsedDice.groups(default="")
	count  =int(count   or "1")
	minimum=int(minimum or "1")
	keepn  =int(keepn   or "1")
	if size : size   =int(size)
	if sides: sides  =[int(x) for x in sides.split(",") if x]
	ret=[]
	if count>65535:
		raise ValueError(f"Too many dice ({count})")
	for ii in range(count):
		if sides:
			ret.append(random.choice(sides))
		else:
			ret.append(random.randint(minimum, size))
	return str({"k":keepHigh, "kl":keepLow, "d":dropHigh, "dl":dropLow, "":_sum}[keep](ret, keepn))

reCount= r"((?<!\))\d*)"
reMin  = r"(?:(\d+)\.\.)"
reSides= r"((?:\d+,)+\d+)"
reSize = r"(\d+)"
reMode =fr"(?:{reSides}|{reMin}?{reSize})"
reKeep = r"(?:([kd]l?)(\d+)?)?"
reDice =fr"{reCount}d{reMode}{reKeep}"

def advancedRollDice(diceString):
	ret=re.sub(reDice, _rollDice, diceString)
	if re.search(r"(?:\d\w+|\B)\(\d+\)", ret):
		ret=advancedRollDice(re.sub(r"(?:\d\w+|\B)\((\d+)\)", "\\1", ret))
	for sus in re.findall(r"(?i)\b[a-z_][a-z_\d]+\b", ret):
		if sus not in allowedVars:
			raise SyntaxError("Possible ACE detected: "+sus)
	else:
		ret=str(eval(re.sub(r"\b(\d+(?:\.\d+)?j?)\b", "safeNum.SafeNum(\\1)", ret)))
	return ret

allowedVars=[
	"min", "max", "sum",
	"any", "all",
	"bool", "int", "float", "str", "list",
	"True", "False", "None",
	"hex", "oct", "bin",
	"len", "lower", "upper",
	"round", "floor", "ceil", "abs", "real", "imag",
	"and", "or", "not",
	"if", "else", "in",
	"lambda",
	"math",  *[x for x in dir(math ) if not x.startswith("_")],
	"cmath", *[x for x in dir(cmath) if not x.startswith("_")],
]

floor=math.floor
ceil =math.ceil

_hex=hex
_oct=oct
_bin=bin

hex=lambda x:_hex(int(x))
oct=lambda x:_oct(int(x))
bin=lambda x:_bin(int(x))

if __name__=="__main__":
	import sys
	if "--1" in sys.argv:
		print(rollDice(sys.argv[1]))
	else:
		print(advancedRollDice(sys.argv[1]))
