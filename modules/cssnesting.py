import sublime, re

#
# Primary functions
#

def apply(view, edit):
	append_selector_to_groupings(view, edit)
	comment_out_groupings(view, edit)

def remove(view, edit):
	uncomment_out_groupings(view, edit)
	strip_selector_from_groupings(view, edit)

def highlights(view):
	matches = get_groups_regions(view)
	highlights = []
	for region in matches:
		selector, contents = get_group_region_parts( view.substr(region) )
		highlights.append(sublime.Region(region.a, region.a + len(selector) - 1)) # add selector to highlights
		highlights.append(sublime.Region(region.b - 1, region.b)) # add close braket to highlights
	return highlights

#
# Helper functions
#

classname = '(\w|#|\.|:| |-|,|\*|\+|\"|\'|\=|\[|\]|>)+'

# returns group selector and [...] as regions array
def get_groups_regions(view):
	return view.find_all(''+ classname +'\s+?\[(.|\n)*?\}\s+\]')

# splits entire group region into selector and rule contents
def get_group_region_parts(text):
	text = text.rstrip()
	selector = text[0:text.find('[')]
	contents = text[text.find('['):len(text)]
	return selector, contents

#
# Content functions
#

# Adds group selector to each subselector within it
def append_selector_to_groupings(view, edit):
	matches = get_groups_regions(view)
	matches = reversed(matches)
	for region in (matches):
		# Get the selector and rule contents
		selector, contents = get_group_region_parts( view.substr(region) )
		# put group selector on each sub selector
		contents = re.sub('('+classname + ')(\s*?\{(.|\n)*?\})', selector.strip() +' \\1\\3', contents)
		# replace entire selection with fixed bit
		view.replace(edit, sublime.Region(region.a, region.b), selector + contents)

# Undoes the above function
def strip_selector_from_groupings(view, edit):
	matches = get_groups_regions(view)
	for region in reversed(matches):
		# Get the selector and rule contents
		selector, contents = get_group_region_parts( view.substr(region) )
		# put group selector on each sub selector
		contents = re.sub(selector.strip()+' ', '', contents)
		# replace entire selection with fixed bit
		view.replace(edit, sublime.Region(region.a, region.b), selector + contents)

# This comments out "classname [" and closing "]" groupings (so they don't ruin the css for production)
def comment_out_groupings(view, edit):
	# openings...
	matches = view.find_all(''+ classname +'\s+?\[')
	matches = reversed(matches)
	for region in (matches):
		text = view.substr(region)
		view.replace(edit, region, '/*' + text + '*/')
	# closings...
	matches = view.find_all('^( |\t)*\]')
	matches = reversed(matches)
	for region in (matches):
		text = view.substr(region)
		text = text.replace(']', '/*]*/')
		view.replace(edit, region, text)

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