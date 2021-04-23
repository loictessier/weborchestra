# weborchestra

weborchestra is a Django application whose main goal is to facilitate the sharing of scores within a musical ensemble while respecting the restrictions due to copyright.

## Structure

this project contains several apps :
- **core** : the base components
- **user** : handle authentication, roles and administration
- **music_library** : to create, access, update and delete music scores

## Tests

To run the tests you should first create a virtualenv.

```
python3 -m venv /path/to/new/virtualenv
source /path/to/new/virtualenv/bin/activate
```

Then install the packages with pip, there are several requirements files for the differents environments (local, production, staging).

```
pip install -r requirements/local.txt
```

Then you can run the tests :

```
python3 manage.py test
```

Use the coverage tool :

```
coverage run --source='.' manage.py test
coverage html
```