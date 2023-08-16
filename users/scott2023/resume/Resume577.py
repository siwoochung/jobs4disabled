# Datbase for the Library
class Book:
	def __init__(self,title,author,isbn):
		self.title = title
		self.author = author
		self.isbn = isbn

class Library:
	def __init__(self, name):
		self.name = name # Library
		self.books = []
	# Method that adds book in to self.books(list of books in library)
	def add_book(self,book):
		self.books.append(book)

	# Method that display all the books in Library
	def display_books(self):
		if len(self.books) == 1: # when there is only one book in the library
			print(f"There is {len(self.books)} book in {self.name}:")
		else:
			print(f"There are {len(self.books)} books in {self.name}:")
		for book in self.books:
			print(f"\t-{book.title} by {book.author}")

	# Method should return true, if there is a book in the library, False otherwise.
	# self.books = [book1,book2,book3,book4,...., bookN]
	def find_book_isbn(self,isbn):
		for book in self.books:
			if book.isbn == isbn:
				print(f"We have {book.isbn} which is {book.title}")
				return True
			else:
				print(f"Sorry, we don't have a book with {isbn}")
				return False
	def find_book_title(self,title):
		found_books = []
		for book in self.books:
			if title in book.title:
				found_books.append(book.title)
		if len(found_books) == 0:
			print(f"Sorry, we don't have {title}")
			return False
		return found_books

book1 = Book("Harry Potter","J.K. Rowling","12345")
library1 = Library("Fiction Library")
print(library1.books)
library1.add_book(book1) # adding book1 into library1 using method add_book
print(library1.books)
library1.display_books()

book2 = Book("The Lightning Thief","Rick Riordan","39291")
book3 = Book("The Hunger Games","Suzanne Collins","23441")
book4 = Book("Harry Potter2","J.K. Rowling","12346")
library1.add_book(book2)
library1.add_book(book3)
library1.add_book(book4)
library1.display_books()
library1.find_book_isbn("99999")
library1.find_book_isbn("12345")
print(library1.find_book_title("Harry Potter"))



# Exceptions: Things that go wrong within our program (Error)

print('Hello, word')

# try & except
# In python, try & except are ways of testing the user input before somthing goes wrong

# try:
# 	x = int(input("Enter a number"))
# except ValueError: #When we get the ValueError from the code under try
# 	print("x is not an integer")

# If you try to divide any number by 0 , you get ZeroDivisionError
y = 100
z = 0
try:
	print(y/z)
except ZeroDivisionError:
	print("Watch out, denominator is 0")



# try:
# 	x = int(input("Enter a number"))
# except ValueError: #When we get the ValueError from the code under try
# 	print("x is not an integer")
# else: # If there is no ValueError go to here
# 	print(x)


# Ask users to enter their age. If they enter something that is not integer, ask them to
# re-enter the age. This should be repeated untill user put the correct input.
# while True:
# 	try:
# 		age = int(input("Enter your age:"))
# 	except ValueError:
# 		print("Enter Again!")
# 	else:
# 		print("Your age: ",age)
# 		break


# 'assert' to test functions in python

# example should return a+b
def example(a,b):
	return a+b

# You done any errory, if the function returns the expected values
# otherwise, you get assertion error, 
assert example(2,3) == 5
assert example(-10,-2) == -12
assert example(0,-2) == -2


# Implement a program that probmpts the user for a fraction, formatted as X/Y
# X and Y are integers. Then outputs the result as percentange
# If the percentage is 1% or less print "Empty". And if the pertage is larger than 99%,
# print "Full"

# If, though, X or Y is not an integer, X is greater than Y, or Y is 0, ask user to enter
# the fraction again. 

fraction = "A/B"

fraction = "5/7"
X,Y = fraction.split("/")
print(X)
print(Y)











