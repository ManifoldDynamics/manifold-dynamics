import struct
import numpy as np
import os

class ManifoldTensor:
    """
    Manifold Tensor (.mft) Handler.
    v1.1 Update: All channels standardized to Float32 for compatibility.
    """
    MAGIC = b'MFT1'
    HEADER_FMT = '<4sIIIIIIddd44x'
    HEADER_SIZE = 96 

    def __init__(self, rows=1024, cols=1024, gsd=10.0, origin=(0.0, 0.0)):
        self.rows = rows
        self.cols = cols
        self.gsd = gsd
        self.origin = origin 
        
        # CHANNEL 0: Elevation (Float32)
        self.elevation = np.zeros((rows, cols), dtype=np.float32)
        
        # CHANNELS 1-6: Derived Metrics (Float32)
        self.derived = np.zeros((6, rows, cols), dtype=np.float32)

    def save(self, filepath):
        """Writes the binary .mft file to disk."""
        print(f"[IO] Saving {filepath}...")
        with open(filepath, 'wb') as f:
            # 1. Pack Header
            header = struct.pack(
                self.HEADER_FMT,
                self.MAGIC,         # Magic Bytes
                1,                  # Version
                self.rows,          # Rows
                self.cols,          # Cols
                7,                  # Total Channels
                0,                  # Compression
                0,                  # Biome ID
                self.gsd,           # GSD
                self.origin[0],     # Lat
                self.origin[1]      # Lon
            )
            f.write(header)
            
            # 2. Write Elevation (Float32)
            f.write(self.elevation.tobytes())
            
            # 3. Write Derived (Float32)
            f.write(self.derived.tobytes())
            
        size_mb = os.path.getsize(filepath) / (1024 * 1024)
        print(f"[IO] Success. Wrote {size_mb:.2f} MB.")
            
    @classmethod
    def load(cls, filepath):
        """Reads a binary .mft file from disk."""
        with open(filepath, 'rb') as f:
            # 1. Read Header
            data = struct.unpack(cls.HEADER_FMT, f.read(cls.HEADER_SIZE))
            if data[0] != cls.MAGIC: raise ValueError("Invalid MFT file")
            
            obj = cls(rows=data[2], cols=data[3], gsd=data[7], origin=(data[8], data[9]))
            
            # 2. Read Elevation (Float32)
            bytes_elev = obj.rows * obj.cols * 4
            obj.elevation = np.frombuffer(f.read(bytes_elev), dtype=np.float32).reshape(obj.rows, obj.cols)
            
            # 3. Read Derived (Float32)
            bytes_derived = obj.rows * obj.cols * 4 * 6
            obj.derived = np.frombuffer(f.read(bytes_derived), dtype=np.float32).reshape(6, obj.rows, obj.cols)
            
            return obj