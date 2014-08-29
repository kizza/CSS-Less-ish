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

### Read More

You can [read more on the wiki](https://github.com/kizza/CSS-Less-ish/wiki).
