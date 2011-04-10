# -*- coding: utf-8 -*-

from cStringIO import StringIO
import logging
import os

from django.core.exceptions import ImproperlyConfigured
from djboss.commands import *
import jsmin as libjsmin

from djjsmin import utils


LOG = logging.getLogger('django.djjsmin')

@command
@argument('-d', '--dev-mode', action='store_true', default=None, dest='development_mode',
          help="Don't minify (just concatenate). Defaults to the value of DEBUG.")
@argument('-p', '--prod-mode', action='store_false', dest='development_mode',
          help="Minify, even when DEBUG is True.")
def jsmin(args):
    """Minify the configured JavaScript libraries."""
    
    if not hasattr(args.settings, 'JSMIN_INPUT'):
        raise ImproperlyConfigured("Must provide a JSMIN_INPUT setting")
    elif not hasattr(args.settings, 'JSMIN_OUTPUT'):
        raise ImproperlyConfigured("Must provide a JSMIN_OUTPUT setting")
    
    root = utils.get_root(args.settings)
    
    # Set up development mode. If nothing is specified, this will default to the
    # value of `settings.DEBUG`. The `-d` and `-p` options override this value.
    if args.development_mode is None:
        development_mode = args.settings.DEBUG
    else:
        development_mode = args.development_mode
    
    # `temp_files` have to be deleted after processing, whether minification was
    # successful or not.
    input_files, temp_files = utils.resolve_patterns(args.settings.JSMIN_INPUT, root)
    
    try:
        # Get an absolute output filename.
        output_file = utils.make_abs(args.settings.JSMIN_OUTPUT, root)
        
        if output_file in input_files:
            # This can happen if you output a '.js' file to the same directory
            # you're reading from. Remove it from the input files.
            input_files.remove(output_file)
        
        input_io = StringIO()
        try:
            # Populate the input StringIO.
            for filename in input_files:
                if filename in temp_files:
                    LOG.info("Reading %s" % p.basename(filename))
                else:
                    LOG.info("Reading %s" % p.relpath(filename))
                
                # The additional whitespace/comments will be filtered out by the
                # minifier later on, unless we are in development mode, in which
                # case we want the whitespace and comments.
                input_io.write("/* FILE: %s */" % filename + os.linesep)
                input_io.write(utils.read_from(filename))
                input_io.write(os.linesep * 2)
            input_io.seek(0)
            
            output_io = open(output_file, 'w')
            try:
                output_io.write(utils.get_prolog(args.settings, root))
                
                if development_mode:
                    LOG.info("Writing to %s" % p.relpath(output_file))
                    output_io.write(input_io.getvalue())
                else:
                    # Minify and write the output.
                    LOG.info("Minifying and writing to %s" % p.relpath(output_file))
                    libjsmin.JavascriptMinify(input_io, output_io).minify()
            finally:
                output_io.close() # Clean up.
        finally:
            input_io.close() # Clean up.
    
    finally:
        # Clean up.
        for temp_filename in temp_files:
            LOG.info("Cleaning temporary file %s" % p.basename(temp_filename))
            os.remove(temp_filename)
