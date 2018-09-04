## Activo
[![Maintainability](https://api.codeclimate.com/v1/badges/6594af3ff034d4737892/maintainability)](https://codeclimate.com/repos/5b16a8d8e4ba1a02d5001488/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/6594af3ff034d4737892/test_coverage)](https://codeclimate.com/repos/5b16a8d8e4ba1a02d5001488/test_coverage)

An asset-management tool for Andela

# Description 
 The **activo-api** is the backbone of an application for managing physical assets of the organisation. The project enables  centralised management of assets of the organisation. The api provides features for registering the allocation and usage of assets, repairs and conditions of devices, allocation of computer devices and seat allocations.

 The API documentation can be found here: [![Run in Postman](https://run.pstmn.io/button.svg)](https://www.getpostman.com/collections/3280d869f88ad87fd633)

 ## Key Application features  
1.	Inventory Management
2.	Asset Allocations
3.	Asset Maintenance & Repair logs

## Development set up
- Check that python 3 is installed:
    ```
    python --v
    >> Python 3.6.5
    ``` 

- Install pipenv:
    ```
    brew install pipenv
    ```

- Check pipenv is installed:
    ```
    pipenv --version
    >> pipenv, version 2018.6.25
    ```
    
- Check that postgres is installed:
    ```
    postgres --version
    >> postgres (PostgreSQL) 10.1

    ```

- Clone the activo-api repo and cd into it:
    ```
    git clone https://github.com/andela/activo-api.git

    ```
- Install dependencies:
    ```
    pipenv install
    ```

- Install dev dependencies to setup development environment:
    ```
    pipenv install --dev
    ```

- Rename the .env.sample file to .env and update the variables accordingly:
    ```
    FLASK_ENV = "development" # Takes either development, production, testing
    API_BASE_URL_V1 = "" # The base url for V1 of the API
    DATABASE_URI = "postgresql://YOUR_DB_USER:YOUR_DB_PASSWORD@YOUR_HOST/YOUR_DATABASE_NAME" # Development and production postgres db uri
    TEST_DATABASE_URI = "postgresql://YOUR_DB_USER:YOUR_DB_PASSWORD@YOUR_HOST/YOUR_TEST_DATABASE_NAME" # Testing postgres db uri
    JWT_PUBLIC_KEY = "" # Andela Authentication public key, obtained from the technology dept
    ```

- Activate a virtual environment:
    ```
    pipenv shell
    ```

- Apply migrations:
    ```
    flask db upgrade
    ```

- If you'd like to seed initial data to the database:
    ```
    flask seed_database
    ```

- Run the application:
    ```
    python manage.py runserver
    ```

- Should you make changes to the database models, run migrations as follows   
    - Migrate database:
        ```
        flask db migrate
        ```

    - Upgrade to new structure:
        ```
        flask db upgrade
        ```

- Deactivate the virtual environment once you're done:
    ```
    exit
    ```


## Contribution guide
##### Contributing
All proposals for contribution must satisfy the guidelines in the product wiki.
When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.This Project shall be utilising a [Pivotal Tracker board](https://www.pivotaltracker.com/n/projects/2170023) to track  the work done.

 ##### Pull Request Process
- A contributor shall identify a task to be done from the [pivotal tracker](https://www.pivotaltracker.com/n/projects/2170023).If there is a bug , feature or chore that has not been included among the tasks, the contributor can add it only after consulting the owner of this repository and the task being accepted.
- The Contributor shall then create a branch off  the ` develop` branch where they are expected to undertake the task they have chosen.
- Contributors are required to activate the git pre-commit hook to auto format staged Python files to pep8 with yapf and check for residual pep8 linting errors using pylint.
All commits are required to pass all checks from the pre-commit hook.
The pre-commit hook can be installed as follows:
Option 1: Copy the `hooks/pre-commit` file into the `.git/hooks` directory.
          You will need to do this every time the `hooks/pre-commit` file is changed.
Option 2: Create a file `.git/hooks/pre-commit` then create a symlink to this file by running the command:
          `ln -s -f ../../hooks/pre-commit .git/hooks/pre-commit`
          You will only need to do this once for your local repository.
- Although highly discouraged, the pre-commit hook can be bypassed by passing the `--no-verify` flag to the commit command as follows:
`git commit --no-verify -m "commit message"`
- After  undertaking the task, a fully detailed pull request shall be submitted to the owners of this repository for review. 
- If there any changes requested ,it is expected that these changes shall be effected and the pull request resubmitted for review.Once all the changes are accepted, the pull request shall be closed and the changes merged into `develop` by the owners of this repository.
