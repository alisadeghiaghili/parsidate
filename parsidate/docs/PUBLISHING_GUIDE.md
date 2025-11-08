# PUBLISHING_GUIDE.md

## How to Publish ParsiDate on PyPI

Follow these steps to publish a new version of the ParsiDate library to the Python Package Index (PyPI).

---

### 1. Prerequisites

- Python 3.8 or higher
- All required dependencies listed in `requirements.txt`
- PyPI account ([https://pypi.org/account/register/](https://pypi.org/account/register/))
- `twine`, `build`, and `setuptools` installed:

```pip install twine build setuptools wheel```

---

### 2. Project Preparation

- Ensure your source folder contains:
    - `setup.py`
    - `pyproject.toml` (optional for modern builds)
    - `README_COMPLETE.md`
    - `LICENSE`
    - `parsidate/` (main package folder, including py.typed)
    - All tests and documentation updated and passing

- Version must be updated in `setup.py` and (if present) `pyproject.toml`.
- Complete all unit tests and update change log.

---

### 3. Build the Package

Run the following in your project root:

```python -m build```

This creates the distribution files in the `dist/` directory.

---

### 4. Upload to TestPyPI (Optional Step)

For a dry run, use TestPyPI first:

```twine upload --repository testpypi dist/*```

Register and find your test page at [https://test.pypi.org/](https://test.pypi.org/).

---

### 5. Publish to PyPI

After checking everything, upload to PyPI:

```twine upload dist/*```

Enter your PyPI credentials when prompted. If successful, your library will be available at https://pypi.org/project/parsidate/

---

### 6. Post-Publish Steps

- Verify the published version and full functionality by installing: `pip install parsidate`
- Test with a clean environment to ensure no missing files.
- Announce release and update documentation badges, etc.

---

### 7. Tips & Gotchas

- Always include the `py.typed` marker file for PEP 561 type hint support.
- Ensure all dependencies are properly listed in `install_requires`.
- Use semantic versioning (e.g., 1.0.0 → 1.1.0 for features, 2.0.0 for breaking changes).
- Run full test suite before every publish.
- Keep `README.md` and license updated and accurate.
- Check long description rendering on PyPI (often from `README.md`).

---

### 8. Useful References

- [PyPI Project Page](https://pypi.org/)
- [Twine Docs](https://twine.readthedocs.io/en/stable/)
- [Python Packaging Guide](https://packaging.python.org/tutorials/packaging-projects/)
- [PEP 561](https://www.python.org/dev/peps/pep-0561/) (Type check support)

---

### 9. Example Project Tree

parsidate/
core/
...
init.py
py.typed
setup.py
pyproject.toml
LICENSE
README.md
README_COMPLETE.md
CHANGES.md
tests/
dist/


---

### 10. Questions

For help, create an issue on the GitHub repository or contact the maintainer at alisadeghiaghili@gmail.com.

---

Ali Sadeghi Aghili | 2025 | ParsiDate GPLv3
