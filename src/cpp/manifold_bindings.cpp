#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

namespace py = pybind11;

// Forward declaration of the C++ solver function defined in kesm_solver.cpp
// This function signature must match the implementation file exactly.
py::array_t<float> compute_stability_index_cpp(
    py::array_t<float> elevation_array, float gsd);


// Define the Python module structure.
// The name '_manifold_backend' must match the name in CMakeLists.txt.
PYBIND11_MODULE(_manifold_backend, m) {
    m.doc() = "PyBind11 interface for high-performance Manifold solvers.";

    // Expose the optimized KESM-Lite Laplacian solver function to Python
    m.def("compute_stability_index_cpp", &compute_stability_index_cpp,
        "Computes the discrete Laplacian stability index in optimized C++.");
}