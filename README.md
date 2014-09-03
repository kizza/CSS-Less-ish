# CSS Less(ish)

A [Sublime Text 2 & 3](http://www.sublimetext.com) plugin that implements a stripped down version of the functionality in css preprocessors (such as [LESS](http://lesscss.org)) so that you can use css variables and nesting without any effort.

![demo](http://imgur.com/03V7JGy.gif)

### CSS Variables

Store variables within comments using the "@" symbol, then use them anywhere within your css.

    /* @link = #6699CC */  
    a { color: @link; }

produces

    a { color: #6699CC; }

### CSS Nesting

Nest styles within other blocks to append that selector to all children.

    header [
        h1 { color:blue }
        a { color:blue }
    ]

produces

    header h1 { color:blue }
    header a { color:blue }

### CSS Colours

Use colour functions when declaring css variables including `lighten`, `darken`, `saturate`, and `desaturate`. You can pass existing variables as arguments too.

    /* 
    @base-colour = #336699
    @link = lighten(@base-colour, 20%) 
    */  
    a { color: @link; }

produces

    a { color: #3d7ab7; }

### CSS Maths

You can add and multiply numeric variables too (works with px, em or %)

    /* 
    @padding = 1em
    @width = 10em + 2 * @padding
    */  
    div { width: @width; }

produces

    div { width: 12em; }

### How does it work?

The plugin doesn't require any third party libraries or tools to be installed - in fact it's not really a css preprocessor at all.

When you save a css file using the features above the plugin instantly compiles down the output "pre save", writes it to disk, then restores your original css (all without you seeing it).

### Why?

CSS proprocessors are wonderfully powerful, but I wanted to be able to use the essential functionality they provide simply and without any effort.  The other advantage is that when debugging, your css styles are traced back to the original source document (since your css smarts comes from the file itself rather than being compiled into a separate file)

### Read More

You can [read more on the wiki](https://github.com/kizza/CSS-Less-ish/wiki).
