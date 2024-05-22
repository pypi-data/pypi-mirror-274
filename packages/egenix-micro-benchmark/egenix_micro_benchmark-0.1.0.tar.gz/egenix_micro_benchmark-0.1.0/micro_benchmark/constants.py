#!/usr/bin/env python3
"""
    globals - configuration and templates for micro_benchmarks

    Written by Marc-Andre Lemburg.
    Copyright (c) 2024, eGenix.com Software GmbH; mailto:info@egenix.com
    License: Apache-2.0

"""
import re

# Output debug information ?
DEBUG = 0

# REs
DECORATOR_RE = re.compile('^\s*@\w+')
FUNCTION_DEF_RE = re.compile('^\s*def ')

# Default number of copies to put into the benchmark_code part of the bench mark
# function
DEFAULT_ITERATIONS = 20

# Code template used to build the benchmark functions
PERF_TEMPLATE = """\
def {fct_name}(iterations):
    loops = range(iterations)
    counter = pyperf.perf_counter
    t0 = counter()
{init_code}
    for _ in loops:
{benchmark_code}
    t1 = counter()
{verify_code}
    return t1 - t0
"""
