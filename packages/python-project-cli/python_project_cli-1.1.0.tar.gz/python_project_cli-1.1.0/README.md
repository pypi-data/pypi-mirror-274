# MentorMate Python CLI
A CLI tool for generating Django and FastAPI projects.

![Tests](https://github.com/MentorMate/python-project-cli/actions/workflows/tests.yaml/badge.svg)

![Deploy](https://github.com/MentorMate/python-project-cli/actions/workflows/main_release.yaml/badge.svg)

## Overview
This is a python-cli tool for interactive project setup, following best practices for **Django** and **FastAPI**.
In order to assure easier distribution, the project is deployed as **pypi** package.
For optimal maintenance the project utilizes the **tox** framework.

# Installation
We use `pip` for our package distribution, that's why we recommend that you use a virtual environment for the package installation (`venv` or `poetry`).
```bash
pip install python-project-cli
```

## Commands
1. **generate**s a new project in interactive mode, usesing `cookiecutter`.
    ```bash
    python-cli generate
    ```

2. Shows the framework repo **status**. We aim to update the main templates frequently, in order to keep up with the everevolving "best" practices, that's why there's a chance for a repo downtime.
    ```bash
    python-cli status
    ```

3. Project's **version**.
    ```bash
    python-cli version
    ```

### Frameworks
- Django
- FastAPI

### Project Maintenance (Internal)
[Confluence link](https://mentormate.atlassian.net/wiki/spaces/MMSDLC/pages/4325900953/Python+CLI+documentation)

## License
PYTHON-PROJECT-CLI is unlicensed, as found in the
[LICENSE](https://github.com/MentorMate/python-project-cli/blob/development/LICENSE) file.
