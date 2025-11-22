import sys
import matplotlib.pyplot as plt
import numpy as np
from manifold.core.io import ManifoldTensor

def diagnose_profile(filepath):
    print(f"DIAGNOSING: {filepath}")
    t = ManifoldTensor.load(filepath)
    
    # Grab a slice through the middle of the map
    row_idx = t.rows // 2
    
    # Get Raw Elevation and Roughness for that row
    elev_profile = t.elevation[row_idx, :]
    rough_profile = t.derived[3, row_idx, :]
    
    # Zoom in on a 100-pixel section (Small enough to see individual steps)
    start = 4000
    end = 4100
    zoom_elev = elev_profile[start:end]
    zoom_rough = rough_profile[start:end]
    
    # PLOT
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    # 1. Elevation Profile
    ax1.plot(zoom_elev, 'b.-', label='Elevation (m)')
    ax1.set_title(f"Elevation Cross-Section (Row {row_idx}, Cols {start}-{end})")
    ax1.set_ylabel("Height (Meters)")
    ax1.grid(True, alpha=0.3)
    
    # Check if values are integers
    is_integer = np.all(np.mod(zoom_elev, 1) == 0)
    if is_integer:
        ax1.text(0.02, 0.9, "WARNING: DATA IS INTEGER STEPPED!", transform=ax1.transAxes, color='red', fontsize=12, fontweight='bold')
    
    # 2. Roughness Profile
    ax2.plot(zoom_rough, 'r.-', label='Roughness')
    ax2.set_title("Roughness Response")
    ax2.set_ylabel("Roughness Value")
    ax2.grid(True, alpha=0.3)
    
    print(f"Data looks like integers? {is_integer}")
    print(f"Unique Z values in slice: {len(np.unique(zoom_elev))}")
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "data/processed/smokies.mft"
    diagnose_profile(path)