# CONTRIBUTING.md

## Contributing to ParsiDate

Thank you for your interest in contributing to ParsiDate!

---

### How to Contribute

1. **Fork this repository**  
   Click the “Fork” button at the top right to create your own copy.

2. **Clone your fork**
```bash
git clone https://github.com/alisadeghiaghili/parsidate.git
cd parsidate
```

3. **Create a feature branch**
`git checkout -b feature/my-feature`

4. **Make your changes**
- Follow the existing code style (PEP8, black, isort).
- Add or update tests if your code alters logic or fixes a bug.
- Add or update docstrings and docs as appropriate.

5. **Run tests and static checks**
```bash
pytest tests/
mypy parsidate/
flake8 parsidate/
isort parsidate/
black --check parsidate/
```

6. **Commit with a descriptive message**
`git commit -am "Add X feature / Fix Y bug"`

7. **Push to your fork**
`git push origin feature/my-feature`


8. **Open a Pull Request**
- Go to your fork on GitHub.
- Click “Compare & Pull Request”.
- Describe your change clearly (purpose, behavior, test info).

---

### Guidelines

- All code must be documented and type-annotated.
- Pass all tests before PR submission.
- Write test coverage for any new feature or bugfix.
- Add yourself to the CONTRIBUTORS list at the end of this file.

---

### Coding Standards

- Follow **PEP8**, **black**, **isort**
- Docstrings must be present for all classes, methods, and modules.
- Use meaningful commit messages.
- Use semantic versioning for any releases or feature additions.

---

### Reporting Issues

If you encounter a bug or want a feature, open an issue. Provide:
- Clear title and description.
- Steps to reproduce for bugs.
- Example code and expected/actual results.

---

### License

By contributing, you agree that your code may be licensed under GPLv3 to all users of this repository.

---

### Maintainer

Ali Sadeghi Aghili (alisadeghiaghili@gmail.com)

---

### Contributors

- Ali Sadeghi Aghili
- [Add your name here]
