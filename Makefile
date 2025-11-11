build:
	docker build -t diogofonseca/bookstore:latest .

run:
	docker run -p 8000:8000 diogofonseca/bookstore:latest

push:
	docker push diogofonseca/bookstore:latest

all: build run
