# Contributing to POF Engine

Thank you for your interest in contributing! This document provides guidelines for contributing to the POF Engine project.

## 🚀 Getting Started

### 1. Fork and Clone
```bash
git clone https://github.com/YOUR_USERNAME/POF_ENGINE.git
cd POF_ENGINE
git remote add upstream https://github.com/platonpavluk16/POF_ENGINE.git
```

### 2. Set Up Development Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install pytest black flake8  # Development tools
```

### 3. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

## 📝 Code Style

### Python Style Guide (PEP 8)
- Use 4 spaces for indentation
- Max line length: 100 characters
- Variable names: `snake_case`
- Class names: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`

### Format Code
```bash
black .
flake8 .
```

### Documentation
- Add docstrings to all classes and functions
- Use Google-style docstrings

Example:
```python
def calculate_distance(pos1, pos2):
    """Calculate Euclidean distance between two positions.
    
    Args:
        pos1: Tuple of (x, y) coordinates
        pos2: Tuple of (x, y) coordinates
    
    Returns:
        float: Distance between the two positions
    """
    pass
```

## 🧪 Testing

### Run Tests
```bash
pytest tests/
```

### Test Requirements
- Write tests for new features
- Maintain >80% code coverage
- Test edge cases

### Test Structure
```python
import unittest
from ECS.component import Component

class TestComponent(unittest.TestCase):
    def test_component_creation(self):
        comp = Component("test")
        self.assertEqual(comp.name, "test")
```

## 🔄 Git Workflow

### Commit Messages
Use clear, descriptive commit messages:

```
Type: Short description (max 50 chars)

Longer explanation if needed. Wrap at 72 characters.
Explain what and why, not how.

- Use bullet points for multiple changes
- Reference issues with #123
- Close issues with: Fixes #123
```

Types:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `refactor:` Code refactoring
- `perf:` Performance improvement
- `test:` Tests
- `chore:` Build/config changes

Example:
```
feat: Add particle system to render module

Implement basic particle effects with:
- Particle pooling for performance
- Custom emission shapes
- Color and lifetime properties

Closes #45
```

### Push and Pull Request
```bash
git push origin feature/your-feature-name
```

Create PR on GitHub with:
- Clear title
- Description of changes
- Reference to related issues
- Screenshots for visual changes

## ✅ PR Checklist

Before submitting:
- [ ] Code follows PEP 8 style
- [ ] All tests pass
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] No breaking changes (or well justified)
- [ ] Commit history is clean
- [ ] No unused imports or variables

## 🐛 Bug Reports

### Report Template
```markdown
**Description:**
Brief description of the bug

**Steps to Reproduce:**
1. ...
2. ...
3. ...

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Environment:**
- OS: Windows/Linux/macOS
- Python: 3.x
- Engine Version: 0.1.0

**Screenshots:**
(if applicable)
```

## ✨ Feature Requests

Include:
- Clear use case
- Why it's needed
- How it benefits users
- Potential implementation approach

## 📚 Documentation

### Update Required For:
- New public APIs
- User-facing changes
- Architecture changes
- Installation changes

### Files to Update:
- README.md
- PROJECT_STRUCTURE.md
- ARCHITECTURE.md
- Docstrings

## 🎯 Areas for Contribution

### High Priority
- [ ] Sound system
- [ ] Particle effects
- [ ] Animation system
- [ ] Performance optimization

### Medium Priority
- [ ] Advanced physics
- [ ] Asset manager
- [ ] More shape types
- [ ] UI improvements

### Low Priority
- [ ] Documentation improvements
- [ ] Example projects
- [ ] Code cleanup

## 📞 Communication

- **Issues**: For bugs and feature requests
- **Discussions**: For ideas and questions
- **Pull Requests**: For code submission

## ⚖️ License

All contributions are licensed under MIT License. By contributing, you agree to license your work under the same terms.

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

---

Thank you for contributing to POF Engine! 🎮
