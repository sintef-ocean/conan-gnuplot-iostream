cmake_minimum_required(VERSION 3.11)

project(TestGnuplotIostream
  LANGUAGES CXX
  DESCRIPTION "Test the gnuplot-iostream package")

include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
conan_basic_setup()

set(CMAKE_SKIP_RPATH ON)

find_package(gnuplot-iostream MODULE REQUIRED)
enable_testing()

add_executable(gnuplot-example-1d gnuplot-example-1d.cpp)
target_link_libraries(gnuplot-example-1d
  gnuplot-iostream::gnuplot-iostream)
#target_compile_features(gnuplot-example-1d PRIVATE cxx_std_17)

add_test(NAME example-1d COMMAND gnuplot-example-1d)
