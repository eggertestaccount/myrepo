<!-- title: Index -->

# `django-jsmin` Documentation

`django-jsmin` is a reusable application for [Django][] which simplifies and automates the process of [minifying][] your JavaScript libraries.

  [django]: http://www.djangoproject.com/
  [minifying]: http://www.crockford.com/javascript/jsmin.html


## Why Minify?

Minified JS is usually much smaller than regular JS. Comments and whitespace are very helpful when developing JavaScript code, but in production they just take up valuable network bandwidth. The effects of minifying code could range from faster page load times to smaller bandwidth bills from your hosting provider.

Minification can also obfuscate your code (making it difficult for third parties to copy), although effective obfuscation isn’t guaranteed, since it’s more of a side-effect of the minification process.


## Installation and Setup

*   Install the `django-jsmin` library:

        :::bash
        $ pip install django-jsmin # OR
        $ easy_install django-jsmin
    
    These commands will both install all the required dependencies.

*   Add `'djjsmin'` to your `INSTALLED_APPS` setting.

*   Add the necessary settings to your `settings.py` file:

        #!python
        JSMIN_ROOT = '/path/to/my/project/'
        
        # JSMIN_INPUT contains a list of all the input files and URLs.
        JSMIN_INPUT = [
            'http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.js',
            'media/js/jquery.*.js', # jQuery plugins
            'media/js/*.src.js', # project-specific libraries
        ]
        
        JSMIN_OUTPUT = 'media/js/project.min.js'
    
    More information on the available settings can be found [here](/settings).


## `DEBUG` mode

If `DEBUG` is set to `True` in your Django project when you run `django-jsmin`,
the JavaScript files will only be concatenated to the output file, not
compressed. This allows you to debug your code with meaningful line numbers
during development, and then use the fully-minified version in production. You
can force specific behaviour with options to the `djboss jsmin` command; see the
output of `djboss jsmin --help` for more information.


## Usage

`django-jsmin` uses [`django-boss`][djboss], a library/tool for writing and
running Django management commands. This will be installed automatically by
setuptools when you install `django-jsmin`.

  [djboss]: http://github.com/zacharyvoase/django-boss

Usage is relatively simple:

    :::bash
    $ djboss --log-level DEBUG jsmin
    Saving http://ajax.googleapis.com/.../jquery.js to a temporary file
    Saved http://ajax.googleapis.com/.../jquery.js to tmpN7MAsi
    Reading tmpN7MAsi
    Reading media/js/jquery.plugin1.js
    Reading media/js/jquery.plugin2.js
    Reading media/js/app-specific.lib.js
    Writing to media/js/minified.min.js
    Cleaning temporary file tmpN7MAsi

The JS file will be output to the filename given by the `JSMIN_OUTPUT` setting, in this case `media/js/minified.min.js`.


## License

`django-jsmin` is licensed under the following MIT/X11-style license:

> Copyright (c) 2009 Zachary Voase
> 
> Permission is hereby granted, free of charge, to any person
> obtaining a copy of this software and associated documentation
> files (the "Software"), to deal in the Software without
> restriction, including without limitation the rights to use,
> copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the
> Software is furnished to do so, subject to the following
> conditions:
> 
> The above copyright notice and this permission notice shall be
> included in all copies or substantial portions of the Software.
> 
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
> EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
> OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
> NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
> HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
> WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
> FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
> OTHER DEALINGS IN THE SOFTWARE.
