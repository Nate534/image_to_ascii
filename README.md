# Image to ASCII Art Converter

[![Hacktoberfest](https://img.shields.io/badge/Hacktoberfest-2024-orange.svg)](https://hacktoberfest.com/)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python application that converts images to ASCII art using advanced mathematical methods for symbol selection, including Principal Component Analysis (PCA) for intelligent character mapping.

## 🚀 Quick Start

### Installation

```bash
pip install Pillow numpy
```

### Basic Usage

```bash
python -m src.image_to_ascii.cli --input skull.jpeg --output skull_art.txt --width 80
```

### Example Output

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
```

## ✨ Features

- **Advanced Symbol Selection**: Uses Principal Component Analysis (PCA) for intelligent ASCII character mapping
- **Customizable Output**: Adjustable width and aspect ratio preservation
- **Modular Architecture**: Clean, extensible codebase perfect for contributions
- **Mathematical Foundation**: Implements sophisticated algorithms for optimal visual representation
- **File-Based Processing**: Supports various image formats through PIL

## 🎯 Hacktoberfest 2024

This project is participating in Hacktoberfest! We have **15 carefully crafted issues** ranging from beginner to advanced levels, each with detailed mathematical explanations and implementation guides.

**[📋 View All Issues](HACKTOBERFEST_ISSUES.md)**

### Issue Categories:
- 🟢 **Beginner**: Brightness mapping, contrast enhancement, edge detection
- 🟡 **Intermediate**: Dithering algorithms, frequency domain analysis, adaptive processing  
- 🔴 **Advanced**: Neural networks, wavelets, genetic algorithms, real-time video

## 🛠️ Development Setup

```bash
git clone https://github.com/yourusername/image-to-ascii.git
cd image-to-ascii
pip install -e .
pytest tests/
```

## 📖 Documentation

Detailed documentation is available in the `docs/` directory:
- [ASCII Generation Process](docs/ascii_generation.md)
- [Character Mapping Algorithms](docs/character_mapping.md)
- [CLI Usage Guide](docs/cli_usage.md)
- [Image Loading and Processing](docs/image_loading.md)
- [Output Formats and Saving](docs/output_saving.md)

## 🤝 Contributing

We welcome contributions of all skill levels! Whether you're fixing bugs, adding features, or improving documentation, your help is appreciated.

1. Check out our [Hacktoberfest Issues](HACKTOBERFEST_ISSUES.md) for contribution ideas
2. Read our [Contributing Guidelines](CONTRIBUTING.md)
3. Follow our [Code of Conduct](CODE_OF_CONDUCT.md)

## 📊 Algorithm Overview

The core algorithm uses **Principal Component Analysis** to match image blocks with ASCII characters:

1. **Image Preprocessing**: Convert to grayscale and resize
2. **Block Division**: Split image into character-sized blocks  
3. **Feature Extraction**: Compute PCA features for each block
4. **Character Matching**: Find ASCII character with closest PCA signature
5. **Output Generation**: Assemble final ASCII representation

## 🧮 Mathematical Foundation

- **PCA Feature Extraction**: `eigenvals, eigenvecs = np.linalg.eig(covariance_matrix)`
- **Distance Calculation**: Euclidean distance in eigenspace
- **Aspect Ratio Correction**: `height = int(width * aspect_ratio / 2)`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python, NumPy, and Pillow
- Mathematical concepts inspired by computer vision research
- Community-driven development through Hacktoberfest

---

**Ready to contribute?** Check out our [issue tracker](HACKTOBERFEST_ISSUES.md) and join the fun! 🎃