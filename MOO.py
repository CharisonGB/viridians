class MOO():
	def __init__(self, dial_count: int, dial_size: int, max_attempts: int):
		self.dial_count = dial_count
		self.dial_size = dial_size
		
		self.max_attempts = max_attempts
		self.attempt_history = []
		
		self.code_min = int(str(1)*dial_count)
		self.code_max = int(str(dial_size)*dial_count)
		self.dwrf_key = [0]*dial_count
		self.lffs_key = [0]*(dial_size + 1)
	
	def set_code(self, moo_code: int):
		try:
			if self.code_max < moo_code or moo_code < self.code_min:
				raise ValueError(f"Code has exactly {self.dial_count} digits.")
			
			self.dwrf_key = [int(d) for d in str(moo_code)]
			
			if max(self.dwrf_key) > self.dial_size or min(self.dwrf_key) < 1:
				raise ValueError(f"Dial out of range {1}..{self.dial_size}.")
			
			for d in self.dwrf_key:
				self.lffs_key[d] = 1
		
		except ValueError as ve:
			print(f"Failed to set MOO code to {moo_code}: {ve}")
	
	
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
	moo = MOO(4, 6, 8)
	answer = 1349
	moo.set_code(answer)
	#moo.attempt(answer)
	#print(moo.attempt_history)
	
if __name__ == '__main__':
	main()