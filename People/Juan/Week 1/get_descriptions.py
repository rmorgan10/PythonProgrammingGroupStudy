#!/usr/bin/env python3


def set_desc(f_nm: str) -> str:
	"""
	Prompts the user for a description of each line in fname, appends the user
	input to that line
	:param f_nm: file where each line is formatted "item : *"
	:return: f_nm
	"""
	bltins = dir(__builtins__)
	skp = "S"
	with open(f_nm, "r") as f:
		lines = f.readlines()
	with open(f_nm, "a+") as f:
		print(f"Fill out what you can, type {skp} to skip")
		while len(bltins) > 0:
			for blt in bltins:
				for ln in lines:
					if blt in ln:
						lines.remove(ln)
						bltins.remove(blt)
						blt = None
						break
				try:
					if blt is None:
						continue
					desc = input(f"{blt} : ")
				except EOFError:
					return f_nm
				if desc == skp:
					continue
				ln = f"{blt} : {desc}\n"
				f.write(ln)
				bltins.remove(blt)
	return f_nm


if __name__ == '__main__':
	fname = "builtins.txt"
	set_desc(fname)
