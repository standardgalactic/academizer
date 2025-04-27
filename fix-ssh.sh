# Make directory for trusted keys if it doesn't exist
sudo mkdir -p /etc/apt/keyrings

# Download the key
curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/3bf863cc.pub | \
  sudo gpg --dearmor -o /etc/apt/keyrings/nvidia.gpg

# Update the NVIDIA repo source (if needed) to use the keyring
# This is just an example — adjust to match your actual .list file path:
echo "deb [signed-by=/etc/apt/keyrings/nvidia.gpg] https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64 /" | \
  sudo tee /etc/apt/sources.list.d/cuda-wsl.list > /dev/null

# Update packages
sudo apt update

