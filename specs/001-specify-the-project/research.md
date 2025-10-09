# Research for Image to ASCII Generator with Advanced Math

## Decision: Advanced Math for Symbol Selection
**Decision**: Use statistical moments (central and normalized moments) for dynamic symbol selection in image to ASCII conversion.

**Rationale**: Statistical moments provide a mathematically rigorous way to capture intensity distribution and shape characteristics of image blocks, allowing for advanced, first-principles based matching to ASCII symbols. This improves the "fit" of symbols to image regions using linear algebra and statistics, all implementable with NumPy.

**Alternatives Considered**:
- Principal Component Analysis (PCA) for shape matching: Rejected due to higher computational complexity and potential overkill for symbol selection.
- Optimization-based least squares: Rejected for performance concerns in real-time conversion.

## Decision: Project Structure
**Decision**: Use a src/ package layout with separate modules for image loading, ASCII conversion, output, and CLI, plus tests/ for pytest and docs/ for per-feature Markdown files.

**Rationale**: Promotes separation of concerns, modularity, and ease of testing/maintenance. Per-feature docs in MD files fulfill the documentation requirement without cluttering code.

**Alternatives Considered**:
- Flat script structure: Rejected for poor scalability and lack of modularity.
- Monolithic file: Rejected for violating separation of concerns.

## Decision: Libraries and Dependencies
**Decision**: Use only Pillow (PIL) for image handling and NumPy for array operations, sticking to standard library for the rest.

**Rationale**: Keeps the implementation simple and adheres to the "no advanced libraries" constraint while enabling necessary image processing and math.

**Alternatives Considered**:
- OpenCV: Rejected for being an advanced library not needed for basic ops.
- Scipy: Rejected as overkill for this scope.

## Decision: Python Version
**Decision**: Target Python 3.8+ for compatibility with Pillow and NumPy.

**Rationale**: Ensures broad compatibility without issues on modern systems, as older versions may lack features.

**Alternatives Considered**:
- Python 3.6: Rejected due to potential compatibility issues with newer PIL versions.
- Python 3.12+: Rejected to avoid limiting users on older systems unnecessarily.