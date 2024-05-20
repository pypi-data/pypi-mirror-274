


def find_venture (ventures, name):
	for venture in ventures:
		if (name == venture ["name"]):
			return venture;
			
	raise Exception (f"Venture with name '{ name }' not found.")