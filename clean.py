import os
import shutil

print("--- HUNTING FOR GHOST FILES ---")
found_any = False

# Walk through every single folder in the project
for root, dirs, files in os.walk("."):
    # We iterate over a copy of dirs so we can remove from the real list
    for d in list(dirs):
        if d.endswith(".egg-info") or d == "build" or d == "dist":
            full_path = os.path.join(root, d)
            print(f"TARGET ACQUIRED: {full_path}")
            found_any = True
            try:
                # The 'True' here ignores errors (like permissions)
                shutil.rmtree(full_path, ignore_errors=False)
                print(f" -> DESTROYED: {d}")
                # Remove from search list so we don't look inside deleted folders
                dirs.remove(d)
            except Exception as e:
                print(f" -> FAILED TO DELETE: {e}")

if not found_any:
    print("No artifacts found. The directory is clean.")
else:
    print("--- CLEANUP COMPLETE ---")