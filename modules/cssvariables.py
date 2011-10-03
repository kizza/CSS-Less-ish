import sublime

#
# Primary functions
#

def apply(view, edit):
	remove_region_cache(view, edit)
	trim_entire_content(view, edit)
	append_region_cache(view, edit)

def remove(view, edit):
	apply_region_cache(view, edit)
	remove_region_cache(view, edit)

def highlights(view):
	return view.find_all("@(\w|-)+")

#
# Content functions
#

region_cache_name = "Variables"

# Returns dictionary of variables a.  Finds a match of _@varname = "value"_ rather than looking specifically within comments (ie assumes variable names DONT have = usually)
def get_css_variables_dict(view):
	# match all @var = "value", or @var='value' or @var-name = 'value'
	matches = view.find_all("@(\w|-)+\s?+=\s?+(\"|\')[^(\"|\')]+(\"|\')",0) 
	d = {}
	#print view.substr(matches)
	for match in matches:
		# grab the actual text matched @var = "val" and split up
		text = view.substr(match)
		varname ,value = text.split("=")
		# format variable name text
		varname = varname.replace('@', '').strip()	
		# format value text
		value = value.replace('\"', '').replace("\'", '').strip()
		# add to dictionary
		d[varname] = value
	return d

def get_first_comment(view):
	return view.find(r"\/\*+(\*|\w|\W)*?\*\/",0)  # better

def get_content(view):
	return view.substr(sublime.Region(0, view.size())).encode('utf-8')

def trim_entire_content(view, edit):
	#text = get_content(view).rstrip()
	#view.replace(edit, sublime.Region(0, view.size()), text)
	while True:
		line_region = view.line(view.size())
		line = view.substr(line_region).strip()
		if line == '':
			view.replace(edit, sublime.Region(line_region.a - 1, line_region.b), '')
		else:	
			break;

#
# Region cache functions
#

def get_region_cache(view):
	return view.find("\/\*+\s?+"+region_cache_name +"[^\*\/]*\*\/", 0) 

def remove_region_cache(view, edit):
	region = get_region_cache(view)
	if region:
		view.replace(edit, region, '')
	return

# Converts variables to their values and appends region indexes to the bottom (to be parsed later)
def append_region_cache(view, edit):
	variables = get_css_variables_dict(view)
	docblock = get_first_comment(view)
	if not docblock:
		print "No first comment found"
		return
	# Loop through region matches (outside of the docblock)
	offset = docblock.b
	match = view.find("@(\w|-)+", offset)
	pos = {} # assoc array of a:b string pairs
	highlight = []
	for varname in variables:
		pos[varname] = []
	while match:
		varname = view.substr(match).replace('@', '')
		if varname in variables:
			value = variables[varname]
			view.replace(edit, match, value)
			offset = match.a + len(value)
			pos[varname].append(str(match.a) + ":" + str(offset))	# store in pos dict
			highlight.append( sublime.Region(match.a, offset) )	# store replaced region for highlighting
		else:
			offset+=1
		match = view.find("@(\w|-)+", offset)	# go again
	# Compile the output	
	output = []
	for varname in variables:
		if pos[varname]:
			output.append ( varname +"{" + ','.join( pos[varname] ) + "}" )
	if len(output) > 0:
		cache = "/* " + region_cache_name + ":"
		cache+= '.'.join(output)
		cache+= " */"
		view.insert(edit, view.size(), "\n\n"+cache)
	return highlight

# Returns cache regions as array[varname] = [ [n,n], [n,n] ]
def parse_region_cache(view):
	region = get_region_cache(view)
	if not region:
		#print "No region cache found"
		return
	cache = view.substr( get_region_cache(view) )
	cache = cache.replace('/* '+region_cache_name+':', '').replace(' */', '')
	regions = {}
	# Break into section
	sections = cache.split('.')
	for section in sections:
		varname, data = section.split('{')
		data = data.replace('}', '')
		pos = data.split(',') 	# array of n:n, n:n
		regions[varname] = []	# empty list for each variable key
		for pair in pos:
			a, b = pair.split(':')	
			regions[varname].append([int(a), int(b)])
	return regions

# Uses parsed region cache to re-apply the variable names within the content
def apply_region_cache(view, edit):
	data = {}		# assoc array with key 'a' as position index - storing 'varname' and related 'b' value
	ordering = []	# ordered array by a region's 'a' index
	parsed = parse_region_cache(view)
	if parsed:
		# Create data and ordering objects
		for varname in parsed:
			for pos in parsed[varname]:
				data[pos[0]] = {'varname':varname, 'b':pos[1]}
				ordering.append(pos[0])
		# sort and reverse ordering - replacing regions from bottom to top 
		ordering.sort()
		for a in reversed(ordering):
			b = data[a]['b']
			varname = data[a]['varname']
			view.replace(edit, sublime.Region(a, b), '@'+varname)
		# # highlight from top to bottom - accounting for 'shifting' regions during above replacement
		# diff = 0	
		# for a in ordering:
		# 	b = data[a]['b']
		# 	varname = data[a]['varname']
		# 	highlights.append(sublime.Region(diff + a, diff + a + len('@'+varname)))	
		# 	diff+= len('@'+varname) - (b-a)