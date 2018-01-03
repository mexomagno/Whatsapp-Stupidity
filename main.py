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
		self._peek_index = -1

	def push(self, s):
		""" Put a string at the end of the history """
		print "pushing '{}'".format(s)
		# push to list
		self._buffer.append(s)
		# If necessary, delete first
		if len(self._buffer) > self._max_buffer_size:
			self._buffer.pop(0)
		# Set peek index to last one
		self._peek_index = len(self._buffer)

	def peek_older(self):
		""" Get entry before the current """
		# If empty, return none
		if len(self._buffer) == 0:
			return None
		# If already at the end, return none
		if self._peek_index < 0:
			return None
		# Peek back
		self._peek_index -= 1
		# If peek index in the end, return None
		if self._peek_index < 0:
			return None
		return self._buffer[self._peek_index]

	def peek_newer(self):
		""" Get entry after the current """
		if len(self._buffer) == 0:
			return None
		if self._peek_index >= len(self._buffer):
			return None
		self._peek_index += 1
		if self._peek_index >= len(self._buffer):
			return None
		return self._buffer[self._peek_index]

	def print_history(self):
		print "History contents: "
		for i in range(len(self._buffer)):
			print "\t{index}:\t{content}{arrow}".format(index=i, 
														content=self._buffer[i], 
														arrow="\t<------- peek index" if (i == self._peek_index) else "")
		if self._peek_index < 0 or  self._peek_index >= len(self._buffer):
			print "\tPeek index: {position}".format(position="START" if self._peek_index < 0 else "END")

def test_history():
	print "History tester"

	buffer_size = 100
	print "Creating history with buffer of size {}".format(buffer_size)
	history = PromptHistory(buffer_size=buffer_size)
	input_str = ""

	history.push("Esto")
	history.push("es")
	history.push("una")
	history.push("prueba")
	history.push("del")
	history.push("historial")
	history.print_history()
	while True:
		print "Press up or down keys: "
		# Get keyboard input
		key = getkey()
		if key == keys.UP:
			print "UP"
			content = history.peek_older()
			print "Content: {}".format(content if content is not None else "START")
		if key == keys.DOWN:
			print "DOWN"
			content = history.peek_newer()
			print "Content: {}".format(content if content is not None else "END")
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