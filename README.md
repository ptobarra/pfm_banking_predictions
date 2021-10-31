# PFM Statistics

PFM Backend Statistics project.

# Create virtual environment

Install virtualenv:

```bash
pip install virtualenv
```

Create a new virtual environment. 'venv' environment name:

```bash
virtualenv venv
```

Activate the virtual environment:

Mac/Linux

```bash
source ./venv/bin/activate
```

Windows

```bash
.\venv\Scripts\activate
```

Intall requeriments:

```bash
pip install -r requirements.txt
```

Add new python libraries to requirements.txt file

Generate requirements file:

```bash
pip freeze >  requirements.txt
```


At the moment, we are using FastAPI for the creation of the endpoints for the project.
To launch the project, you must access in a terminal the root folder of the project and execute this command:
```bash
uvicorn controllers.main_controller:main --reload
```