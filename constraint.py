import urlparse
from parse_domain import parse_domain

class Constraint:
	DEPTH = 2
	def __init__(self):
		self.depth = 0

	def inherit(self, base_url, url):
		base_up = urlparse.urlparse(base_url)
		up = urlparse.urlparse(url)

		base_domain = parse_domain(base_url, 2)
		domain = parse_domain(url, 2)

		if base_domain != domain:
			return None

		if self.depth >= Constraint.DEPTH: # only crawl two levels
			return None
		else:
			new_constraint = Constraint()
			new_constraint.depth = self.depth + 1

			return new_constraint
