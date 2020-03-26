#!/usr/local/bin/python3

import docker

client = docker.from_env()

for c in client.containers.list(all=True):
    c.remove(force=True)

client.images.prune(filters={"dangling": False})

client.networks.prune()

client.images.build(path=".", dockerfile="Dockerfile.virtuoso", tag="virtuoso", rm=True)
