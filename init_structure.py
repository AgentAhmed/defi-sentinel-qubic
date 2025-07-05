import os

folders = [
    "agents",
    "contracts",
    "mcp",
    "frontend",
    "scripts",
    "test"
]

base_path = "defi-sentinel-qubic"

os.makedirs(base_path, exist_ok=True)

for folder in folders:
    path = os.path.join(base_path, folder)
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, ".keep"), "w") as f:
        f.write("")  # Helps Git keep empty folders

# Create empty files
open(os.path.join(base_path, "README.md"), "a").close()
open(os.path.join(base_path, "requirements.txt"), "a").close()
open(os.path.join(base_path, ".gitignore"), "a").close()

print("✅ Project structure created successfully.")
