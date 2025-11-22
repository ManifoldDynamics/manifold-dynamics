# Minimum version requirement (Resetting to stable standard)
cmake_minimum_required(VERSION 3.12) 
project(manifold_backend LANGUAGES CXX)

# Find Python3 and PyBind11
find_package(Python3 3.12 REQUIRED COMPONENTS Interpreter Development)
find_package(pybind11 CONFIG REQUIRED)

# Define the shared library that Python will call, specifying the source files
pybind11_add_module(_manifold_backend
    manifold_bindings.cpp
    kesm_solver.cpp
)

# Link necessary libraries
target_link_libraries(_manifold_backend PRIVATE Python3::Module)
target_include_directories(_manifold_backend PRIVATE ${Python3_INCLUDE_DIRS}
    ${CMAKE_CURRENT_SOURCE_DIR}
)