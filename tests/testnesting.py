import sys
if sys.version_info < (3, 0):
	import testcase
else:
	from . import testcase

class TestNesting(testcase.TestCase):

	title = "CSS Nesting"

	def test_nestings(self):
		self.set_text( self.input() )
		self.text_equals( self.input() )
		self.compile()
		self.text_equals( self.result() )
		self.decompile()
		self.text_equals( self.input() )

	def input(self):
		return """
	.header [
		h1 {}
		.title {} /* Comment */
	]

	.header [
		h1, h2, h3 { text-decoration:underline; }
		dl.the-item:nth-child(3n+1) > a {
			border:solid 2px green;
		}
	]
"""

	def result(self):
		return """
	/*.header [*/
		.header h1 {}
		.header .title {} /* Comment */
	/*]*/

	/*.header [*/
		.header h1, .header h2, .header h3 { text-decoration:underline; }
		.header dl.the-item:nth-child(3n+1) > a {
			border:solid 2px green;
		}
	/*]*/
"""
