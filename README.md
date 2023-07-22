<h1 align="center">Foodgram Project React </h1>
<h1 align="center">
  
  [![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2F4erdenko%2Ffoodgram-project-react%2Fbadge&style=flat)](https://actions-badge.atrox.dev/4erdenko/foodgram-project-react/goto)
  
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)  
</h1>
  
<h1 align="center"><img src="https://i.imgur.com/E0AsEow.png" align="center" height="500" />
</h1>

Foodgram Project React is a web platform where users can share their recipes, add other users' recipes to their favorites, and create a shopping list based on selected recipes.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Steps](#steps)
- [Usage](#usage)
- [Configuration](#configuration)
- [Documentation](#documentation)
- [Data Import](#data-import)
- [CI/CD](#continuous-integration-and-deployment)
- [Contributing](#contributing)
- [Credits](#credits)
- [License](#license)

## Features

- Recipe management: Users can create, view, edit and delete their own recipes.
- Recipe view: Recipes from all users are available for view.
- Favorites: Users can add recipes to their favorites list.
- Shopping List: Users can create a shopping list based on selected recipes.

## Technologies

- Python 3.9
- Django 3.2
- React 17
- PostgreSQL 13
- Docker 20
- Nginx 1.19

## Installation

### Prerequisites

- Docker
- Docker-compose

### Steps

1. Clone this repository:

```bash
git clone https://github.com/4erdenko/foodgram-project-react.git
```

2. Navigate to the project directory:

```bash
cd foodgram-project-react
```

3. Create a .env file in the root directory and fill it with your environment variables. A template .env file can be found in the repository.

4. Run docker-compose to build and start the containers:

```bash
cd infra
docker compose up -d
```

5. The application will be accessible at `http://localhost` (or whatever your Docker host address is).

## Usage

To start using Foodgram Project React, create an account or log in using an existing one. You can then start creating, editing and deleting your recipes, as well as add other users' recipes to your favorites or to your shopping list.
## Configuration

The project uses environment variables for configuration. These variables are set in a file named `.env` which you'll need to create in the project root.

An example `.env` file, named `.env.EXAMPLE`, is included in the repository. This file lists all the environment variables used in the project with dummy values. Here's what the file contains:

```
POSTGRES_DB=kittygram
POSTGRES_USER=kittygram_user
POSTGRES_PASSWORD=kittygram_password
DB_HOST=db
DB_PORT=5432

SECRET_KEY='key'
DEBUG=False
ALLOWED_HOSTS=yourwebsite.com,111.222.333.444,127.0.0.1,localhost
CSRF=https://yourwebsite.com,https://111.222.333.444,127,http://127.0.0.1,http://localhost
```

To configure your application, make a new file named `.env` and copy the contents of `.env.EXAMPLE` into it. Then replace the dummy values with your actual data.

Here's what each of the environment variables is used for:

- `POSTGRES_DB`: The name of your PostgreSQL database.
- `POSTGRES_USER`: The username of your PostgreSQL user.
- `POSTGRES_PASSWORD`: The password for your PostgreSQL user.
- `DB_HOST`: The hostname where your PostgreSQL database is hosted.
- `DB_PORT`: The port number on which your PostgreSQL service is running.

- `SECRET_KEY`: A secret key for Django.
- `DEBUG`: A boolean flag that turns on/off debug mode in Django.
- `ALLOWED_HOSTS`: A comma-separated list of strings representing the host/domain names that this Django site can serve.
- `CSRF`: The list of trusted origins for CSRF. If not provided, Django will use `ALLOWED_HOSTS`.

**Note:** Remember to set `DEBUG` as `False` when you're running in a production environment. Also, make sure to use a strong, unpredictable secret key.
## Documentation

The project includes documentation for the API endpoints. The documentation is automatically generated and can be accessed via the web interface.

To run the documentation locally, ensure you have Docker and docker-compose installed, then follow the steps below:

1. Navigate to the `infra/api` directory:

```bash
cd infra/api
```

2. Run the docker-compose file:

```bash
docker compose up -d
```

This will start two containers: one for the frontend and another for the Nginx server. Nginx is configured to serve the frontend application and the documentation.

3. Open your web browser and navigate to `http://localhost/api/docs`.

You should now be able to see the documentation for the project's API.
## Data Import

To import ingredient data into your application, navigate to the root directory of your project and run the following command:

```bash
python manage.py import_ingredients path/to/ingredients.csv
```
Or make sure that the ingredients.csv file is in the same directory.
## Continuous Integration and Deployment

The project uses GitHub Actions to automatically run tests, build Docker images, and deploy the application whenever changes are pushed to the `master` branch. 

The CI/CD workflow is defined in a file named `.github/workflows/pipeline.yml` in your repository.

The workflow consists of the following jobs:

- `backend_tests_and_build_and_push_to_docker_hub`: This job runs the backend tests, builds the backend Docker image, and pushes it to Docker Hub.

- `build_frontend_and_push_to_docker_hub`: This job depends on the successful completion of the previous job. It builds the frontend Docker image and pushes it to Docker Hub.

- `Deployment`: This job depends on the successful completion of the previous job. It prepares the environment on the server, deploys the new Docker images, and handles database migrations and static files.

- `Telegram_Notification`: This job sends a notification to a specified Telegram chat upon successful deployment.

### Configuration

The workflow uses GitHub Secrets to manage sensitive data like usernames, passwords, and SSH keys. You will need to set up these secrets in your GitHub repository's settings.

Here's what each secret is used for:

- `DOCKER_USERNAME`: Your Docker Hub username.
- `DOCKER_PASSWORD`: Your Docker Hub password.
- `HOST`: The IP address or domain name of your server.
- `USER`: The username you use to SSH into your server.
- `SSH_KEY`: The private SSH key to connect to your server.
- `SSH_PASSPHRASE`: The passphrase of your SSH key, if it's protected by one.
- `ENV`: The environment variables for your application, formatted as a string.
- `TELEGRAM_TOKEN`: The token for the Telegram bot that sends deployment notifications.
- `TELEGRAM_TO`: The ID or username of the Telegram chat where deployment notifications are sent.

### Deployment

Whenever you push changes to the `master` branch, the workflow runs and automatically deploys your application if the tests pass and the Docker images build successfully.

Upon successful deployment, you will receive a notification in the specified Telegram chat. If something goes wrong, you can check the workflow's logs in your repository's "Actions" tab on GitHub.

**Note:** This workflow assumes that you have a server set up with Docker and Docker Compose installed. If your server setup is different, you might need to modify the workflow file to fit your needs.
## Contributing

Contributions are welcome. Please open an issue to discuss the proposed changes, or open a pull request with changes.

## Credits

- Author: [Valentin Kharenko](https://github.com/4erdenko)
- Code Reviewer: [Artem Nechai](https://github.com/Corrosion667)

## License

Foodgram Project React is licensed under the [MIT License](LICENSE).
