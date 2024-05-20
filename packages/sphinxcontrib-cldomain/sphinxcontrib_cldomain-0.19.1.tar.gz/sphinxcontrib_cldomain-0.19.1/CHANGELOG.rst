0.19.1 - 2024-05-19
-------------------
Minor Fixes
~~~~~~~~~~~

* Don't implicitly load a Package with the name of the System, if no
  packages are specified.
* Error if the symbol is not exported from the package
* Update the sphinx version dependency to 7.3.0
* Update metadata to include python 3.10

0.19.0 - 2024-04-28
-------------------
Features
~~~~~~~~

* allow declaration of packages separate from systems
* load missing package data on demand
* support using a custom lisp executable to run backend

Minor Fixes
~~~~~~~~~~~

* handle lambda lists like (foo bar . baz)
* quote all symbols so that log messages are easier to read
* to support windows better call script instead of relying on shebang
* support class specializers like (eql (find-class 'my-class))
* support eql specialisers that match non-symbol values
* rename specializer from eq to eql
* raise exceptions that have better descriptions
* return correct Sphinx extension metadata object when initialising
  plugin
* set correct default value for cl_packages config

Documentation
~~~~~~~~~~~~~

* improve configuration documentation

Tests
~~~~~

* add a test for the package json encoding
* improve coverage of encode-specializer

Cleanups
~~~~~~~~

* remove dependency on pants

0.18.1 - 2023-06-04
-------------------
Minor Fixes
~~~~~~~~~~~

* handle condition slot documentation strings
* rendering of slot's in pdf's

Documentation
~~~~~~~~~~~~~

* cleanup index page
* fix pdf and info links
* build latex after rendering

0.18.0 - 2023-03-04
-------------------
Features
~~~~~~~~

* add support for documenting CLOS object slots

Minor Fixes
~~~~~~~~~~~

* raise a runtime error if the package is missing
* remove nospecializers method option
* handle nil arguments correctly
* convert desc_sig_keyword to desc_clparameter
* add &body to potential lambda list keywords
* add missing sphinx dependency
* print the localised name of the object type
* add print-object methods to help with debugging
* add missing :name values for variables and classes
* cleanup conditional
* simplify xref logic
* handle classes with no slots
* cleanup formatting and fix tests

Documentation
~~~~~~~~~~~~~

* update documentation and restructure
* update makefile and doc building
* update theme to custom cldomain theme

Cleanups
~~~~~~~~

* cleanup licensing dates


0.17.1 - 2023-01-18
-------------------
Minor Fixes
~~~~~~~~~~~

* remove clear_doc method

0.17.0 - 2023-01-18
-------------------
Features
~~~~~~~~

* refactor object backend
* cleanup generic/method linking
* update the generic linking so it's less obtrusive
* setf expander support

Minor Fixes
~~~~~~~~~~~

* cleanup specializer handling

Documentation
~~~~~~~~~~~~~

* changelog had the wrong title headings

Build Tooling
~~~~~~~~~~~~~

* add example envrc

0.16.2 - 2023-01-08
-------------------

Minor Fixes
~~~~~~~~~~~

* add missing roswell file

0.16.1 - 2023-01-08
-------------------

Minor Fixes
~~~~~~~~~~~

* add back files missing from dist

0.16.0 - 2023-01-08
-------------------

Features
~~~~~~~~

* rename type to class

Minor Fixes
~~~~~~~~~~~

* fix method arguments in PDF output closes `#7
  <https://github.com/russell/sphinxcontrib-cldomain/issues/7>`_
* fix dictionary changed size during iteration
* rename type to class, in reality we are documenting classes, not
  types.
* bump pants to 2.14.0
* remove list_unused_symbols
* disable more warnings

Documentation
~~~~~~~~~~~~~

* add PDF and Info examples to documentation
* update changelog
* update bugtracker and documentation url
* fix sphinx url
* fix reference to pdf

Tests
~~~~~

* add tests for types, clos classes
* hookup lisp tests

Build Tooling
~~~~~~~~~~~~~

* migrate from pants to pyproject for building

Cleanups
~~~~~~~~

* modernise system definition

0.15.3 - 2022-07-24
-------------------
* assign *TRACE-OUTPUT* and *DEBUG-IO* to *ERROR-OUTPUT*

0.15.2 - 2022-07-24
-------------------
* fix don't decode bytes before writing them

0.15.1 - 2022-07-24
-------------------
* fix decode bytes before writing them

0.15 - 2022-07-23
-----------------
* stop qualifying lambda list symbols with a package
* fix display of method specializer links #16
* fix labelling of link back to generic

0.14 - 2022-07-10
-----------------
* convert to unix-opts, because i couldn't get clon to work
* strip packages from symbols if it's the current package, so
  CL-GIT::BODY would become BODY.
* add whitespace between method arguments so method ``(full-name
  (objectreference))`` will print as method ``(full-name (object
  reference))``
* symbols that a appear at the start of newlines are now correctly
  rendered, this might break CLISP, but will work in SBCL.  The bug
  was introduced by trying to support CLISP, but i think valid
  rendering trumps multiplatform support for now.

0.13 - 2015-09-06
-----------------
* updated com.dvlsoft.clon to net.didierverna.clon.

0.12 - 2015-02-24
-----------------
* fixed argument generation bug.

0.11 - 2014-12-30
-----------------
* support loading symbol information from multiple packages.

0.10 - 2014-06-12
-----------------
* added back parentheses to parameter lists.
* added type information to parameter list of methods.
* added links to other methods from a method docstring.
* fixed bug with macro documentation strings.
* added better keyword detection in documentation strings.
* fixed bug where symbols at the end of documentation
  strings were ignored.

0.9 - 2014-02-10
----------------
* fixed problem with version number generation.

0.8 - 2014-02-10
----------------
* fixed bug with lisps argument.
* removed dependency on swank.
* remove specializers symbols package if it's the current
  package.

0.7 - 2013-06-12
----------------
* started to make internals more modular.
* print specialisation for methods.
* add links to method specializers.
* added methods to index.

0.6 - 2013-04-22
----------------
* added more documentation.
* added better error handling when json fails to parse.
* methods can now pull documentation from their generic.

0.5 - 2013-04-20
----------------
* inherit environment when calling subprocesses.
* better handling of symbols in doc strings.

0.4 - 2013-04-19
----------------
* fixed some packaging bugs.
* made the data model more tolerant to missing symbols.
* fixed symbol resolving bug.
* added output of unused symbols.

0.3 - 2013-04-16
----------------
* cleaned up specializer output.
* fixed bug when rendering specializers that have the form :KEYWORD
  SYMBOL.
* updated documentation.
* split out package code from lisp program.

0.2 - 2013-04-14
----------------

* link between generics and specializers.
* ignore symbols in documentation if they are in the arg list.
* better Quicklisp support.
* handling of symbols that boarder on punctuation.

0.1 - UNRELEASED
----------------

* initial prototype
