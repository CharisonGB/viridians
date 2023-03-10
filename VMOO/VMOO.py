# Virtualized Mechanically Operated Opener
if __name__ == '__main__':
	print("Virtualized Mechanically Operated Opener (VMOO)")
	exit(0)

class MOO():
	def __init__(self, dial_count: int, dial_size: int, max_tries: int):
		self.dial_count = dial_count
		self.dial_size = dial_size if 0 < dial_size <= 9 else 9
		
		self.max_tries = max_tries
		self.tries_history = []
		
		self.code = 0
		self.code_min = int(str(1)*dial_count)
		self.code_max = int(str(dial_size)*dial_count)
		self.dwrf_key = [0]*dial_count
		self.lffs_key = [0]*(dial_size + 1)
	
	def configs_str(self):
		configs_str = f"- CONFIGS \n"
		configs_str = f"{configs_str}  | DIALS:\t{self.dial_count}x(1..{self.dial_size})\n"
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
	
	def validate_code(self, moo_code: int):
		if self.code_max < moo_code or moo_code < self.code_min:
			raise ValueError(f"Code must have exactly {self.dial_count} digits.")
		dial_values = [int(dial_val) for dial_val in str(moo_code)]
		if max(dial_values) > self.dial_size or min(dial_values) < 1:
			raise ValueError(f"One or more dials are out of range ({1}..{self.dial_size}).")
		return dial_values
	
	def set_code(self, moo_code: int):
		try:
			self.dwrf_key = self.validate_code(moo_code)
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
	
	def try_code(self, moo_code: int):
		try:
			dial_values = self.validate_code(moo_code)
			dwrf = self.calc_dwrf(dial_values)
			lffs = self.calc_lffs(dial_values)
			self.tries_history.append({'TRY':moo_code, 'D/WRF':dwrf, 'LF/FS':lffs})
			if self.max_tries != 0 and self.calc_remaining_tries() <= 0:
				return None
			return moo_code == self.code
		except ValueError as ve:
			raise ValueError(f"{moo_code} is an invalid MOO code.\n{ve}")