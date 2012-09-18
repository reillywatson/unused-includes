unused-includes
===============

Run through my C++ project and pull out unused #includes.  Requires Python and envoy.

Notes
=====

This isn't very sophisticated.  You probably want to use a real static analyzer instead.  Basically, it just goes through files as follows:

1. pull out #includes
2. strip filename out of include
3. Check to see if you reference the same string as that filename (for instance, if you include "SomeClass.h", see if SomeClass gets mentioned in your .cpp file)
4. Remove #includes that might not be used
5. make
6. If build fails, try subsets of this list of possibly unused includes

This works for the project I'm using it for, but in general this is a stupid way to do this, I just wanted to see if it would work at all.
