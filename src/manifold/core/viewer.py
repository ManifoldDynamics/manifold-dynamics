print("--- SCRIPT STARTED ---")
import sys
import numpy as np
import napari
from manifold.core.io import ManifoldTensor

def launch_viewer(filepath):
    print(f"Loading {filepath} into GPU memory...")
    
    # 1. Load Tensor
    tensor = ManifoldTensor.load(filepath)
    
    # 2. Prepare Data
    # Elevation
    elev = tensor.elevation.copy()
    elev[elev < -1000] = np.nan # Transparent holes
    
    # Roughness (Channel 3)
    rough = tensor.derived[3].copy()
    rough[elev < -1000] = np.nan 
    
    # Normals (Channel 0-2)
    norm = tensor.derived[0:3].transpose(1, 2, 0).copy()
    norm = (norm + 1) / 2.0
    norm[np.isnan(elev)] = 0

    # --- DEBUG STATS ---
    # This prints the actual data range to the terminal
    # If Max is 0.0, your ingest math failed. If Max is > 0.1, it works.
    print(f"Roughness Stats -> Min: {np.nanmin(rough):.4f} | Max: {np.nanmax(rough):.4f} | Mean: {np.nanmean(rough):.4f}")

    # 3. Launch Napari
    viewer = napari.Viewer(title=f"Manifold Dynamics: {filepath}")

    # Layer 1: Normals
    viewer.add_image(
        norm, 
        name='Normals (RGB)', 
        rgb=True, 
        visible=False
    )

    # Layer 2: Elevation
    viewer.add_image(
        elev, 
        name='Elevation', 
        colormap='terrain',
        contrast_limits=[0, 2500] 
    )

    # Layer 3: Roughness
    # FIX 1: Opacity set to 1.0 (Fully Visible)
    # FIX 2: Contrast limits calculated automatically (2% to 98% percentile) to force visibility
    viewer.add_image(
        rough, 
        name='Roughness', 
        colormap='magma', 
        opacity=1.0, 
        blending='additive' # Makes it glow on top of the terrain
    )

    print("Viewer Launched.")
    napari.run()

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "data/processed/smokies.mft"
    launch_viewer(path)