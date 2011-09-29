# CSS Less-ish

This is a very very stripped down version of the functionality available via http://lesscss.org/

For debugging purposes (ie. FireBug etc) I wanted to use the functionality of .less, while still being able to trace back styles to their original source.

The solution for me is to have SublimeText process and compile the smarts for me - keeping the functionality within my editor and leaving the file on disk as valid css

Ultimately this plugin compiles and strips out the smarts at the "pre save" hook, saves the file, then restores the smarts instantly (it also works when opening a saved file)

## CSS VARIABLES

You can store variables within css comments using the @ symbol, then use them within your styles

	/* @link = "#FF0000" */
	a { color: @link; }

produces

	/* @link = "#FF0000" */
	a { color: #FF0000; }

## CSS NESTING

You can wrap styles within other blocks to append

	.header [
		h1 { color:blue }
		a { color:blue }
	]

produces

	/*.header [*/
		.header h1 { color:blue }
		.header a { color:blue }
	/*]*/