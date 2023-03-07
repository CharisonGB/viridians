# Virtualized Mechanically Operated Opener
if __name__ == '__main__':
	print("Virtualized Mechanically Operated Opener (VMOO)")
	exit(0)

class MOO():
	def __init__(self, dial_count: int, dial_size: int, max_tries: int):
		self.dial_count = dial_count
		self.dial_max = dial_size
		lg = lambda b, n : 0 if n//b <= 0 else 1+lg(b, n//b) # evil recursive lambda
		self.dial_width = lg(10, dial_size) + 1
		
		self.max_tries = max_tries
		self.tries_history = []
		
		self.code = ""
		self.dwrf_key = [0]*dial_count
		self.lffs_key = [0]*(dial_size + 1)
	
	def configs_str(self):
		configs_str = f"- CONFIGS \n"
		configs_str = f"{configs_str}  | DIALS:\t{self.dial_count}x(1..{self.dial_max})\n"
		configs_str = f"{configs_str}  | CODE:\t{self.code}\n"
		return configs_str
	
	def attempts_str(self):
		attempts_str = "".join([f"  | TRY:{a['TRY']} --> [ D/WRF:{a['D/WRF']} | LF/FS:{a['LF/FS']} ]\n" for a in self.tries_history])
		attempts_str = f"- ATTEMPTS \n{attempts_str}"
		attempts_str = f"{attempts_str}  | ATTEMPTS REMAINING:\t{self.calc_remaining_tries()}\n"
		return attempts_str
	
	def __str__(self):
		moo_str = f"{self.configs_str()}{self.attempts_str()}"
		return moo_str
	
	def parse_code(self, moo_code: str):
		if len(moo_code) != self.dial_width * self.dial_count:
			raise ValueError(f"Code must be expressed with exactly {self.dial_count}, {self.dial_width}-wide digits.")
		dial_values = [int(moo_code[dial*self.dial_width:(dial+1)*self.dial_width])
			for dial in range(self.dial_count)] # incomprehensible list comprehension, lmao
		if max(dial_values) > self.dial_max or min(dial_values) < 1:
			raise ValueError(f"One or more dials are out of range ({1}..{self.dial_max}).")
		return dial_values
	
	def set_code(self, moo_code: str):
		try:
			self.dwrf_key = self.parse_code(moo_code)
			for d in self.dwrf_key:
				self.lffs_key[d] = 1
			self.code = moo_code
		except ValueError as ve:
			raise ValueError(f"Failed to set MOO code to {moo_code}.\n{ve}")
	
	def calc_remaining_tries(self):
		return self.max_tries - len(self.tries_history)
	
	def calc_dwrf(self, dial_values: [int]):
		dwrf = 0
		for dial_val, dwrf_val in zip(dial_values, self.dwrf_key):
			if dial_val == dwrf_val:
				dwrf += 1
		return dwrf
	
	def calc_lffs(self, dial_values: [int]):
		lffs_key = self.lffs_key.copy()
		lffs = -self.calc_dwrf(dial_values)
		for dial_val in dial_values:
			lffs += lffs_key[dial_val]
			lffs_key[dial_val] = 0
		return lffs if lffs >= 0 else 0
	
	def try_code(self, moo_code: str):
		try:
			dial_values = self.parse_code(moo_code)
			dwrf = self.calc_dwrf(dial_values)
			lffs = self.calc_lffs(dial_values)
			self.tries_history.append({'TRY':moo_code, 'D/WRF':dwrf, 'LF/FS':lffs})
			if self.max_tries != 0 and self.calc_remaining_tries() <= 0:
				return None
			return moo_code == self.code
		except ValueError as ve:
			raise ValueError(f"{moo_code} is an invalid MOO code.\n{ve}")