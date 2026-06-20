# Contributing to Tent of Trials / Kickama

Thank you for your interest in contributing! This project is a polyglot monorepo with modules in Python, Rust, TypeScript, Go, Java, Ruby, Lua, Haskell, and C/C++.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Module Overview](#module-overview)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Issue Reporting](#issue-reporting)
- [Bounty Process](#bounty-process)
- [License](#license)

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/Kickama
   cd Kickama
   ```
3. Add the upstream remote:
   ```bash
   git remote add upstream https://github.com/lobster-trap/Kickama.git
   ```

## Development Setup

### Prerequisites

Install dependencies for the modules you want to work on:

**Python (tooling):**
```bash
python3 -m pip install -r requirements-dev.txt  # if available
```

**Rust (backend):**
```bash
curl https://sh.rustup.rs -sSf | sh
source "$HOME/.cargo/env"
cargo fetch
```

**TypeScript / React (frontend):**
```bash
npm install
```

**Go (market):**
```bash
go mod download
```

### Build All Modules

```bash
python3 build.py              # Build all modules
python3 build.py --clean      # Clean all artifacts
python3 build.py --module backend,frontend  # Build specific modules
python3 build.py --release    # Release mode (Rust only)
```

Build diagnostics are written to the `diagnostic/` directory. Include them in your PR for verification.

## Module Overview

| Module | Language | Directory | Description |
|--------|----------|-----------|-------------|
| tooling | Python | `tools/` | Build scripts, CI utilities |
| backend | Rust | `backend/` | Core trading engine |
| frontend | TypeScript | `frontend/` | Web UI (React) |
| market | Go | `market/` | Market data processing |
| frailbox | C | `frailbox/` | Low-level signal processing |
| engine | C++ | `engine/` | Order book engine |
| compliance | Java | `compliance/` | Regulatory checks |
| market v2 | Ruby | `v2/` | Alternative market module |
| scans | Lua | `scans/` | Scanning utilities |
| openapi | Haskell | `openapi/` | API specification tools |
| openapi-tools | Lua | `openapi-tools/` | OpenAPI tooling |
| data | (mixed) | `data/` | Sample data and generators |

## Coding Standards

### General
- **EditorConfig**: This project includes a `.editorconfig` file. Please ensure your editor supports it.
- **Line endings**: LF (Unix-style)
- **Encoding**: UTF-8
- **Trailing whitespace**: Trim trailing whitespace (except in Markdown)

### Language-Specific
- **Python**: Follow PEP 8. Use type hints for all public functions.
- **Rust**: Follow Rustfmt defaults. Run `cargo fmt` before committing.
- **TypeScript/JavaScript**: Use 2-space indentation. Follow the existing style.
- **Go**: Follow `gofmt`. Use tab indentation.
- **Java**: Follow Google Java Style Guide.
- **C/C++**: Follow the existing code style.
- **Ruby**: Follow the community style guide (2-space indentation).

## Testing

Run tests for the specific module you're modifying:

```bash
# Python
python3 -m pytest tests/ -v

# Rust
cd backend && cargo test

# TypeScript
npm test

# Go
cd market && go test ./...
```

## Pull Request Guidelines

1. **Branch Naming**: Use prefixes like `fix/`, `feat/`, `docs/`, `chore/` followed by a brief description.
2. **Commit Messages**: Write clear, descriptive commit messages. Reference related issues.
3. **Single Purpose**: Each PR should address a single issue or feature.
4. **Include Diagnostics**: If the build system produces diagnostic files, include them in your PR.
5. **Keep It Small**: Smaller PRs are reviewed faster.
6. **Update Documentation**: If your change affects the API or behavior, update relevant docs.

### PR Checklist

Before submitting your PR, ensure:

- [ ] Code compiles without errors
- [ ] Tests pass
- [ ] New tests added for new functionality
- [ ] Code follows project coding standards
- [ ] Commit messages reference related issues
- [ ] Diagnostic files included (if applicable)
- [ ] No unrelated changes

## Issue Reporting

- Search existing issues before creating a new one.
- Use the issue templates if available.
- Include steps to reproduce for bugs.
- Label your issue appropriately.

## Bounty Process

Bounties are tracked as GitHub issues with the `bounty` label. Each bounty has a fixed price.

1. **Claim**: Comment on the issue to express interest (optional but recommended).
2. **Work**: Fork the repo, create a branch, implement the fix.
3. **Submit**: Open a pull request. Include "Closes #ISSUE_NUMBER" in the description.
4. **Review**: Maintainers will review your PR.
5. **Payout**: Once merged, the bounty amount is paid out as per the project's payment process.

## License

This project incorporates components under the following licenses:

- Apache License, Version 2.0 (default for new contributions)
- MIT License (for specific components)

See the `LICENSE` file for details.

---

**Note**: By contributing, you agree that your contributions will be licensed under the project's license(s).
