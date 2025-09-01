ruff_format:
	ruff format

run:
	cd src && python3 main.py

run_tests:
	pytest tests

docker-up:
	cd deploy/ && make deploy

docker-remove:
	-docker stop $$(docker ps -q)             
	-docker rm -f $$(docker ps -aq)           
	-docker rmi -f $$(docker images -q)
	-docker image prune -f

.PHONY: ruff_format