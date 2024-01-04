# DevOps Apprenticeship: Project Exercise

> If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter). Note this VM comes pre-setup with Python & Poetry pre-installed.

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.8+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

This project uses the Trello REST API, so you will need to create a free Trello account, your Trello workspace and a board that the application can use to store your To Do items. The steps to get the Board ID are below.
1. Create a free Trello account via the sign up link: https://trello.com/signup
2. Create a Trello workspace via the appropriate link.
3. Create a new board via the appropriate link.
4. Immediately after the board has been created, add ".json" to the end of the URL in your browser address bar.
5. Copy the first "id" field which is your `board_id`.
NOTE: Trello should automatically create To Do and Done lists on the new board, however if this is not the case, the application will create these for you when it starts.

The Trello API also requires an API Key (`api_key`) and a Token (`token`) for authorisation.

Trello API Key and Token creation: 
1. Create a new custom Power-Up and link it to your workspace: https://developer.atlassian.com/cloud/trello/guides/power-ups/managing-power-ups/#adding-a-new-custom-power-up
2. Generate the API Key: https://developer.atlassian.com/cloud/trello/guides/power-ups/managing-power-ups/#generating-an-api-key
3. Generate the Token by visiting the Power-Ups Admin screen, selecting your Power-Up, clicking API Key and then the Token link.

Lastly, these three parameters need to added into the  `.env` file that you have cloned previously in the fields below.

# Trello token and API key for utilising Trello REST API
TRELLO_API_KEY=`api_key`
TRELLO_TOKEN=`token`

# Trello board id
TRELLO_BOARD_ID=`board_id`

## Running the App Locally

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

You can add a new to-do item by entering the task in the text box and clicking the Add button.
You can mark an item as Done by selecting the relevant checkbox and clicking the Done button. You can select multiple items at once. Completed items will move to the bottom of the task list.
You can delete an item from the list completely by selecting the relevant checkbox and clicking the Delete button. You can select multiple items at once.

## Running the App On A Remote VM

Ensure that you have the `.env.j2`, `inventory.ini`, `playbook.yml` and `todoapp.service` files on the VM that you are going to use as your Ansible control node. You should make sure you are able to SSH from the control node to the target machine where you want to run the application. Issue the following command from your home directory on the control node:
```bash
$  ansible-playbook playbook.yml -i inventory.ini
```
This will install the application on the target VM and start the application service. You should then be able to access the application by navigating to http://*your_target_vm_ip*:5000

## Running the App in a container using Docker

It is a prerequisite to have a Docker Engine running before attempting to build the environments. You can do this by installing Docker Desktop (licenses are free for educational use even in a professional environment): https://docs.docker.com/get-docker/

Once you have the Docker Engine running you can build the development and production images using the following commands.

## Building the Docker image per environment
```bash
$  docker build --target development --tag todo-app:dev
$  docker build --target production --tag todo-app:prod
```

Once the images are successfully built, you can run the development and production containers using the following commands.

## Running the Development container (with flask and hot reload)
```bash
$  docker run --env-file ./.env -p 5000:5000 --mount "type=bind,source=$(pwd)/todo_app,target=/opt/todoapp/todo_app" todo-app:dev
```
[NOTE: For running the development environment you can also use the docker-compose.yml file, by running the `docker compose up` command.]

## Running the Production container (with gunicorn)
```bash
$  docker run --env-file ./.env --publish 5000:8000 todo-app:prod
```

## Running the Tests

In order to run the tests you will need to make sure that Pytest is installed by running the below once all the above steps have been followed.
```bash
$ poetry add pytest
```
Pytest will pickup tests in files with a name of the form `test_*.py` or `*_test.py`. The tests can be found in the `./todo_app/test` folder.

To run all the tests you can execute the below on the Terminal in VSCode.
```bash
$ poetry run pytest
```
Alternatively you can run all the tests or run them individually from the command line by opening a prompt from the project folder and using:
```bash
$ poetry run pytest ./todo_app/test/test_view_model.py
$ poetry run pytest ./todo_app/test/test_client.py
$ poetry run pytest ./todo_app/test
```




