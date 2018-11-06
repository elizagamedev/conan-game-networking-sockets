cmake_minimum_required(VERSION 2.8.12)
project(cmake_wrapper)

include(conanbuildinfo.cmake)
conan_basic_setup()

if(UNIX)
  add_compile_options("-msse2")
endif()

add_subdirectory("source_subfolder")
