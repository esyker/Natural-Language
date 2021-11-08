1. Create a virtual env outside the folder where the code is:

1.1 Create:
> virtualenv ln-virtual-env

1.2 Activate:
> source ln-virtual-env/bin/activate

(On Windows: > .\ln-virtual-env\Scripts\activate)

To check if the right Python is being used: 
> which python

(On Windows: > where python)

More on virtualenv: https://virtualenv.pypa.io/en/legacy/userguide.html

If you have any trouble with virtualenv, an alternative is Conda: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html


2. Install the requirements (inside the project folder):
> pip install -r requirements.txt