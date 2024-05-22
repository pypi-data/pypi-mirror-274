#!/usr/bin/env python3
"""
    examples - Simple examples of how to use the micro_benchmark package

    Written by Marc-Andre Lemburg.
    Copyright (c) 2024, eGenix.com Software GmbH; mailto:info@egenix.com
    License: Apache-2.0

"""

### Examples

# Example bench mark function:
#
# The two sections "# Init" and "# Bench" are required (together with the
# comments.  The two sections are used to build the actual micro benchmark
# functions.
#
# The Init section defines the variables to be used for the Bench section.
# The bench section is run multiple times (depends on the functions
# .iterations attribute, which defaults to 10).
#
def bench_match_int():

    # Init
    obj = 1

    # Bench
    match obj:
        case float() as float_value: # noqa
            pass
        case int() as int_value:
            pass
        case _:
            pass

    # Verify
    assert int_value == 1

###

if __name__ == '__main__':
    from micro_benchmark import runtime
    runner = runtime.run(globals())
