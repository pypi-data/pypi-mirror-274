#!/usr/bin/env python3
"""
    micro_benchmark - User friendly way to run micro benchmarks

    Use: Simply call script with -h as argument to see all available pyperf
    options.

    Example: See the Examples section below or the bench_match.py script for
    an example how to define micro- benchmarks.  Each such script will
    provide the same interface as this one when using the run() function.

    Written by Marc-Andre Lemburg.
    Copyright (c) 2024, eGenix.com Software GmbH; mailto:info@egenix.com
    License: Apache-2.0

"""
import re
import pyperf
from micro_benchmark import constants, code

### Globals

# Output debug information ?
_debug = constants.DEBUG

###

def run_benchmark(runner, fct):

    if hasattr(fct, 'iterations'):
        iterations = fct.iterations
    else:
        iterations = constants.DEFAULT_ITERATIONS
    if hasattr(fct, 'name'):
        benchmark_name = fct.name
    else:
        benchmark_name = fct.__name__
    bench_fct = code.benchmark_function(fct, iterations=iterations)
    if _debug:
        print (bench_fct)
    runner.bench_time_func(benchmark_name, bench_fct, inner_loops=iterations)
    return runner

def worker_add_cmdline_args(cmd, args):

    # Make sure our custom args are added to workers as well
    if args.mb_filter:
        cmd.extend(('--mb-filter', *args.mb_filter))
    if _debug:
        print (f'worker cmd: {cmd}')

def create_runner():

    # Create pyperf Runner instance
    runner = pyperf.Runner(
        add_cmdline_args=worker_add_cmdline_args,
    )

    # Add extra parameters for our own use
    runner.argparser.add_argument(
        '--mb-filter',
        help='filter micro benchmark function (regexp)',
        nargs='*',
        type=str)

    # Parse command line
    runner.parse_args()

    return runner

def run(namespace, prefix='bench_', filters=None):

    """ Run all benchmark functions found in namespace.

        namespace can be a dictionary or any other object with a
        .__dict__ attribute, e.g. a module, class, etc.

        prefix is the prefix name of benchmark functions to look for
        (defaults to 'bench_').

        filters may be given as a list of regular expression to limit
        the number of functions to run.  The expressions are OR-joined.
        If the parameter is not given, the command line argument
        --mb-filter is used. If this is missing as well, no filtering
        takes place.

    """
    # Create runner (early, since this provides the CLI interface)
    runner = create_runner()

    # Check command line filters
    if filters is None:
        filters = runner.args.mb_filter
        if _debug:
            print (f'filters: {filters}')

    # Prepare filter
    if filters:
        re_filter = re.compile('|'.join(filters)).search
    else:
        re_filter = lambda x: True

    # Find all bench_* functions in namespace
    if hasattr(namespace, 'items'):
        namespace_items = namespace.items()
    elif hasattr(namespace, '__dict__'):
        namespace_items = namespace.__dict__.items()
    else:
        raise TypeError(
            f'namespace must provide an .items() method or '
            f'have a .__dict__ attribute, found a {type(namespace)}')
    benchmarks = []
    for key, value in namespace_items:
        if key.startswith(prefix) and callable(value):
            if re_filter(key) is None:
                if _debug:
                    print (f'filtering out {key}')
                continue
            benchmarks.append(value)

    # Use runner to run all found benchmark functions
    for bench_fct in benchmarks:
        run_benchmark(runner, bench_fct)
    return runner

###

if __name__ == '__main__':
    from micro_benchmark import examples
    runner = run(examples)
