build:
	docker build . -t gradio-sp-inference-service:1.0.0
dev:
	docker run -p 8082:8082 --rm -it -v ${PWD}:/workspace $ gradio-sp-inference-service:1.0.0
