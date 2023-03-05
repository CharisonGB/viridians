class MOO():
	def __init__(self, dwrf: int, dial_size: int):
		self.dwrf_key = [int(d) for d in str(dwrf)]
		self.dial_count = len(self.dwrf)
		self.dial_size = dial_size
		self.lffs_key = [0]*dial_size
		for d in self.dwrf: self.lffs_key[d] = 1
	
	#def calc_lffs(self):

def main():
	moo = MOO(1425, 6)
	print(moo.lffs_key)
	
if __name__ == '__main__':
	main()