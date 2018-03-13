.PHONY: help
help:
	@# Print help text
	@./make-help.py $(MAKEFILE_LIST)

.PHONY: build
build:
	@# Build the docker image for lime-mud
	docker build --pull -t lime-mud .

.PHONY: test
test: build
	@# Run unit tests for lime-mud
	docker run lime-mud python3 manage.py test


.PHONY: publish
publish: test
	@# Upload lime-mud to our PyPi server
	@docker run lime-mud python3 manage.py upload --username $(DEVPI_USERNAME) --password $(DEVPI_PASSWORD) --index https://pypi.lundalogik.com:3443/lime/develop/+simple/


.PHONY: ptw
ptw:
	@# Start watching file system for changes and re-run tests when a change is detected.
	docker-compose run app ptw
