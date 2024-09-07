class SafeNum:
	def __init__(self, num):
		if isinstance(num, SafeNum):
			self.num=num.num
		else:
			self.num=num

	# General math
	def __add__     (self, other): return SafeNum(self.num+ SafeNum(other).num)
	def __sub__     (self, other): return SafeNum(self.num- SafeNum(other).num)
	def __mul__     (self, other): return SafeNum(self.num* SafeNum(other).num)
	def __matmul__  (self, other): return SafeNum(self.num@ SafeNum(other).num) # Yeah idk why this exists either
	def __truediv__ (self, other): return SafeNum(self.num/ SafeNum(other).num)
	def __floordiv__(self, other): return SafeNum(self.num//SafeNum(other).num)
	def __mod__     (self, other): return SafeNum(self.num% SafeNum(other).num)
	
	def __radd__     (self, other): return self+ other
	def __rsub__     (self, other): return self- other
	def __rmul__     (self, other): return self* other
	def __rmatmul__  (self, other): return self@ other
	def __rtruediv__ (self, other): return self/ other
	def __rfloordiv__(self, other): return self//other
	def __rmod__     (self, other): return self% other

	# THe entire reason this class exists
	def __pow__(self, other, mod=None):
		if abs(self)*complex(other).real>=100000:
			raise ValueError(f"An exponentiation that's too big was detected ({self}**{other})")
		return SafeNum(pow(self.num, SafeNum(other).num, mod))
	def __rpow__(self, other, mod=None): return pow(self, other, mod)

	# Binary ops
	def __and__   (self, other): return SafeNum(self.num& SafeNum(other).num)
	def __xor__   (self, other): return SafeNum(self.num^ SafeNum(other).num)
	def __or__    (self, other): return SafeNum(self.num| SafeNum(other).num)
	def __lshift__(self, other): return SafeNum(self.num<<SafeNum(other).num)
	def __rshift__(self, other): return SafeNum(self.num>>SafeNum(other).num)

	def __rand__   (self, other): return self& other
	def __rxor__   (self, other): return self^ other
	def __ror__    (self, other): return self| other
	def __rlshift__(self, other): return self<<other
	def __rrshift__(self, other): return self>>other

	# Monads
	def __pos__   (self): return SafeNum(+self.num)
	def __neg__   (self): return SafeNum(-self.num)
	def __invert__(self): return SafeNum(~self.num)
	def __trunc__ (self): return SafeNum(self.num.__trunc__()) # I trust nothing at this point
	def __round__ (self): return SafeNum(round(self.num))
	def __abs__   (self): return SafeNum(abs  (self.num))

	# Comparison
	def __gt__(self, other): return SafeNum(self.num> SafeNum(other).num)
	def __ge__(self, other): return SafeNum(self.num>=SafeNum(other).num)
	def __eq__(self, other): return SafeNum(self.num==SafeNum(other).num)
	def __le__(self, other): return SafeNum(self.num<=SafeNum(other).num)
	def __lt__(self, other): return SafeNum(self.num< SafeNum(other).num)
	def __ne__(self, other): return SafeNum(self.num!=SafeNum(other).num)

	# Type conversion
	def __bool__   (self): return bool(self.num)
	def __int__    (self): return int(self.num)
	def __float__  (self): return float(self.num)
	def __complex__(self): return complex(self.num)

	# Formatting
	def __str__ (self): return str(self.num)
	def __repr__(self): return str(self)
