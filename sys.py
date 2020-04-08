import sys

def square(x):
	number = x*x
	return number

if len(sys.argv) == 1:
	print('there is no command line arg')

elif sys.argv[1]== 'square':
	print(square(2))