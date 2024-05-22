#!/usr/bin/env python3
"""
    Example micro benchmark for the match statement

    Written by Marc-Andre Lemburg.
    Copyright (c) 2024, eGenix.com Software GmbH; mailto:info@egenix.com
    License: Apache-2.0
"""
import micro_benchmark

### Benchmarks

def bench_match_int():

    # Init
    obj = 1

    # Bench
    match obj:
        case float():
            type = 'float'
        case int():
            type = 'int'
        case _:
            pass

    # Verify
    assert type == 'int'

### CLI

if __name__ == '__main__':
    micro_benchmark.run(globals())
