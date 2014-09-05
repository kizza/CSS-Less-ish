#
# CSS functions
# referencing http://caniuse.com/ and http://jsfiddle.net/simevidas/udyTs/show/light/
#

def box_shadow(value):
	return output([
		'-webkit-box-shadow: '+value+';',
		# '   -moz-box-shadow: '+value+';',
		'        box-shadow: '+value+''
	])

def transition(value):
	return output([
		'-webkit-transition: '+value+';',
		# '   -moz-transition: '+value+';',
		# '    -ms-transition: '+value+';',
		# '     -o-transition: '+value+';',
		'        transition: '+value+''
	])

def transform(value):
	return output([
		'-webkit-transform: '+value+';',
		'    -ms-transform: '+value+';',
		'        transform: '+value+''
	])

def linear_gradient(value):
	value1 = value
	value2 = value
	if value.count(',')==1: 		# default direction
		value1 = 'bottom, '+value
		value2 = 'to top, '+value
	elif value.count(',') == 2:	# sent direction (for formatting)
		args = value.split(',')
		direction = args.pop(0)
		if direction.strip() == 'to bottom':
			value1 = 'top, '+ ', '.join(args)
		elif direction.strip() == 'to top':
			value1 = 'bottom, '+ ', '.join(args)
	return output([
		'background-image: -webkit-linear-gradient('+value1+');',
		'background-image: linear-gradient('+value2+')'
	])

def output(bits):
	for i, item in enumerate(bits):
		if i > 0:
			bits[i] = "\t"+item
	return "\n".join(bits)