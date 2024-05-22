
# eGenix Micro Benchmark

**Easily write micro benchmarks in Python.**

*Please note*: This is still an alpha version of the software. Things are most likely going to change at a higher rate until we've reached a point when a stable release can be made.

## Abstract

This package provides a set of tools for easily writing micro benchmarks in Python.

It builds upon the [pyperf](https://pypi.org/project/pyperf/) package, which is an evolution of the older [pybench](https://github.com/python/cpython/tree/v3.6.15/Tools/pybench) tool. pybench was part of Python for a very long time (and was also authored by Marc-André Lemburg, just like this new package). pyperf, written by Victor Stinner, builds upon the pybench concepts, but comes with more modern ways of doing benchmarking and timing, with the aim of producing more stable results.

Since micro benchmarks will typically test language features which run at a nanosecond scale, it is necessary to repeat the test code several times in order to have the test case run long enough to stand out compared to the timing machinery around it.

This package offers a very elegant way to do this and also provides generic discovery functionality to make writing such benchmarks a breeze.

## Example

Here's an example micro benchmark module (examples/bench_example.py):

```python
#!/usr/bin/env python3
import micro_benchmark

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

# CLI interface
if __name__ == '__main__':
    micro_benchmark.run(globals())
```

## Concept

The *init* part is run to set up the variables for the main part, the *bench* part. This part is not measured.

The *bench* part is run inside a loop managed by pyperf lots of times to measure the performance. Since the for-loop used for this incurs some timing overhead as well, the *bench* part is repeated a certain number of times (this is called *iterations* in the context of this package).

The *verify* part is run after the bench part to check whether the bench part did in fact run correctly and as expected. This part is not measured.

## Running a benchmark

Invoking the benchmark is easy. Simply run it with Python:

```
python3 examples/bench_example.py
```

The benchmark will take all the command line arguments pyperf supports, in addition to these extra ones added by the egenix-micro-benchmarks package:

- `--mb-filter=<regexp>`
  Only run those benchmark functions which match the given regular expression. The matching is done as a substring match, so e.g. using `--mb-filter="match"` will match the function in the example module.

The output will look something like this:

```
.....................
bench_match_int: Mean +- std dev: 105 ns +- 10 ns
```

giving you the time it tool to run a single iteration of the bench part, together with an indication how reliable this reading is, by providing the standard deviation of the timings.

In some cases, pyperf may warn you about unstable results. Benchmarking typically works best on quiet machines which don't have anything much else to do.

# Public API

`micro_benchmark.run(namespace, prefix='bench_', filters=None)`

> Run all benchmark functions found in namespace.
>
> *namespace* can be an object with an '`.items()`' method (e.g. the
globals() dictionary) or a `.__dict__` attribute (e.g. a module,
package, class, etc.).
>
> *prefix* is the prefix name of benchmark functions to look for
(defaults to '`bench_`').
>
> *filters* may be given as a list of regular expression to limit the
number of functions to run.  The expressions are OR-joined. If the
parameter is not given, the command line argument `--mb-filter` is used.
If this is missing as well, no filtering takes place.

`micro_benchmark.configure(iterations=None, name=None)`

> Provide additiona configuration for a benchmark function.
>
> *iterations* can be set to override the default for this function
(which is 20)
>
> *name* can be given to provide a more verbose name for the function.
The name is used by pyperf when generating output and for recording the
results in the JSON results file. It defaults to the function's name.

# Development

## Preparing the venv

In order to prepare the virtual env needed for the package to run, edit the `Makefile` to your liking and then run:

```
make install-venv
source env.sh # for bash
source env.csh # for C-shell
make install-packages
```

(or use any other virtual env tool you like :-))

## Create a release

- Make sure you update the version number in micro_benchmark/__init__.py

- Create a distribution and upload to TestPyPI_
```
make create-dist
make test-upload
```
- Check release on TestPyPI and try downloading the package from there
  - Special attention should be paid to the contents of the .tar.gz file
  - This should contain all necessary files to build the package
- Publish to PyPI:
```
make prod-upload
```
- Send out release emails

## Roadmap

- [x] Turn into a package
- [x] Release as a PyPI package
- [ ] Add more documentation and convert to MkDocs
- [ ] Add a whole set of micro benchmarks (e.g. the ones from pybench)
  - May be better to do this as a separate package

# License

(c) Copyright 2024, eGenix.com Software, Skills and Services GmbH, Germany.
This software is licensed under the Apache License, Version 2.0.
Please see the LICENSE file for details.


# Contact

For inquiries related to the package, please write to info@egenix.com.
