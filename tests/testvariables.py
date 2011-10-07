import testcase

class TestVariables(testcase.TestCase):

	title = "CSS Variables"

	def test_variables(self):
		self.set_text( self.text() )
		self.compile()
		# check variables exist with correct values
		self.variable_equals('var1', 'val1')
		self.variable_equals('var2', 'val2')
		self.variable_equals('var3', 'val3')
		self.variable_equals('var4', 'val1')	# referenced
		# check variables have been swapped in
		self.find('colour1: val1;')
		self.find('colour2: val2;')
		self.find('colour3: val3;')
		self.find('colour4: val1;')
		# check restoring resets variables
		self.decompile()
		self.find('colour1: @var1;')
		self.find('colour2: @var2;')
		self.find('colour3: @var3;')
		self.find('colour4: @var4;')

	def text(self):
		return """
/*
* @var1 =  "val1" // Comment
* @var2 ='val2'
* @var3= val3 
* @var4 =  @var1 // Variable reference
*/

h1 { colour1: @var1;/* comment */}
h2 { colour2: @var2;// comment}
h3 { colour3: @var3;}
h4 { colour4: @var4;}

"""
