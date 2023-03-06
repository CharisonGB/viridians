import sys
import argparse
from MOO import MOO

def get_basic_MOO_parser():
	parser = argparse.ArgumentParser(usage="basic_MOO.py <code> [-c|--dial-count] [-s|--dial-size] [-t|--max-tries]",
		description="Configure the Basic MOO.")
	parser.add_argument('code', action='store', type=int,
		help="set the correct code for this MOO; can fail against other args")
	parser.add_argument('-c', '--dial-count', action='store', type=int, default=4,
		help="the number of digits in the MOO code; defaults to 4")
	parser.add_argument('-s', '--dial-size', action='store', type=int, default=6,
		help="the maximum value of any digit in the MOO code; defaults to 6")
	parser.add_argument('-t', '--max-tries', action='store', type=int, default=8,
		help="the max number of tries to guess the MOO code; defaults to 8")
	return parser

def main():
	parser = get_basic_MOO_parser()
	args = vars(parser.parse_args(sys.argv[1:]))
	try:
		basic_moo = MOO(args['dial_count'], args['dial_size'], args['max_tries'])
		basic_moo.set_code(args['code'])
	except ValueError as ve:
		print(f"Failed to configure MOO.\n{ve}\nExiting...")
		exit(1)
	
	code_correct = False
	while code_correct is not None:
		try:
			moo_code = int(input("Enter the MOO code: "))
			code_correct = basic_moo.try_code(moo_code)
			if not code_correct:
				print("ACCESS DENIED")
			else:
				print("ACCESS GRANTED")
				break
			print(basic_moo.attempts_str())
		except ValueError as ve:
			print(f"{ve}\n")
			continue
		except KeyboardInterrupt:
			print("\nExiting...")
			exit(1)
		except Exception as ex:
			print(ex)
	
	print(basic_moo)

if __name__ == '__main__':
	main()
	exit(0)