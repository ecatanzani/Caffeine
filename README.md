# Caffeine
Personal Interactive Status Monitor

### Prerequisites
Caffeine requires a custom conda environment, provided by the requirements file for both macOS and Linux systems.
Due to packages compability create an empty conda env and install the specific requirements through the pip file.

Create a stand-alone conda env:
```conda create --name <env_name> python=3.9```


Pip installation:
After the env has been created: ```pip install -r <requirement_file>```


Conda installation: 
Remember to add the ```conda-forge``` channel to the current conda installation before create the new env, otherwise some packages will not be available: ```conda config --append channels conda-forge```

Create the new env as: ```conda create --name <env_name> --file <requirement_file>```