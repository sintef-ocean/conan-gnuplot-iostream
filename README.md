[![GCC Conan](https://github.com/sintef-ocean/conan-gnuplot-iostream/workflows/GCC%20Conan/badge.svg)](https://github.com/sintef-ocean/conan-gnuplot-iostream/actions?query=workflow%3A"GCC+Conan")
[![Clang Conan](https://github.com/sintef-ocean/conan-gnuplot-iostream/workflows/Clang%20Conan/badge.svg)](https://github.com/sintef-ocean/conan-gnuplot-iostream/actions?query=workflow%3A"Clang+Conan")
[![MSVC Conan](https://github.com/sintef-ocean/conan-gnuplot-iostream/workflows/MSVC%20Conan/badge.svg)](https://github.com/sintef-ocean/conan-gnuplot-iostream/actions?query=workflow%3A"MSVC+Conan")
[![Download](https://api.bintray.com/packages/sintef-ocean/conan/gnuplot-iostream%3Asintef/images/download.svg)](https://bintray.com/sintef-ocean/conan/gnuplot-iostream%3Asintef/_latestVersion)


[Conan.io](https://conan.io) recipe for [gnuplot-iostream](https://github.com/dstahlke/gnuplot-iostream).

The recipe generates library packages, which can be found at [Bintray](https://bintray.com/sintef-ocean/conan/gnuplot-iostream%3Asintef).
The package is usually consumed using the `conan install` command or a *conanfile.txt*.

## How to use this package

1. Add remote to conan's package [registry.txt](http://docs.conan.io/en/latest/reference/config_files/registry.txt.html):

   ```bash
   $ conan remote add sintef https://api.bintray.com/conan/sintef-ocean/conan
   $ conan remote add bincrafters https://api.bintray.com/conan/bincrafters/public-conan
   ```

2. Using *conanfile.txt* in your project with *cmake*

   Add a [*conanfile.txt*](http://docs.conan.io/en/latest/reference/conanfile_txt.html) to your project. This file describes dependencies and your configuration of choice, e.g.:

   ```
   [requires]
   gnuplot-iostream/[>=2020.06.20]@sintef/stable

   [options]

   [settings]
   cppstd=17

   [imports]
   licenses, * -> ./licenses @ folder=True

   [generators]
   cmake_paths
   cmake_find_package
   ```

   Insert into your *CMakeLists.txt* something like the following lines:
   ```cmake
   cmake_minimum_required(VERSION 3.13)
   project(TheProject CXX)

   include(${CMAKE_BINARY_DIR}/conan_paths.cmake)
   find_package(gnuplot-iostream MODULE REQUIRED)

   add_executable(the_executor code.cpp)
   target_link_libraries(the_executor gnuplot-iostream::gnuplot-iostream)
   ```
   Then, do
   ```bash
   $ mkdir build && cd build
   $ conan install .. -s build_type=<build_type>
   ```
   where `<build_type>` is e.g. `Debug` or `Release`.
   You can now continue with the usual dance with cmake commands for configuration and compilation. For details on how to use conan, please consult [Conan.io docs](http://docs.conan.io/en/latest/)

## Package options

Option | Default | Values
---|---|---
`with_boost` | `True` | `[True, False]`

## Known recipe issues

`gnuplot-iostream` requires c++17 and you need to specify this standard for targets that
use the header file.

It is possible to get a header only installation without explicit dependency on boost. In
that case you are responsible for linking the necessary requirements
yourself. Specifically, you need the following boost components: `filesystem`, `iostreams`
and `system`.
