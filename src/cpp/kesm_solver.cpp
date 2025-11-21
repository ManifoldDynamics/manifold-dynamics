#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <stdexcept>
#include <algorithm>

namespace py = pybind11;

// Define the function that was declared in manifold_bindings.cpp
// This function replaces the scipy.ndimage.laplace(elevation) call.
py::array_t<float> compute_stability_index_cpp(
    py::array_t<float> elevation_array, float gsd)
{
    // Basic input validation
    if (elevation_array.ndim() != 2)
        throw std::runtime_error("Input elevation must be a 2D NumPy array.");

    // Access raw data pointers and shapes
    auto buf = elevation_array.request();
    const float* elev_data = static_cast<const float*>(buf.ptr);
    size_t rows = buf.shape[0];
    size_t cols = buf.shape[1];
    
    // Create the output array of the same size
    py::array_t<float> output_array = py::array_t<float>({rows, cols});
    auto output_buf = output_array.request();
    float* output_data = static_cast<float*>(output_buf.ptr);

    // Pre-calculate scaling factor
    float gsd_sq = gsd * gsd;

    // Zero-initialize the entire output array
    std::fill(output_data, output_data + rows * cols, 0.0f);
    
    // Core Loop: Apply 5-point stencil (Laplacian) to the interior pixels
    // We skip the 1-pixel border for speed and simplicity.
    for (size_t i = 1; i < rows - 1; ++i) {
        for (size_t j = 1; j < cols - 1; ++j) {
            // Index calculation: row * cols + col
            size_t idx = i * cols + j;

            // Calculate indices of neighbors
            size_t idx_up = (i - 1) * cols + j;
            size_t idx_down = (i + 1) * cols + j;
            size_t idx_left = i * cols + (j - 1);
            size_t idx_right = i * cols + (j + 1);

            // Laplacian: E(i+1) + E(i-1) + E(i,j+1) + E(i,j-1) - 4 * E(i, j)
            float laplacian = elev_data[idx_up] + elev_data[idx_down] +
                              elev_data[idx_left] + elev_data[idx_right] -
                              4.0f * elev_data[idx];
                              
            // Apply scale factor (for physical units)
            output_data[idx] = laplacian / gsd_sq;
        }
    }

    return output_array;
}