# How To Install Shell Plus For Django

## Overview of Shell Plus

[Django Shell Plus](https://django-extensions.readthedocs.io/en/latest/shell_plus.html) has the following advantages

- You don't need to manually import models, etc - it does it for you every time
- Your Django console has colors, better error messages, and more interactivity because it can be using [iPython](https://ipython.readthedocs.io/en/stable/)
  - Colors
  - Better error messages
  - Debugger
  - Jupyter Notebook

For Django not having to manually import stuff, and the colors/better error messages are the big benefits.

Django Shell Plus is a part of [Django Extensions](https://django-extensions.readthedocs.io/en/latest/installation_instructions.html)

## Installation

You need to do this for every Django Project you want it for - it's not global.

1. Activate the Python Virtual Environment for your Django Project
2. `pip install django-extensions`
3. Add `django_extensions` to `INSTALLED_APPS` for `settings.py` in your Django Project [like how the docs say here](https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration)
4. `pip install ipython` as you almost definitely want to use iPython with shell plus. This may have additional steps, if needed [follow the iPython docs install instructions](https://ipython.readthedocs.io/en/stable/install/index.html)

Step 4 is optional but highly recommended.

And, that's it!

## Running shell plus

Instead of `python manage.py shell`, run:

```bash
python manage.py shell_plus --ipython
```

That will run shell plus using iPython, **and set iPython to be your default.** So next time you only need to run:

```bash
python manage.py shell_plus
```

and it will use iPython automatically. If you don't want to use iPython omit the `--ipython` in the previous command.

You can see the full list of options and features for shell_plus [here in the docs](https://django-extensions.readthedocs.io/en/latest/shell_plus.html)

## Recommendations

As this needs to be installed per-project, if you want to do this, make it the first thing you do for every Django Project. Start by installing iPython, using it when you use shell plus as described, and don't worry about any of the fancy features.

*If all this feels like overkill or too many steps, don't worry about it and just stick with the regular Django Shell - it works just fine!*



