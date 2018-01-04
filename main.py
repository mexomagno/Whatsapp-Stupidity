#!/usr/bin/python
# coding: utf-8
import sys
import pyperclip
from getkey import getkey, keys

class PromptHistory:
	""" Represents a bash-like history record """

	def __init__(self, buffer_size=100):
		""" Creates a new prompt history with a fixed capacity """
		# history lines container
		self._buffer = list()
		# max entries
		self._max_buffer_size = buffer_size
		# navigation through entries
		# Position len(_buffer) means the current last entry
		self._peek_index = 0
		# last inputted line to store while peeking lines
		self._held_input = None

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
		# Set peek index to the end of the buffer
		self._peek_index = len(self._buffer)

	def peek_older(self):
		""" Get entry before the current """
		# If empty, return the current held input
		if len(self._buffer) == 0:
			return self._held_input
		# Peek older. When on top, always return the first entry
		self._peek_index = max(0, self._peek_index - 1)
		return self._buffer[self._peek_index]

	def peek_newer(self):
		""" Get entry after the current """
		# If empty, return the current held entry
		if len(self._buffer) == 0:
			return self._held_input
		# Peek newer. Wnen overflow, return the held input
		self._peek_index = min(len(self._buffer), self._peek_index + 1)
		if self._peek_index == len(self._buffer):
			return self._held_input
		return self._buffer[self._peek_index]

	def hold_current(self, s):
		self._held_input = s

	def is_peeking(self):
		return len(self._buffer) > 0 and self._peek_index < len(self._buffer)

	def print_contents(self):
		print "History contents: "
		for i in range(len(self._buffer)):
			print "\t{index}:\t{content}{arrow}".format(index=i, 
														content=self._buffer[i], 
														arrow="\t<------- peek index" if (i == self._peek_index) else "")
		if self._peek_index < 0 or  self._peek_index >= len(self._buffer):
			print "Peek index:\t{position}".format(position="START" if self._peek_index < 0 else "END")
		print "Held text:\t{}".format(self._held_input)

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
		sys.stdout.write("\r{prompt}{input_string} \b\033[K".format(prompt=enter_string_prompt, input_string=input_string))
		sys.stdout.flush()
		key = getkey()
		if key == keys.UP:
			# HISTORY UP
			currently_peeking = history.is_peeking()
			peek_value = history.peek_older()
			if peek_value is not None:
				# If not peeking, store current
				if not currently_peeking:
					history.hold_current(input_string)
				input_string = peek_value
			continue
		elif key == keys.DOWN:
			# HISTORY DOWN
			peek_value = history.peek_newer()
			if peek_value is not None:
				if peek_value != input_string:
					input_string = peek_value 
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
		# elif key == keys.CTRL_DELETE:
		# 	# Delete by word
		# 	if len(input_string) > 0:
		# 		input_string = input_string.rsplit(" ", 1)[0] + " "
		# 		if input_string == " ":
		# 			input_string = ""
		elif key == keys.CTRL_D or key == keys.ESC or key == keys.CTRL_C:
			print "\nQuitting..."
			sys.exit(0)
		elif key == keys.ENTER:
			# PROCESS
			if len(input_string) == 0:
				print "You must enter something!"
				continue
			print "\nYour text: '{}'".format(input_string)
			history.push(input_string)
			output = add_format(input_string, copy_to_clipboard=True)
			print "Success! Just paste somewhere"
			input_string = ""
		elif key == keys.LEFT or key == keys.RIGHT:
			pass
		else:
			# Remove tildes
			if key in u"áãâàä":
				key = "a"
			elif key in u"éẽêèë":
				key = "e"
			elif key in u"íĩîìï":
				key = "i"
			elif key in u"óõôòö":
				key = "o"
			elif key in u"úũûùü":
				key = "u"
			else:
				pass

			try:
				key = key.decode("ascii")
			except UnicodeDecodeError as e:
				# Weird symbol, just ignore
				continue
			except UnicodeEncodeError as e:
				continue
			# Normal character
			input_string += key

if __name__ == "__main__":
	main()



"""
TODO: 
	- Randomize format selection
	- Add extra fuck-up
		* Uppercases
		* Replace by similar characters (A->4, E->3...)
	- Fix line when exceeds rightmost character

"""