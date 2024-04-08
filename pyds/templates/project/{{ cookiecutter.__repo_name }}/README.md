# {{ cookiecutter.project_name }}

{{ cookiecutter.short_description }}

Made with ❤️ by {{ cookiecutter.full_name }} (@{{ cookiecutter.github_username }}).

## Get started for development

To get started:

```bash
git clone git@github.com:{{ cookiecutter.github_username }}/{{ cookiecutter.__repo_name}}
cd {{ cookiecutter.__repo_name }}
mamba env update -f environment.yml
conda activate {{ cookiecutter.__conda_env_name }}
python -m pip install -e .
```
