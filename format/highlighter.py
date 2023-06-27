import re
import os

def highlight(type, code):
    # type: python, html, swift
	"pass a string and it will be highlighted"

	# keywords to be colored in orange
	keywords = {
        "python": ['and', 'assert', 'break', 'class', 'continue', 'def',
        'del', 'elif', 'else', 'except', 'exec', 'finally',
        'for', 'from', 'global', 'if', 'import', 'in',
        'is', 'lambda', 'not', 'or', 'pass', 'print',
        'raise', 'return', 'try', 'while', 'yield',
        'None', 'True', 'False',],
        "html": [],
        "swift": []
    }

	for k in keywords[type]:
		code = code.replace(k, "<b style='color:orange'>" + k + "</b>")

	code = code.replace("\n","<br>")

	# The 'indentation'
	code = code.replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")

	# functions to be colored in blue
	_def= re.findall("\w+\(", code)
	for w in _def:
		code = code.replace(w, "<b style='color:blue'>" + w[:-1] + "</b>(")
	return code


# html = highlight("""""")

# print(html)
#
# with open("code.html", "w") as file:
# 	file.write(html)
#
# os.startfile("code.html")
