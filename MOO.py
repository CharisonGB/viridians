class MOO():
	def __init__(self, dwrf: int, dial_size: int, max_attempts: int):
		self.dwrf_key = [int(d) for d in str(dwrf)]
		self.lffs_key = [0]*(dial_size + 1)
		for d in self.dwrf_key: self.lffs_key[d] = 1
		
		self.dial_count = len(self.dwrf_key)
		self.dial_size = dial_size
		
		self.max_attempts = max_attempts
		self.attempt_history = []
	
	def calc_remaining_attempts(self):
		return self.max_attempts - len(self.attempt_history)
	
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
		return lffs
	
	def attempt(self, answer: int):
		dial_values = [int(a) for a in str(answer)]
		dwrf = self.calc_dwrf(dial_values)
		lffs = self.calc_lffs(dial_values)
		self.attempt_history.append(f"TRY:{answer} | D/WRF:{dwrf} | LF/FS:{lffs}")
		if self.max_attempts != 0 and self.calc_remaining_attempts() <= 0:
			return None
		return dwrf, lffs

def main():
	moo = MOO(4535, 6, 8)
	answer = 3456
	moo.attempt(answer)
	print(moo.attempt_history)
	
if __name__ == '__main__':
	main()