
generate-peas-client:
	npx swagger-typescript-api -p http://localhost:8000/openapi.json -o ./src/generated/

run-dev:
	npm start
	
container-test:
	docker build -t peas-frontend .
	docker run -it --rm -p 3000:3000 peas-frontend