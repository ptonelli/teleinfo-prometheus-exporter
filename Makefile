IMAGE_NAME := teleinfo-prometheus-exporter
REGISTRY := docker.nautil.org
PUSH_TAG := $(REGISTRY)/$(IMAGE_NAME):$(shell date +%Y%m%d%H%M%S)

docker:
	docker build --network host -t $(IMAGE_NAME):latest .

push:
	docker tag $(IMAGE_NAME):latest $(PUSH_TAG)
	docker push $(PUSH_TAG)
