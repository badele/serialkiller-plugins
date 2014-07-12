#!/usr/bin/env python
# -*- coding: utf-8 -*-

__authors__ = 'Bruno Adelé <bruno@adele.im>'
__copyright__ = 'Copyright (C) 2013 Bruno Adelé'
__description__ = """A plugins for serialkiller project"""
__license__ = 'GPL'
__version__ = '0.0.1'


import sys
import argparse
import importlib

def parse_arguments(cmdline=""):
    """Parse the arguments"""

    parser = argparse.ArgumentParser(
        description=__description__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-a', '--action',
        action='store',
        dest='action',
        default='check',
        help='Action'
    )

    parser.add_argument(
        '-p', '--plugin',
        action='store',
        dest='plugin',
        help='Python plugin location'
    )

    parser.add_argument(
    '-v', '--values',
    action='store',
    dest='value',
    nargs='*',
    default=None,
    help='Params values'
    )

    parser.add_argument(
        '-f', '--format',
        action='store',
        dest='format',
        default='key',
        choices=[
            'key',
            'csv',
            'json',
        ],
        help='format'
    )



    a = parser.parse_args(cmdline)
    return a


def requirePlugin(args):
    if not args.plugin:
        print("Please select plugin")
        sys.exit(1)

    if not args.plugin.startswith('skplugins.'):
        print("Please select a plugin module")
        sys.exit(1)

def extractParams(args):
    """Extract params values"""

    if not args.value:
        return dict()

    params = {}
    for values in args.value:
        k, v = values.split('=')
        params[k] = v

    return params


def check(args):
    requirePlugin(args)
    plugin = loadPlugin(args)
    show(plugin,args.format)

def loadPlugin(args):
    """Load plugin"""
    lastdot = args.plugin.rfind(".")  + 1
    modulename = args.plugin
    classname = args.plugin[lastdot:]
    params = extractParams(args)


    module = importlib.import_module(modulename)
    moduleClass = getattr(module, classname)
    return moduleClass(**params)

def show(plugin, format):
    if format == 'key':
        for k,v in iter(sorted(plugin.results.iteritems())):
            print "%s=%s" % (k,v)

        for k,v in iter(sorted(plugin.params.iteritems())):
            print "param_%s=%s" % (k,v)


    if format == 'csv':
        i = 0
        header = ''
        results = ''
        for k,v in iter(sorted(plugin.results.iteritems())):
            if i > 0:
                header += ', '
                results += ', '
            i += 1
            header += k
            results += str(v)
        print header
        print results

    if format == 'json':
        # No need JSON class
        #print json.dumps(values, sort_keys=True, indent=4, separators=(',', ': '))

        # Header
        print "{"

        # Params
        print '    "result": {'
        i = 0
        for k,v in iter(sorted(plugin.results.iteritems())):
            if i < len(plugin.results) - 1:
                print '        "%s": %s,' % (k,v)
            else:
                print '        "%s": %s' % (k,v)
            i += 1
        print '    },'

        # Params
        print '    "params": {'
        i = 0
        for k,v in iter(sorted(plugin.params.iteritems())):
            if i < len(plugin.params) - 1:
                print '        "%s": %s,' % (k,v)
            else:
                print '        "%s": %s' % (k,v)
            i += 1
        print '    }'
        print "}"

def main():
    # Parse arguments
    args = parse_arguments(sys.argv[1:])  # pragma: no cover

    if args.plugin is not None:
        check(args)


if __name__ == '__main__':
    main()  # pragma: no cover
