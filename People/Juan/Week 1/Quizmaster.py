#!/usr/bin/env python3


def build_dict(f_name):
	desc_dict = {}
	lens = []
	with open(f_name, "r") as descriptions:
		for i, line in enumerate(descriptions):
			print(f"line {i} : {line}")
			lens.append(len(line.split(" : ")))
			#desc_dict.update({ln_1 : ln_2})
	print(filter(lambda l: l > 2, lens)[0])
	print(desc_dict)


if __name__ == '__main__':
	build_dict("builtins.txt")