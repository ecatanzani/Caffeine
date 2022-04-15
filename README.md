# Caffeine
Personal Interactive Status Monitor

This tool is used to check and store athlete progresses together with the personal trainer.
The improvements are clearly visible in the storyboard for each class of body measurements.

![PHOTO-2021-08-24-09-38-07](https://user-images.githubusercontent.com/18316072/163548969-b7c90da5-1151-496b-af7c-2dccad033d03.jpg)

The simple interface permits to load the client record and the trend are automatically obtained in real-time. The web application is based on the streamlit framework.

<img width="1440" alt="Schermata 2022-04-15 alle 10 38 46" src="https://user-images.githubusercontent.com/18316072/163549111-cf50d901-717f-46f5-ac84-63d39c5b2225.png">


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

