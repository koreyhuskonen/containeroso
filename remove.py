#!/usr/local/bin/python3

# A convenience script to remove all Docker containers, images, and networks

import docker

client = docker.from_env()

for c in client.containers.list(all=True):
    c.remove(force=True)

client.images.prune(filters={"dangling": False})

client.networks.prune()
