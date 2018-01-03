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
		self._held_input = ""

	def push(self, s):
		""" Put a string at the end of the history """
		# Avoid push if equals to the last entry
		if len(self._buffer) > 0 and self._buffer[-1] == s:
			return
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
			return self._held_input
		if self._peek_index >= len(self._buffer):
			return self._held_input
		self._peek_index += 1
		if self._peek_index >= len(self._buffer):
			return self._held_input
		return self._buffer[self._peek_index]

	def hold_current(self, s):
		self._held_input = s

	def is_peeking(self):
		return len(self._buffer) > 0 and 0 <= self._peek_index < len(self._buffer)

	def print_contents(self):
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


def add_format(input_string, copy_to_clipboard=True):
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
	if copy_to_clipboard:
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
	# create history
	history = PromptHistory(10)
	enter_string_prompt = "Your text here (ctrl+D to exit) >>> "
	while True:
		sys.stdout.write("\r{prompt}{input_string} \b".format(prompt=enter_string_prompt, input_string=input_string))
		sys.stdout.flush()
		key = getkey()
		if key == keys.UP:
			# HISTORY UP
			# save current entry on current history position
			if not history.is_peeking():
				peek_value = history.peek_older()
				if peek_value is not None:
					history.hold_current(input_string)
					input_string = peek_value
				continue
		elif key == keys.DOWN:
			# HISTORY DOWN
			if history.is_peeking():
				input_string = history.peek_newer()
		elif key == keys.BACKSPACE:
			# DELETE LAST
			if len(input_string) > 0:
				input_string = input_string[:len(input_string)-1]
		elif key == keys.CTRL_V:
			# PASTE
			# read from clipboard
			clipboard = pyperclip.paste()
			try:
				clipboard.decode("ascii")
			except UnicodeDecodeError as e:
				# Wrong contents on clipboard. Ignore
				continue
			# Append to current input
			input_string += clipboard
		elif key == keys.ENTER:
			# PROCESS
			if len(input_string) == 0:
				print "You must enter something!"
				continue
			print "\nYour text: '{}'".format(input_string)
			output = add_format(input_string, copy_to_clipboard=True)
			print "Success! Just paste somewhere"
			input_string = ""
			continue
		else:
			try:
				key = key.decode("ascii")
			except UnicodeDecodeError as e:
				# Weird symbol, just ignore
				continue
			# Normal character
			input_string += key

if __name__ == "__main__":
	main()



"""
TODO: 
	- Fix tildes
	- Add history (bash-like)
	- Randomize format selection
	- Add extra fuck-up
		* Uppercases
		* Replace by similar characters (A->4, E->3...)

"""