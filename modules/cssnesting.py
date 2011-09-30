import sublime
import re

#
# Primary functions
#

def apply(view, edit):
	append_selector_to_groupings(view, edit)
	highlights = comment_out_groupings(view, edit)
	return highlights

def remove(view, edit):
	uncomment_out_groupings(view, edit)
	highlights = strip_selector_from_groupings(view, edit)
	return highlights

#
# Content functions
#

classname = '(\w|#|\.|:| |-|,|\*|\+|\"|\'|\=|\[|\]|>)+'

# returns group selector and [...] as regions array
def get_groups_regions(view):
	return view.find_all(''+ classname +'\s+?\[(.|\n)*?\}\s+\]')

def highlight(view, highlights):
	view.add_regions("css-nestings", highlights, 'constant.character', sublime.DRAW_OUTLINED)

# Adds group selector to each subselector within it
def append_selector_to_groupings(view, edit):
	matches = get_groups_regions(view)
	matches = reversed(matches)
	for region in (matches):
		# Get the text
		text = view.substr(region)
		text = text.rstrip()
		# grab the selctor and group contents
		selector = text[0:text.find('[')]
		contents = text[text.find('['):len(text)]
		# put group selector on each sub selector
		contents = re.sub('('+classname + ')(\s+\{(.|\n)*?\})', selector.strip() +' \\1\\3', contents)
		# replace entire selection with fixed bit
		view.replace(edit, sublime.Region(region.a, region.b), selector + contents)

# Undoes the above function
def strip_selector_from_groupings(view, edit):
	matches = get_groups_regions(view)
	matches = reversed(matches)
	highlights = []
	for region in (matches):
		# Get the text
		text = view.substr(region)
		text = text.rstrip()
		# grab the selctor and group contents
		selector = text[0:text.find('[')]
		contents = text[text.find('['):len(text)]
		# put group selector on each sub selector
		contents = re.sub(selector.strip()+' ', '', contents)
		# replace entire selection with fixed bit
		view.replace(edit, sublime.Region(region.a, region.b), selector + contents)
		# show notification of affected areas
		highlights.append( sublime.Region(region.a, region.a + len(selector) - 1) )
	return highlights

# This comments out "classname [" and closing "]" groupings (so they don't ruin the css for production)
def comment_out_groupings(view, edit):
	highlights = []
	# openings...
	matches = view.find_all(''+ classname +'\s+?\[')
	matches = reversed(matches)
	for region in (matches):
		text = view.substr(region)
		highlights.append(region)
		view.replace(edit, region, '/*' + text + '*/')
	# closings...
	matches = view.find_all('^( |\t)*\]')
	matches = reversed(matches)
	for region in (matches):
		text = view.substr(region)
		text = text.replace(']', '/*]*/')
		highlights.append(region)
		view.replace(edit, region, text)
	return highlights

# This undo's the "comment_out_groupings"
def uncomment_out_groupings(view, edit):
	# openings...
	matches = view.find_all('\/\*'+ classname +'\s+?\[\*\/')
	matches = reversed(matches)
	for region in (matches):
		text = view.substr(region)
		text = text.replace('/*', '').replace('*/', '')
		view.replace(edit, region, text)
	# closings...
	matches = view.find_all('\/\*\]\*\/')
	matches = reversed(matches)
	for region in (matches):
		text = view.substr(region)
		view.replace(edit, region, ']')



