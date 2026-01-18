# Contributing to DocuMind AI 🚀

First off, thank you for considering contributing to DocuMind AI! It's people like you that make the open-source community such an amazing place to learn, inspire, and create.

## 🛡️ Security Policy

**Please do not report security vulnerabilities through public GitHub issues.**
If you discover a potential security notification or have a question about the security of this project, please email the maintainer directly.

## 🤝 How to Contribute

### 1. Fork & Clone
1.  Fork the repo on GitHub.
2.  Clone the project to your own machine.

### 2. Branching Strategy
We look for clean, atomic commits.
*   **Feature Branches**: `feature/add-dark-mode`
*   **Bug Fixes**: `fix/upload-error`
*   **Documentation**: `docs/update-readme`

```bash
git checkout -b feature/amazing-feature
```

### 3. Development Workflow
*   **Backend**: Ensure you are using the virtual environment (`venv`). Run tests if available.
*   **Frontend**: Use `npm run lint` to ensure code quality before pushing.

### 4. Processing Secrets
*   **NEVER** commit your `.env` file.
*   **NEVER** hardcode API keys in your Python or TypeScript files.
*   If your contribution requires a new environment variable, update `.env.example` (with a dummy value) so others know to add it.

### 5. Pull Requests
1.  Push your branch to GitHub.
2.  Open a Pull Request (PR) against the `main` branch.
3.  Describe your changes clearly. "Fixed bug" is not enough; explain *what* you fixed and *how*.

## 🎨 Coding Standards

### Python (Backend)
- Follow **PEP 8** style guidelines.
- Use explicit type hinting (e.g., `def my_func(a: int) -> str:`).
- Document complex logic with docstrings.

### TypeScript (Frontend)
- Use functional components.
- Interfaces over Types where possible.
- Ensure the UI is responsive.

---
By contributing, you agree that your contributions will be licensed under its MIT License.