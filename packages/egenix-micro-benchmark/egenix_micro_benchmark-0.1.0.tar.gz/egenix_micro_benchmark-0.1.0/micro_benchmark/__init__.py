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
# Public API
from micro_benchmark.runtime import run # noqa
from micro_benchmark.decorators import configure # noqa

# Version
__version__ = '0.1.0'
