# Configuration Structure

This document explains the configuration file structure for the civiclookup project.

## Python Configuration Files

The Python configuration files are located at the repository root:

- `requirements.txt`: Python dependencies
- `pyproject.toml`: Configuration for Black and isort
- `mypy.ini`: Type checking configuration
- `.flake8`: Linting configuration

### Why are these files at the root?

Most Python tools look for their configuration files in the current directory and work their way up to the repository root. While it's possible to specify custom locations for these files using command-line arguments, it adds complexity and can make development workflows harder.

For example:
- `pip install -r` expects requirements.txt in the current directory
- `black` and `isort` look for pyproject.toml at the repository root
- `mypy` looks for mypy.ini at the repository root
- `flake8` looks for .flake8 at the repository root

## JavaScript Configuration Files

The JavaScript configuration files are located in the `js/` directory:

- `package.json`: NPM package configuration and dependencies
- `.prettierrc`: Prettier formatting configuration
- `.eslintrc.json`: ESLint linting configuration
- `tsconfig.json`: TypeScript configuration

These files are localized to the JavaScript portion of the project since:
- Node.js tooling expects these files in the directory where you run npm commands
- It keeps the language-specific configuration isolated

## Alternatives

If you prefer to have more organized configuration files:

1. For Python, you could move the config files to a dedicated `config/` directory, but you would need to specify their location when running tools:
   ```bash
   black --config=config/pyproject.toml python/
   flake8 --config=config/.flake8 python/
   mypy --config-file=config/mypy.ini python/
   ```

2. For Python package development, you could use [setuptools-scm](https://github.com/pypa/setuptools_scm) to handle versioning and configuration in a more organized way.

3. For monorepo-style organization, tools like [Poetry](https://python-poetry.org/) or [Pants](https://www.pantsbuild.org/) provide better support for organizing complex repositories.