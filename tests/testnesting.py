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
\t.header [
\t\th1 {}
\t\t.title {} /* Comment */
\t]

\t.header [
\t\th1, h2, h3 { text-decoration:underline; }
\t\tdl.the-item:nth-child(3n+1) > a {
\t\t\tborder:solid 2px green;
\t\t}
\t]
"""

    def result(self):
        return """
\t/*.header [*/
\t\t.header h1 {}
\t\t.header .title {} /* Comment */
\t/*]*/

\t/*.header [*/
\t\t.header h1, .header h2, .header h3 { text-decoration:underline; }
\t\t.header dl.the-item:nth-child(3n+1) > a {
\t\t\tborder:solid 2px green;
\t\t}
\t/*]*/
"""
