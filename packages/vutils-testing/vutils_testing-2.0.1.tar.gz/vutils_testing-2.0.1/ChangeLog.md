# Change Log

## 2.0.1

* Minor code cleanup

## 2.0.0

* Remove obsoleted classes/functions (`vutils.testing.utils`):
  * `TypingPatcher`
  * `ClassLikeSymbol`
  * `cover_typing`

## 1.0.3

* Disable `pylint` `no-member` check
* Constraint `requests` to safe version

## 1.0.2

* Fix doc strings, slim imports

## 1.0.1

* Remove unused `pytest-order` from `tox.ini`

## 1.0.0

* Move the development status to production/stable
* Code cleanup

## 0.6.2

* Fix `safety` issues

## 0.6.1

* Fix `flake8` issues

## 0.6.0

* New class `ClassLikeSymbol`

## 0.5.3

* Fix PEP 585 issue
* Remove deprecated `pylint` warnings from `pyproject.toml`
* Run tests with `cover_typing` as last

## 0.5.2

* Fixed typo in class name in `README.md`
* Switch to Python 3.10+ typing notation
* Drop Python 3.6, add Python 3.10

## 0.5.1

* Fixed key-value arguments loss when `PatchSpec` instance is called more than
  once

## 0.5.0

* New class `LazyInstance`

## 0.4.0

* New class `AssertRaises`

## 0.3.0

* `make_mock` now passes its arguments to `unittest.mock.Mock`
* New method `TestCase.assert_not_called`

## 0.2.0

* Added functions
  * `cover_typing`
  * `make_callable`
  * `make_mock`
  * `make_type`
* Added classes
  * `PatcherFactory`

## 0.1.0

* Initial development version
