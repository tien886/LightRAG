.PHONY: up \
        down \
        logs \
        install \
        run

up:  ## Start Neo4j + supporting containers
	podman-compose -f podman-compose.yml up -d

down:  ## Stop and remove all containers
	podman-compose -f podman-compose.yml down

logs:  ## Tail logs from all containers
	podman-compose -f podman-compose.yml logs -f

install:  ## Install Python dependencies
	pip install -r requirements.txt
run:  ## Start FastAPI server (production)
	python server.py
