# Installation Guide - POF Engine

## 📋 Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **GPU**: OpenGL 3.3+ compatible graphics card

## 🚀 Quick Start (2 minutes)

### 1. Clone Repository
```bash
git clone https://github.com/platonpavluk16/POF_ENGINE.git
cd POF_ENGINE
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Engine
```bash
python main.py
```

✅ You should see the POF Engine window with a blue circle!

---

## 💻 Detailed Installation

### Windows

#### Prerequisites
1. Install Python 3.8+
   - Download from [python.org](https://www.python.org)
   - ✅ Check "Add Python to PATH" during installation

2. Install Git (optional but recommended)
   - Download from [git-scm.com](https://git-scm.com)

#### Installation Steps
```bash
# Open Command Prompt or PowerShell

# Clone repository
git clone https://github.com/platonpavluk16/POF_ENGINE.git
cd POF_ENGINE

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Run the engine
python main.py
```

---

### macOS

#### Prerequisites
1. Install Python 3.8+
   ```bash
   # Using Homebrew (recommended)
   brew install python3
   
   # Or download from python.org
   ```

2. Install Xcode Command Line Tools
   ```bash
   xcode-select --install
   ```

#### Installation Steps
```bash
# Clone repository
git clone https://github.com/platonpavluk16/POF_ENGINE.git
cd POF_ENGINE

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Run the engine
python main.py
```

---

### Linux (Ubuntu/Debian)

#### Prerequisites
```bash
# Update package manager
sudo apt update
sudo apt upgrade

# Install Python and development tools
sudo apt install python3.10 python3.10-venv python3-pip
sudo apt install libgl1-mesa-glx libglfw3
```

#### Installation Steps
```bash
# Clone repository
git clone https://github.com/platonpavluk16/POF_ENGINE.git
cd POF_ENGINE

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Run the engine
python main.py
```

---

## 📦 Alternative: Install as Package

### Development Install
```bash
pip install -e .
```

### Regular Install
```bash
pip install .
```

---

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'glfw'"

**Solution:**
```bash
pip install --upgrade glfw
```

### "ModuleNotFoundError: No module named 'OpenGL'"

**Solution:**
```bash
pip install PyOpenGL PyOpenGL_accelerate
```

### Windows: "RuntimeError: Could not find OpenGL context"

**Solution:**
- Update GPU drivers
- Ensure GPU supports OpenGL 3.3+
- Run as administrator

### macOS: "Library not loaded" error

**Solution:**
```bash
# Reinstall dependencies
pip uninstall glfw PyOpenGL -y
pip install glfw PyOpenGL
```

### Linux: GLFW errors

**Solution:**
```bash
# Install missing libraries
sudo apt install libglfw3 libglfw3-dev
sudo apt install libgl1-mesa-glx libx11-dev
```

---

## ✅ Verify Installation

Run this test script:
```python
# test_install.py
import glfw
from OpenGL.GL import *
import numpy as np

print("✓ glfw imported successfully")
print("✓ OpenGL imported successfully")
print("✓ numpy imported successfully")

if glfw.init():
    print("✓ GLFW initialized successfully")
    glfw.terminate()
else:
    print("✗ GLFW initialization failed")
```

Run with:
```bash
python test_install.py
```

---

## 🔄 Updating

### Update to Latest Version
```bash
cd POF_ENGINE
git pull origin main
pip install -r requirements.txt --upgrade
```

---

## 🐧 Virtual Environment Management

### Deactivate Environment
```bash
# Windows, macOS, Linux
deactivate
```

### Delete Environment (to start fresh)
```bash
# Windows
rmdir /s venv

# macOS/Linux
rm -rf venv
```

### Switch Python Version
```bash
# Specify Python version
python3.11 -m venv venv
```

---

## 🎯 Next Steps

After installation:

1. Read [README.md](README.md) for features overview
2. Check [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for architecture
3. Review [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
4. Run through example scenes
5. Create your first game object!

---

## 📚 Additional Resources

- **OpenGL Setup Issues**: [OpenGL Troubleshooting](https://www.khronos.org/opengl/)
- **Python Virtual Environments**: [Official Guide](https://docs.python.org/3/tutorial/venv.html)
- **GLFW Documentation**: [glfw.org](https://www.glfw.org/)

---

## ❓ Still Having Issues?

1. Check [Issues](https://github.com/platonpavluk16/POF_ENGINE/issues) on GitHub
2. Create a new issue with:
   - Your OS and Python version
   - Error message (full traceback)
   - Steps to reproduce
   - Setup environment details

---

Happy developing! 🎮✨
