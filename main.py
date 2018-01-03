#!/usr/bin/python
# coding: utf-8
import sys
import pyperclip
from getkey import getkey, keys

class PromptHistory:
	""" Represents a bash-like history record """

	def __init__(self, buffer_size=100):
		self._buffer = list()
		self._max_buffer_size = buffer_size
		self._peek_index = 0
		self.reset_peek_index()

	def push(self, s):
		""" Put a string at the end of the history """
		print "pushing '{}'".format(s)
		pass

	def peek_older(self):
		""" Get entry before the current """
		print "peeking older"
		pass

	def peek_newer(self):
		""" Get entry after the current """
		print "peeking newer"
		pass

	def reset_peek_index(self):
		""" Return peek index to the last one """
		print "Reseting peek index"
		self._peek_index = len(list()) - 1

	def print_history(self):
		print "History contents: "
		for i in range(len(self._buffer)):
			print "\t{index}:\t{content}{arrow}".format(i, self._buffer[i], "<------- peek index" if (i == self._peek_index) else "")


def test_history():
	print "History tester"

	buffer_size = 100
	print "Creating history with buffer of size {}".format(buffer_size)
	history = PromptHistory(buffer_size=buffer_size)
	input_str = ""

	history.print_history()
	while True:
		print "Press up or down keys: "
		# Get keyboard input
		key = getkey()
		if key == keys.UP:
			print "UP"
		if key == keys.DOWN:
			print "DOWN"
		if key == 'q':
			break
	print "quit"


def add_format(input_string):
	output = ""
	formatting = "_*~ "
	format_index = 0
	for letter in input_string:
		if letter == " ":
			# extra spaces
			output = "{output}  ".format(output=output)
		else:
			output = "{output} {formatting}{letter}{formatting}".format(
				output=output,
				formatting=(formatting[format_index] if formatting[format_index] != " " else ""),
				letter=letter)
		format_index = (format_index + 1 ) % len(formatting)
	pyperclip.copy('{}'.format(output))
	return output

def quit():
	print "\nQuitting..."
	sys.exit(0)

def main():
	# get input text
	input_string = ""
	for i in range(1, len(sys.argv)):
		input_string += " {}".format(sys.argv[i])
	input_string = input_string.strip();
	if input_string != "":
		# Convert and exit
		output = add_format(input_string)
		print "Your new text is in the clipboard!"
		print "Output is: {}".format(output)		
		sys.exit()

	# Convert infinitely in a loop
	while True:
		try:
			input_string = raw_input("Your text here (ctrl+D to exit): ")
		except KeyboardInterrupt:
			quit()
		except EOFError:
			quit()
		if len(input_string) == 0:
			print "You must enter something"
			continue
		output = add_format(input_string)
		print "Success! Just paste somewhere"


if __name__ == "__main__":
	# main()
	test_history()



"""
TODO: 
	- Fix tildes
	- Add history (bash-like)
	- Randomize format selection
	- Add extra fuck-up
		* Uppercases
		* Replace by similar characters (A->4, E->3...)

"""