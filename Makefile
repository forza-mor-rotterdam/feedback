# Build scripts to run commands within the Docker container or create local environments

# Docker variables
RUN_IN_NEW_WEBCONTEXT = docker-compose run -it feedback_app
EXEC_IN_WEB = docker-compose run feedback_app
EXEC_IN_WEB_CMD = $(EXEC_IN_WEB) python manage.py

#  General
##############################################

run: ## start the stack
	@echo Running from file. './docker-compose.yml.'
	docker-compose up

run_and_build: ## Build and then start the stack
	@echo Building containers and running from file. './docker-compose.yml.'
	docker-compose up --build

stop: ## Stop containers
	@echo Stopping containers.
	docker-compose down

clear_docker_volumes: ## clear docker volumes
	check_clean_db
	@echo Stopping and removing containers.
	docker-compose down -v

create_superuser: ## create superuser for public tenant
	@echo Create superuser. You will be prompted for email and password
	$(EXEC_IN_WEB_CMD) createsuperuser

check_clean_db: ## clear docker vols
	@echo -n "This will clear local docker volumes before running tests. Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]

format: ## Use pre-commit config to format files
	pre-commit run --all-files

# Static files
##############################################

collectstatic: ## collectstatic files
	$(EXEC_IN_WEB_CMD) collectstatic

makemigrations: ## Makemigrations
	$(EXEC_IN_WEB_CMD) makemigrations

migrate: ## Migrate
	$(EXEC_IN_WEB_CMD) migrate