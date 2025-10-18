# Contributing to Image to ASCII Art Converter

Welcome to our open source project! We're excited to have you contribute. This guide will help you get started, whether you're a first-time contributor or an experienced developer.

## 🎯 Hacktoberfest Contributors

This project participates in Hacktoberfest! Check out our [Hacktoberfest Issues](HACKTOBERFEST_ISSUES.md) for contribution opportunities ranging from beginner to advanced levels.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git
- Basic understanding of image processing concepts (helpful but not required)

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/image-to-ascii.git
   cd image-to-ascii
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -e .[dev]
   ```

4. **Run Tests**
   ```bash
   pytest tests/ -v
   ```

## 🛠️ How to Contribute

### 1. Choose an Issue
- Browse our [issue tracker](https://github.com/yourusername/image-to-ascii/issues)
- Look for `good first issue` labels for beginner-friendly tasks
- Check [HACKTOBERFEST_ISSUES.md](HACKTOBERFEST_ISSUES.md) for detailed mathematical implementations

### 2. Claim an Issue
- Comment on the issue saying you'd like to work on it
- Wait for maintainer approval before starting work
- Ask questions if anything is unclear

### 3. Development Workflow
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make your changes
# ... code, test, repeat ...

# Run tests and linting
pytest tests/
black src/ tests/
flake8 src/ tests/

# Commit your changes
git add .
git commit -m "feat: add your feature description"

# Push to your fork
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

## 📝 Code Standards

### Python Style Guide
- Follow [PEP 8](https://pep8.org/) style guidelines
- Use [Black](https://black.readthedocs.io/) for code formatting
- Maximum line length: 88 characters
- Use type hints where appropriate

### Code Quality Tools
```bash
# Format code
black src/ tests/

# Check linting
flake8 src/ tests/

# Type checking (optional but recommended)
mypy src/
```

### Documentation
- Add docstrings to all public functions and classes
- Include mathematical formulas in docstrings when relevant
- Update README.md if adding new features
- Add examples for complex algorithms

## 🧪 Testing Guidelines

### Writing Tests
- Write tests for all new functionality
- Use descriptive test names: `test_brightness_mapping_with_edge_cases`
- Include edge cases and error conditions
- Test mathematical accuracy with known inputs/outputs

### Test Structure
```python
def test_feature_name():
    # Arrange
    input_data = create_test_data()
    
    # Act
    result = your_function(input_data)
    
    # Assert
    assert result == expected_output
    assert isinstance(result, expected_type)
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/

# Run specific test file
pytest tests/unit/test_ascii_conversion.py

# Run tests matching pattern
pytest -k "test_brightness"
```

## 📊 Mathematical Contributions

Many of our issues involve mathematical concepts. When contributing:

1. **Understand the Math**: Research the algorithm thoroughly
2. **Document Formulas**: Include mathematical notation in docstrings
3. **Provide References**: Link to papers or resources you used
4. **Add Examples**: Show the algorithm working with sample data
5. **Benchmark Performance**: Compare with existing implementations

### Example Mathematical Documentation
```python
def apply_sobel_filter(image: np.ndarray) -> np.ndarray:
    """
    Apply Sobel edge detection filter to image.
    
    The Sobel operator uses two 3×3 convolution kernels:
    Gx = [[-1, 0, 1],     Gy = [[-1, -2, -1],
          [-2, 0, 2],           [ 0,  0,  0],
          [-1, 0, 1]]           [ 1,  2,  1]]
    
    Edge magnitude: |G| = √(Gx² + Gy²)
    
    Args:
        image: Input grayscale image as numpy array
        
    Returns:
        Edge magnitude image
        
    References:
        Sobel, I. (1968). An Isotropic 3×3 Image Gradient Operator
    """
```

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Clear Description**: What happened vs. what you expected
2. **Reproduction Steps**: Minimal code to reproduce the issue
3. **Environment**: Python version, OS, package versions
4. **Sample Data**: Images or inputs that cause the problem
5. **Error Messages**: Full stack traces

### Bug Report Template
```markdown
**Bug Description**
Brief description of the issue

**To Reproduce**
1. Load image: `img = load_image('test.jpg')`
2. Convert: `ascii_art = image_to_ascii(img, 80)`
3. Error occurs

**Expected Behavior**
What should have happened

**Environment**
- Python version: 3.9.0
- OS: Ubuntu 20.04
- Package versions: `pip list`

**Additional Context**
Any other relevant information
```

## 🎨 Feature Requests

We love new ideas! When suggesting features:

1. **Check Existing Issues**: Avoid duplicates
2. **Explain Use Case**: Why is this feature needed?
3. **Provide Examples**: Show how it would work
4. **Consider Complexity**: Is it appropriate for the project scope?
5. **Mathematical Basis**: For algorithm features, explain the math

## 📋 Pull Request Guidelines

### Before Submitting
- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No merge conflicts

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Mathematical Details (if applicable)
- Algorithm used: [e.g., Floyd-Steinberg dithering]
- Complexity: O(n²)
- References: [links to papers/resources]

## Testing
- [ ] Added tests for new functionality
- [ ] All tests pass
- [ ] Tested with sample images

## Screenshots/Examples
[If applicable, show before/after ASCII art examples]
```

## 🏆 Recognition

Contributors will be:
- Listed in our README.md
- Mentioned in release notes
- Eligible for Hacktoberfest rewards (during October)
- Part of our growing community!

## 📞 Getting Help

- **Questions**: Open a GitHub Discussion
- **Real-time Chat**: Join our community Discord (link in README)
- **Email**: contributors@example.com

## 📜 Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md). We're committed to providing a welcoming and inclusive environment for all contributors.

---

Thank you for contributing to Image to ASCII Art Converter! Your efforts help make this project better for everyone. 🎉