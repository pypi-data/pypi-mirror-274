

LIBC ?= manylinux
ARCH ?= x86_64
DOCKER_ARGS := --build-arg ARCH=$(ARCH) --file docker/Dockerfile.$(LIBC) --tag $(LIBC)-$(ARCH)-dist --load
DOCKER_RUN_ARGS := --rm -d --name $(LIBC)-$(ARCH)-dist

.PHONY: clean dist/${LIBC}-${ARCH}

all: dist/${LIBC}-${ARCH}

clean:
	rm -rf dist

dist/${LIBC}-${ARCH}:
	docker buildx build $(DOCKER_ARGS) .
	docker run $(DOCKER_RUN_ARGS) $(LIBC)-$(ARCH)-dist
	docker cp $(LIBC)-$(ARCH)-dist:/build/dist dist
	docker stop -t 0 $(LIBC)-$(ARCH)-dist
