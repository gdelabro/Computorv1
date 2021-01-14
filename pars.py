import sys
import re

def quit(msg = None):
	if msg is not None:
		print(msg)
	sys.exit(0)

def ft_sqrt(nb):
	mn = 0
	mx = nb if nb >= 1 else 1
	while mx - mn > 0.000000001:
		mid = (mn + mx) / 2
		if mid * mid < nb:
			mn = mid
		else:
			mx = mid
	return mx

class Equ_solver():
	def __init__(self, equation):
		equation = equation.replace(" ", "")
		self.sides = equation.split("=")
		if len(self.sides) is not 2:
			quit("only one equality accepted.")
		if "x" in equation or "o" in equation:
			quit("bad character found in equation.")
		self.x = {
			0 : 0,
			1 : 0,
			2 : 0,
			}
		self.x2 = {}
		self.degree = 0
		self.split_xs()
		self.reduct_form()
		if self.degree > 2:
			quit("The polynomial degree is stricly greater than 2, I can't solve.")
		if self.degree == 2:
			self.solve_equation_2()
		elif self.degree == 1:
			self.solve_equation_1()
		else:
			if self.x[0] == 0:
				print("All values of x are a solution.")
			else:
				print("The equation has no solution.")

	def split_xs(self):
		i = 0
		for side in self.sides:
			if not i:
				xs = self.x
			else:
				xs = self.x2
			if re.search("X[0-9]", side) or re.search("^[+][-]", side):
				quit("equation not well formated.")
			side = side.replace("-", "+-")
			side = side.replace("+X", "+1X")
			side = side.replace("-X", "-1X")
			side = side.replace("*X", "X")
			side = side.replace("X^", "x")
			side = side.replace("X", "x1")
			if len(side) > 0 and side[0] == "x":
				side = "1" + side
			if len(side) > 2 and side[0] == "+" and side[1] == "-":
				side = side[1:]
			vals = side.split("+")
			for val in vals:
				if val == "":
					quit("empty value found.")
				if "x" not in val:
					val += "x0"
				val_sep = val.split("x")
				if len(val_sep) is not 2:
					quit("equation is not well formated.")
				try:
					degree = int(val_sep[1])
					multiplicator = float(val_sep[0])
					xs[degree] += multiplicator
				except KeyError:
					xs[degree] = multiplicator
				except ValueError:
					quit("equation is not well formated.")
			i = 1

	def reduct_form(self):
		for key in self.x2:
			val = self.x2[key]
			try:
				self.x[key] -= val
			except KeyError:
				self.x[key] = -val
		print("Reduced form is: ", end="")
		wrote = 0
		for key in sorted(self.x):
			self.x[key] = round(self.x[key], 6)
			if self.x[key] == 0.0:
				continue
			if key > self.degree:
				self.degree = key
			val = self.x[key]
			if wrote > 0 and val > 0:
				print(" + ", end="")
			if val < 0 and wrote > 0:
				print(" - ", end="")
				val = -val
			if val.is_integer() is True:
				val = int(val)
			x_string = f"x^{key}"
			if key == 0:
				x_string = ""
			if key == 1:
				x_string = "x"
			print(f"{val}{x_string}", end="")
			wrote += 1
		if wrote == 0:
			print("0", end="")
		print(" = 0")
		print(f"Polynomial degree: {self.degree}")

	def solve_equation_2(self):
		a = self.x[2]
		b = self.x[1]
		c = self.x[0]
		discriminant = (b ** 2) - (4 * a * c)
		if discriminant == 0:
			print("Discriminant is 0, the solution is:")
			sol = round(-b / 2*a, 6)
			if sol.is_integer():
				sol = int(sol)
			print(sol)
		elif discriminant > 0:
			print("Discriminant is strictly positive, the two solutions are:")
			sol1 = round((-b - ft_sqrt(discriminant)) / (2 * a), 6)
			if sol1.is_integer():
				sol1 = int(sol1)
			sol2 = round((-b + ft_sqrt(discriminant)) / (2 * a), 6)
			if sol2.is_integer():
				sol2 = int(sol2)
			print(f"x1 = {sol1}\nx2 = {sol2}")
		else:
			print("Discriminant is strictly negative, the two solutions are:")
			discriminant = -discriminant
			sol = [round(-b / (2 * a), 6), round(ft_sqrt(discriminant) / (2 * a), 6)]
			print(f"x1 = {sol[0]} + {sol[1]}i\nx2 = {sol[0]} - {sol[1]}i")
		
	def solve_equation_1(self):
		print("The solution is:")
		sol = round(-self.x[0] / self.x[1], 6)
		if sol.is_integer() == True:
			sol = int(sol)
		print("x =", sol)
