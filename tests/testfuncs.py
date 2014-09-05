import sys, re
if sys.version_info < (3, 0):
	import testcase
	import modules.cssfuncs as funcs
else:
	from . import testcase
	from ..modules import cssfuncs as funcs


class TestFunctions(testcase.TestCase):

	title = "CSS Functions"

	def test_functions(self):
		self.set_text( self.input() )
		self.text_equals( self.input() )
		self.compile()
		self.find( re.escape(self.result()) )
		self.decompile()
		self.text_equals( self.input() )

	def vars(self):
		return """
/*
* @box-shadow    = box-shadow(0 0 4px #ff0)
* @transition    = transition(all 0.3s ease)
* @transform     = transform(rotate(7.deg))
* @gradient1     = linear-gradient(#fff, #f00)
* @gradient2     = linear-gradient(to top, #fff, #f00)
* @gradient3     = linear-gradient(to bottom , #fff, #f00)
*/
"""

	def input(self):
		return self.vars()+"""
h1 {
	@box-shadow;

	@transform;

	@transition;

	@gradient1;

	@gradient2;

	@gradient3;
}
"""

	def result(self):
		return self.vars()+"""
h1 {
	-webkit-box-shadow: 0 0 4px #ff0;
	        box-shadow: 0 0 4px #ff0;

	-webkit-transform: rotate(7.deg);
	    -ms-transform: rotate(7.deg);
	        transform: rotate(7.deg);

	-webkit-transition: all 0.3s ease;
	        transition: all 0.3s ease;

	background-image: -webkit-linear-gradient(bottom, #fff, #f00);
	background-image: linear-gradient(to top, #fff, #f00);

	background-image: -webkit-linear-gradient(bottom,  #fff,  #f00);
	background-image: linear-gradient(to top, #fff, #f00);

	background-image: -webkit-linear-gradient(top,  #fff,  #f00);
	background-image: linear-gradient(to bottom , #fff, #f00);
}
"""
