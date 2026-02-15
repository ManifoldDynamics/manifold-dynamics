import numpy as np
from scipy.ndimage import laplace
from manifold.core.io import ManifoldTensor
import sys
import argparse

class KESM_Lite:
    def __init__(self, tensor):
        self.tensor = tensor
        self.elevation = tensor.elevation
        self.gsd = tensor.gsd

    def compute_stability_index(self):
        """
        Implements Whitepaper Eq 7: Discrete Laplacian Proxy.
        Calculates the local curvature (2nd derivative) of the terrain to find sinks/peaks.
        """
        print("[KESM] Calculating Thermodynamic Stability (Laplacian)...")
        
        # --- FIX: Sanitize input data before math (Prevents Overflow) ---
        elev_safe = self.elevation.copy()
        # Replace extreme negative values (NoData) with NaN to stop overflow
        elev_safe[elev_safe < -1000] = np.nan
        # -----------------------------------------------------------------

        # Calculate Laplacian (Curvature)
        curvature = laplace(elev_safe)
        
        # Scale by grid size squared
        stability_index = curvature / (self.gsd ** 2)
        
        # Fill NaNs created by the laplace filter (usually borders) with 0
        stability_index = np.nan_to_num(stability_index, nan=0.0)
        
        return stability_index.astype(np.float32)

    def classify_terrain(self, stability_index, tau_pos, tau_neg):
        """
        Implements Whitepaper Eq 8: Stability Classification.
        NOTE: Thresholds (tau_pos/tau_neg) are passed for tuning.
        """
        print("[KESM] Classifying Terrain Types...")
        
        classification = np.zeros_like(stability_index, dtype=np.int8)
        
        # Class 1: Frost Hollow (Sink)
        classification[stability_index > tau_pos] = 1
        
        # Class -1: Exposed Peak (Source)
        classification[stability_index < tau_neg] = -1 
        
        return classification

def main():
    parser = argparse.ArgumentParser(description="KESM-Lite: Cold Air Drainage Analysis")
    parser.add_argument("input", nargs='?', default="data/processed/smokies.mft", help="Input MFT file path")
    args = parser.parse_args()

    path = args.input
    print(f"Loading {path}...")
    try:
        tensor = ManifoldTensor.load(path)
    except FileNotFoundError:
        print(f"Error: MFT file not found at {path}. Did you run ingest.py?")
        sys.exit(1)
    
    # Run Physics
    solver = KESM_Lite(tensor)
    stability = solver.compute_stability_index()
    
    # --- FINAL TUNING: WIDENED THRESHOLD (tau = 0.1) ---
    TAU = 0.1 
    classification = solver.classify_terrain(stability, tau_pos=TAU, tau_neg=-TAU)
    
    # --- VISUALIZATION ---
    try:
        import napari
        viewer = napari.Viewer(title="KESM-Lite: Cold Air Drainage Analysis")

        # Layer 1: Terrain
        viewer.add_image(tensor.elevation, name="Terrain", colormap="terrain")

        # Layer 2: Physics (The Flux Potential Heatmap)
        viewer.add_image(
            stability,
            name="Flux Potential (Laplacian)",
            colormap="coolwarm",
            opacity=0.6,
            contrast_limits=[-TAU, TAU]
        )

        # Layer 3: Classification (The discrete Blue Sinks / Red Peaks)
        labels_layer = viewer.add_labels(
            classification,
            name="Classification",
            opacity=0.5
        )

        # Set the colors explicitly
        labels_layer.color = {1: 'blue', -1: 'red', 0: 'transparent'}

        print("Running Viewer. Check the Blue Areas (Frost Hollows) and Red Areas (Peaks).")
        napari.run()
    except ImportError:
        print("Napari not installed or display not available. Visualization skipped.")
    except Exception as e:
        print(f"Could not launch viewer: {e}")

if __name__ == "__main__":
    main()
