from MOO import MOO

def main():
	# FIXME: Read from cl
	basic_moo = MOO(4, 6, 8)
	basic_moo.set_code(4535)
	code_correct = False
	panel = {'D/WRF':0, 'LF/FS':0}
	
	while code_correct is not None:
		try:
			moo_code = int(input("Enter the MOO code:"))
			code_correct = basic_moo.try_code(moo_code)
			if not code_correct:
				print("ACCESS DENIED")
			else:
				print("ACCESS GRANTED")
				break
			print(f"{basic_moo.tries_history}")
		except ValueError:
			continue
		except Exception as ex:
			print(ex)

if __name__ == '__main__':
	main()