## CSS Less(ish)

This is a [SublimeText 2](http://www.sublimetext.com/2) plugin that facilitates a very very stripped down version of the functionality in LESS csss. ([http://lesscss.org](http://lesscss.org) on [github](https://github.com/cloudhead/less.js) too)

I wanted to implement a few clever ideas in LESS, while being able to trace back styles to their original source file and line number for debugging purposes. (eg. FireBug etc)

The solution for me was to have SublimeText handle the css smarts for me in the editor while leaving the file on disk as valid css.  I wanted to be able to put @link="#FF0000" within my css comments then be able to type @link anywhere within my css and have SublimeText "pop in the right value" just before the file saved to disk. My IDE would have css smarts, not the browser or javascript.

Ultimately this plugin compiles and applies the css smarts at the SublimeText "pre save" hook, saves the file then restores the original view (it also works when opening a saved file). Indeed it's not perfection, but I find it incredibly useful.

### CSS Variables

You can store variables within css comments using the "@" symbol, then use them within your styles as so...

    /* @link = "#FF0000" */  
    a { color: @link; }`

produces

    /* @link = "#FF0000" */
    a { color: #FF0000; }

### CSS Nesting

You can nest styles within other blocks to append that selector to all children.

    .header [
        h1 { color:blue }
        a { color:blue }
    ]

produces

    .header h1 { color:blue }
    .header a { color:blue }

## Comments

This solution won't break if opened within other IDEs. Doing so will reveal that the biggest trick is that the "css smarts" are serialized (so to speak) within a single line comment at the bottom of the file.  It's quite small and out of the way.  

Ultimately if you had two @variables in the css each with the same value, once saved and compiled down there was no way to know which variable was which anymore.  The solution was to store these variable mappings somewhere in the file.

As I said earlier it's not perfection, but it does work.