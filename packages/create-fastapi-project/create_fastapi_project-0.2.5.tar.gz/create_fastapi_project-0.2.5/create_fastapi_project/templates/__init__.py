import os
import shutil
from enum import Enum
from dotenv import dotenv_values
from create_fastapi_project.helpers.install import (
    add_configuration_to_pyproject,
    install_dependencies,
)


class ITemplate(str, Enum):
    basic = "basic"
    langchain_basic = "langchain_basic"
    full = "full"


def install_template(root: str, template: ITemplate, app_name: str):
    print(f"Initializing project with template: {template}")
    # Get the directory of the current script
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_script_dir, template)

    eslint = False
    # Define the files and subdirectories to copy
    ignore: list[str] = []
    if not eslint:
        ignore.append(".env")

    # Copy files and subdirectories
    shutil.copytree(
        template_path,
        root,
        symlinks=False,
        ignore=shutil.ignore_patterns(*ignore),
        copy_function=shutil.copy2,
        ignore_dangling_symlinks=True,
        dirs_exist_ok=True,
    )

    poetry_path = os.path.join(root, "backend", "app")
    if  template == ITemplate.langchain_basic:
        # TODO: CHECK PATHS IN MACOS AND WINDOWS | (os.path.join)        
        poetry_frontend_path = os.path.join(root, "frontend", "app")
    
    has_pyproject = add_configuration_to_pyproject(poetry_path)

    if has_pyproject:
        dependencies = [
            "fastapi[all]",
            "fastapi-pagination[sqlalchemy]",
            "asyncer",
            "httpx",
        ]
        dev_dependencies = [
            "pytest",
            "mypy",
            "ruff",
            "black",
        ]
        if template == ITemplate.langchain_basic:
            langchain_dependencies = [
                "langchain",
                "openai",
                "adaptive-cards-py",
                "google-search-results",
            ]
            frontend_dependencies = [
                "streamlit",
                "websockets",
            ]
            dependencies.extend(langchain_dependencies)
        if template == ITemplate.full:
            full_dependencies = [
                "alembic",
                "asyncpg",
                "sqlmodel",
                "python-jose",
                "cryptography",
                "passlib",
                "SQLAlchemy-Utils",
                "SQLAlchemy",
                "minio",
                "Pillow",
                "watchfiles",
                "asyncer",
                "httpx",
                "pandas",
                "openpyxl",
                "redis",
                "fastapi-async-sqlalchemy",
                "oso",
                "celery",
                "transformers",
                "requests",
                "wheel",
                "setuptools",
                "langchain",
                "openai",
                "celery-sqlalchemy-scheduler",
                "psycopg2-binary",
                "fastapi-limiter",
                "fastapi-pagination[sqlalchemy]",
                "fastapi-cache2[redis]",
            ]
            full_dev_dependencies = [
                "pytest-asyncio",
            ]
            dependencies.extend(full_dependencies)
            dev_dependencies.extend(full_dev_dependencies)

        print("- Installing main packages. This might take a couple of minutes.")
        print("poetry_path", poetry_path)
        print("template", template)
        install_dependencies(poetry_path, dependencies)
        print("- Installing development packages. This might take a couple of minutes.")
        install_dependencies(poetry_path, dev_dependencies, dev=True)

        if template == ITemplate.langchain_basic:
            add_configuration_to_pyproject(poetry_frontend_path)
            print(
                "- Installing frontend packages. This might take a couple of minutes."
            )
            install_dependencies(poetry_frontend_path, frontend_dependencies)

        # Set your dynamic environment variables

        # Load variables from .env.example
        example_env = dotenv_values(".env.example")
        example_env["PROJECT_NAME"] = app_name

        # Write modified environment variables to .env and .env.example file
        with open(".env", "w") as env_file, open(
            ".env.example", "w"
        ) as example_env_file:
            for key, value in example_env.items():
                env_file.write(f"{key}={value}\n")
                example_env_file.write(f"{key}={value}\n")

    return has_pyproject
