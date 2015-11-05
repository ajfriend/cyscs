# scs_python
[![Build Status](https://travis-ci.org/ajfriend/scs_python.svg?branch=master)](https://travis-ci.org/ajfriend/scs_python)

A Python interface, written in Cython, for [SCS](https://github.com/cvxgrp/scs), a numerical optimization package for solving convex cone problems.

## Usage
```
import scs
sol = scs(data, cone, **options)
```