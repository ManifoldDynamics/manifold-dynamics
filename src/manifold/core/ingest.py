print("--- SCRIPT STARTED ---")
import sys
import os
import argparse
import numpy as np
import rasterio
from scipy.ndimage import uniform_filter, gaussian_filter, median_filter
from manifold.core.io import ManifoldTensor

# --- GEOMETRIC HEALING ---

def destripe_terrain(elevation):
    """
    Non-destructive method to remove tile stitching artifacts by aligning offsets.
    """
    print("    ...Running Robust Destriper (Median Method)...")
    healed = elevation.copy()
    
    # --- PASS 1: Vertical Stripes (Column Alignment) ---
    col_profile = np.nanmean(healed, axis=0)
    
    # High sigma (100) separates the mountain trend from the local grid jump
    ideal_profile = gaussian_filter(col_profile, sigma=100) 
    
    # The correction is the difference between the actual mean and the smooth trend
    correction = col_profile - ideal_profile
    healed -= correction[np.newaxis, :]
    
    # --- PASS 2: Horizontal Stripes (Row Alignment) ---
    row_profile = np.nanmean(healed, axis=1)
    ideal_row_profile = gaussian_filter(row_profile, sigma=100)
    row_correction = row_profile - ideal_row_profile
    healed -= row_correction[:, np.newaxis]
    
    return healed.astype(np.float32)

# --- SEMANTIC MATH ---

def calculate_tpi(elevation):
    """
    Calculates Topographic Position Index (TPI).
    Measures difference between center elevation and mean local elevation.
    """
    print("       - Calculating TPI...")
    # 15x15 pixel window is standard for regional context
    mean_local = uniform_filter(elevation, size=15) 
    tpi = elevation - mean_local
    return tpi.astype(np.float32)

def calculate_vrm(normals):
    """
    Calculates Vector Ruggedness Measure (VRM).
    VRM = 1 - magnitude of the mean normal vector.
    """
    print("       - Calculating VRM...")
    # Normals shape is (3, R, C). Transpose to (R, C, 3) for local operations
    n = normals.transpose(1, 2, 0)
    
    # Local Mean Vector over 3x3 window
    mean_nx = uniform_filter(n[:, :, 0], size=3)
    mean_ny = uniform_filter(n[:, :, 1], size=3)
    mean_nz = uniform_filter(n[:, :, 2], size=3)
    
    magnitude_mean = np.sqrt(mean_nx**2 + mean_ny**2 + mean_nz**2)
    vrm = 1.0 - magnitude_mean
    return vrm.astype(np.float32)

# --- CORE MATH ---

def compute_eigen_roughness(elevation, gsd, nodata_value):
    """
    Calculates Roughness using the Structure Tensor (PCA) method.
    """
    print("    ...Computing Structure Tensor (PCA)...")
    z = elevation.copy()
    if nodata_value is not None: z[z == nodata_value] = np.nan
    z[z < -10000] = np.nan

    rows, cols = z.shape
    def local_mean(arr):
        return uniform_filter(arr, size=3, mode='reflect')

    y, x = np.indices((rows, cols))
    x = x.astype(np.float32) * gsd
    y = y.astype(np.float32) * gsd

    mx, my, mz = local_mean(x), local_mean(y), local_mean(z)
    
    Czz = local_mean(z * z) - mz * mz
    Cxz = local_mean(x * z) - mx * mz
    Cyz = local_mean(y * z) - my * mz
    Cxx = local_mean(x * x) - mx * mx
    Cyy = local_mean(y * y) - my * my
    Cxy = local_mean(x * y) - mx * my

    cov_field = np.stack([
        np.stack([Cxx, Cxy, Cxz], axis=-1),
        np.stack([Cxy, Cyy, Cyz], axis=-1),
        np.stack([Cxz, Cyz, Czz], axis=-1)
    ], axis=-2).reshape(-1, 3, 3)
    
    mask = np.isnan(cov_field).any(axis=(1, 2))
    cov_field[mask] = np.eye(3)
    
    vals = np.linalg.eigvalsh(cov_field)
    lambda_3 = vals[:, 0]
    
    roughness = np.sqrt(np.abs(lambda_3)).reshape(rows, cols)
    roughness[mask.reshape(rows, cols)] = np.nan
    
    roughness = median_filter(roughness, size=3) # Post-Process Polish

    return roughness.astype(np.float32)

def calculate_normals(elevation, gsd, nodata_value):
    """
    Calculates surface normal vectors (Nx, Ny, Nz) using denoised gradients.
    """
    print(f"    ...Normalizing geometry")
    z = elevation.copy()
    if nodata_value is not None: z[z == nodata_value] = np.nan
    z[z < -10000] = np.nan

    dy, dx = np.gradient(z, gsd)
    
    # Denoise the gradients (Fixes jitter/artifacts)
    dx = gaussian_filter(dx, sigma=2.0)
    dy = gaussian_filter(dy, sigma=2.0)
    
    nx, ny, nz = -dx, dy, np.ones_like(z)
    
    mag = np.sqrt(nx**2 + ny**2 + nz**2)
    with np.errstate(invalid='ignore'):
        nx /= mag
        ny /= mag
        nz /= mag
    
    nx = np.nan_to_num(nx, nan=0.0)
    ny = np.nan_to_num(ny, nan=0.0)
    nz = np.nan_to_num(nz, nan=1.0)

    return np.stack([nx, ny, nz]).astype(np.float32)

# --- MAIN ASSEMBLY ---

def ingest_geotiff(input_path, output_path):
    print(f"[INGEST] Opening {input_path}...")
    
    with rasterio.open(input_path) as src:
        raw_elevation = src.read(1).astype(np.float32)
        transform = src.transform
        gsd = transform[0]
        origin_lon = transform[2]
        origin_lat = transform[5]
        rows, cols = raw_elevation.shape
        nodata = src.nodata
        print(f" -> Grid: {cols}x{rows} | GSD: {gsd:.2f}m")

    print(" -> Filling Voids for Processing...")
    if nodata is not None: voids = raw_elevation == nodata
    else: voids = raw_elevation < -10000
    
    global_med = np.nanmedian(raw_elevation[~voids])
    raw_elevation[voids] = global_med

    # 1. Non-Destructive Healing
    elevation = destripe_terrain(raw_elevation)

    tensor = ManifoldTensor(rows, cols, gsd, (origin_lat, origin_lon))
    tensor.elevation = elevation 
    
    print(" -> Computing Physics Channels...")
    
    # CORE CHANNELS
    normals = calculate_normals(elevation, gsd, nodata)
    roughness = compute_eigen_roughness(elevation, gsd, nodata)
    
    # SEMANTIC CHANNELS
    print("    - Calculating Semantic Features (TPI, VRM)...")
    tpi = calculate_tpi(elevation)
    vrm = calculate_vrm(normals)
    
    # --- ASSEMBLE TENSOR (FINAL 7-CHANNEL STRUCTURE) ---
    print(" -> Final Tensor Assembly...")
    tensor.derived[0:3] = normals     # CH 0-2 (Nx, Ny, Nz)
    tensor.derived[3] = roughness     # CH 3 (Roughness)
    tensor.derived[4] = tpi           # CH 4 (TPI)
    tensor.derived[5] = vrm           # CH 5 (VRM)
    
    print(f" -> Final Tensor Shape: Elevation + 6 Derived Channels.")
    print(f"[INGEST] Saving to {output_path}...")
    tensor.save(output_path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()
    if not os.path.exists(args.input):
        print(f"Error: Could not find {args.input}")
        return
    ingest_geotiff(args.input, args.output)

if __name__ == "__main__":
    main()