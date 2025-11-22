print("--- SCRIPT STARTED ---")
import sys
import matplotlib.pyplot as plt
import numpy as np
from manifold.core.io import ManifoldTensor

def view_manifold(filepath):
    print(f"--- LOADING {filepath} ---")
    tensor = ManifoldTensor.load(filepath)
    
    # Downsample (Take every 10th pixel)
    step = 10
    elev = tensor.elevation[::step, ::step]
    roughness = tensor.derived[3, ::step, ::step]

    # --- DEBUG: PRINT THE REAL VALUES ---
    # This tells us exactly what the "Garbage" value is
    print(f"Raw Data Stats:")
    print(f"   Min Value: {np.min(elev):.2f}") 
    print(f"   Max Value: {np.max(elev):.2f}")
    
    # --- THE HAMMER FIX ---
    # Instead of masking, we use 'vmin' and 'vmax' inside the plotter.
    # This forces the color scale to stick to reality (0m to 3000m).
    # We also replace the deep negative voids with 'NaN' so they show as white/transparent
    # rather than skewing the math.
    elev_plot = elev.copy()
    elev_plot[elev_plot < -100] = np.nan
    # -----------------------

    # Setup Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
    fig.canvas.manager.set_window_title('Manifold Dynamics - Tensor Viewer')
    
    # PLOT 1: Elevation
    # Force the range: 0m (Sea Level) to 2500m (Clingmans Dome is ~2025m)
    im1 = ax1.imshow(elev_plot, cmap='terrain', vmin=0, vmax=2500)
    ax1.set_title(f"Elevation (Fixed Scale)\nOrigin: {tensor.origin}")
    plt.colorbar(im1, ax=ax1, label='Meters')
    
    # PLOT 2: Roughness
    im2 = ax2.imshow(roughness, cmap='magma', vmin=0, vmax=0.5)
    ax2.set_title("Computed Surface Roughness")
    plt.colorbar(im2, ax=ax2, label='Variance (0.0 - 1.0)')
    
    plt.tight_layout()
    print("Rendering...")
    plt.show()

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "data/processed/smokies.mft"
    view_manifold(path)