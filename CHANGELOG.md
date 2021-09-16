# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Available types:

- `Added` for new features.
- `Changed` for changes in existing functionality.
- `Deprecated` for soon-to-be removed features.
- `Removed` for now removed features.
- `Fixed` for any bug fixes.
- `Security` in case of vulnerabilities.

## [Unreleased]

### Added
- Can add website links to assignemnt in TestCase classes


## [1.5.2]
### Fixed
- Change in pythons unittest made it so tip for StopIteration wasnät showing on python38-9.



## [1.5.1]
### Fixed
- Bug caused tags-wrapped functions to have incorrect metadata.


## [1.5.0]

### Added
- Added som common functions/classes can be imported directly from examiner.

### Fixed
- --tags will not properly skip tests if they don't match.



## [1.4.0] - 2021-05-20
### Changed
- Script no longer output results if no tests are found.
- --extra only runs extra assignments



## [1.3.0] - 2021-05-20
### Added
- New assert method assertOrder



## [1.2.0] - 2021-05-20
### Added
- Support for assertCountEqual



## [1.1.0] - 2021-05-18
### Changed
- Increased max len for test name and result in output.
- --trace flag now shows entire traceback

### Added
- Support for assertRaises



## [1.0.4] - 2021-05-04
### Added
-  Two new assert methods, assertModule and assertAttribute.


## [1.0.3] - 2021-04-30
### Added
- --trace option to traceback assertion errors

## [1.0.2] - 2021-04-21
### Changed
- Changed allowed naming for test classes and test functions
### Added
- assertNotIn method

## [1.0.1] - 2021-04-16
### Added
- CHANELOG to track changes.
- CircleCI build to push releases to dbwebb-se/python repo
