#!/usr/bin/env python3
"""
    code - Generate benchmarking code

    Written by Marc-Andre Lemburg.
    Copyright (c) 2024, eGenix.com Software GmbH; mailto:info@egenix.com
    License: Apache-2.0

"""
import inspect
import textwrap
import pyperf
from micro_benchmark import constants

### Globals

# Output debug information ?
_debug = constants.DEBUG

### Tools

def benchmark_code(fct,
                   iterations=constants.DEFAULT_ITERATIONS,
                   fct_name=None):

    if fct_name is None:
        fct_name = fct.__name__
    if _debug:
        print (f'generating benchmark code for {fct}')
    (lines, start_lineno) = inspect.getsourcelines(fct)
    if _debug:
        print (f'inspect code lines: {lines}')

    # Remove decorators and def
    while constants.DECORATOR_RE.match(lines[0]) is not None:
        del lines[0]
    if constants.FUNCTION_DEF_RE.match(lines[0]) is not None:
        del lines[0]
    else:
        raise ValueError(f'Function does not start with "def": {fct}')

    # Remove empty lines
    lines = [line
             for line in lines
             if line.strip()]

    # Dedent code
    code = ''.join(lines)
    lines = textwrap.dedent(code).splitlines(keepends=True)
    if _debug:
        print (f'code lines: {lines}')

    # Find init, bench and verify sections
    init = []
    bench = []
    verify = []
    junk = []
    add_to = junk
    for line in lines:
        if line.startswith('# Init'):
            add_to = init
            continue
        elif line.startswith('# Bench'):
            add_to = bench
            continue
        elif line.startswith('# Verify'):
            add_to = verify
            continue
        add_to.append(line)
    assert len(junk) == 0, f'found extra code: {junk}'
    init_code = ''.join((
        f'    {line}' for line in init))
    benchmark_code = ''.join((
        f'        {line}' for line in bench * iterations))
    verify_code = ''.join((
        f'    {line}' for line in verify))

    # Build benchmark function
    code = constants.PERF_TEMPLATE.format(
        fct_name=fct.__name__,
        init_code=init_code.rstrip(),
        benchmark_code=benchmark_code.rstrip(),
        verify_code=verify_code.rstrip(),
        )

    return fct_name, code

def benchmark_function(fct,
                       iterations=constants.DEFAULT_ITERATIONS,
                       fct_name=None,
                       globals=None):

    # Generate code
    fct_name, code = benchmark_code(fct, iterations=iterations, fct_name=fct_name)

    # Prepare the globals namespace to run in
    if globals is None:
        globals = {}
    if 'pyperf' not in globals:
        # make sure pyperf is available, since the generated benchmark
        # code needs this
        globals['pyperf'] = pyperf

    # Note: pyperf uses worker processes which need to rerun the code
    # generation upon startup
    bench_fct = compile(code, '<generated>', 'exec')
    exec(bench_fct, globals, globals)
    if _debug:
        print ('Built and defined global function:')
        print (code)
        print ()
    return globals[fct_name]

###

if __name__ == '__main__':
    from micro_benchmark import examples
    benchmark = benchmark_function(examples.bench_match_int)
    benchmark(10)
