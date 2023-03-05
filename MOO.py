class MOO():
	def __init__(self, dwrf: int, dial_size: int):
		self.dwrf_key = [int(d) for d in str(dwrf)]
		self.dial_count = len(self.dwrf_key)
		self.dial_size = dial_size
		self.lffs_key = [0]*(dial_size + 1)
		for d in self.dwrf_key: self.lffs_key[d] = 1
	
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
		
		print(f"D/WRF: {dwrf} | LF/FS: {lffs}")
		return True

def main():
	moo = MOO(4535, 6)
	answer = 3456
	moo.attempt(answer)
	
if __name__ == '__main__':
	main()