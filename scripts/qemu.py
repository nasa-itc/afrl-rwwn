#!/usr/bin/env python3

import argparse
import subprocess
import multiprocessing as mp 
from pathlib import Path

import docker

REPO_ROOT = Path(__file__, "../..").resolve()

QEMU_RUNNER_IMAGE = "itc/qemu"
QEMU_BUILDER_IMAGE = "itc/qemu-builder"
QEMU_BUILD_CACHE_VOLUME = "qemu-build-cache"
processes=[]

def build_docker_image(tag, path):
    """build qemu docker image if it doesn't exist"""
    # connect to docker daemon
    client = docker.from_env()
    # get docker image to see if it already exists
    build_image = False
    try:
        image = client.images.get(tag)
    except docker.errors.ImageNotFound:
        # prompt user to create docker image
        if input(f"docker image '{tag}' does not exist. create (y/n)? ").lower() in ["y", "yes"]:
            build_image = True
        else:
            raise
    # build qemu builder image
    if build_image:
        #image, logs = client.images.build(path=str(path), tag=tag, forcerm=True)
        logs = client.api.build(path=str(path), tag=tag, forcerm=True, decode=True)
        for entry in logs:
            if "stream" in entry:
                print(entry["stream"], end="")

def build_qemu(tag=QEMU_BUILDER_IMAGE, build_cache=QEMU_BUILD_CACHE_VOLUME, args=[]):
    """build qemu using docker qemu builder image"""
    # connect to docker daemon
    client = docker.from_env()
    # build qemu builder image
    docker_path = Path(REPO_ROOT, "docker/qemu-builder")
    build_docker_image(tag, docker_path)
    # create build cache volume if it doesn't exist
    try:
        volume = client.volumes.get(build_cache)
    except docker.errors.NotFound:
        volume = client.volumes.create(name=build_cache)
    # run docker build
    mounts = {str(REPO_ROOT): {"bind": "/qemu/src", "mode": "rw"},
              build_cache: {"bind": "/qemu/build", "mode": "rw"}}
    container = client.containers.run(tag, command=args, volumes=mounts, auto_remove=True, detach=True)
    for chunk in container.logs(stream=True):
        print(chunk.decode(), end="")

def run_qemu(tag=QEMU_RUNNER_IMAGE, instances=1, args=[]):
    """run qemu"""
    # build qemu runner image
    docker_path = Path(REPO_ROOT, "docker/qemu")
    build_docker_image(tag, docker_path)
    # run qemu
    try:
        for i in range(instances):
            p = mp.Process(target=run_qemu_instance, args=(i,))
            p.start()        
            processes.append(p)  # Keep list of processes (maybe just pids?) to clean up later?
    except KeyboardInterrupt:
        pass

def run_qemu_instance(i):
    docker_path = Path(REPO_ROOT, "docker/qemu")
    docker_path = docker_path / ".." 
    subprocess.run(["docker-compose", "-p", str(i), "up", "--detach"], cwd=docker_path)
    subprocess.run(["mate-terminal", "-t", f"{i}: zcu106", "-e", f"docker attach {i}_xilinx-zcu106_1"])


def stop_qemu(instances=1, args=[]):
    """stop all docker services and cleanup resources"""
    docker_path = Path(REPO_ROOT, "docker")
    for i in range(instances):
        #subprocess.run(["docker-compose", "-p", str(i), "down"], cwd=docker_path)
        subprocess.run(["docker-compose", "-p", str(i), "down", "--volumes"], cwd=docker_path)
    for p in processes:
        print(f"Process {p.pid()} is being joined") #  Doesn't work if script is called from separate shell but could work if this is used as class?
        p.join()

if __name__ == "__main__":
    """main qemu launcher script"""
    mp.set_start_method('spawn')
    # main parser
    parser = argparse.ArgumentParser(description="qemu launcher")
    sp = parser.add_subparsers(title="subcommands", dest="cmd", required=True)
    # build subcommand
    parser_build = sp.add_parser("build", help="build qemu using docker build")
    parser_build.add_argument("--tag", default=QEMU_BUILDER_IMAGE, help="qemu docker builder image")
    parser_build.add_argument("--build-cache", default=QEMU_BUILD_CACHE_VOLUME, help="qemu build cache volume")
    parser_build.set_defaults(fn=build_qemu)
    # run subcommand
    parser_run = sp.add_parser("run", help="run qemu")
    parser_run.add_argument("--tag", default=QEMU_RUNNER_IMAGE, help="qemu docker runner image")
    parser_run.add_argument("-n", default=1, dest="instances", type=int, help="number of instances")
    parser_run.set_defaults(fn=run_qemu)
    # cleanup subcommand
    parser_run = sp.add_parser("stop", help="stop and cleanup all docker containers, volumes, etc")
    parser_run.add_argument("-n", default=1, dest="instances", type=int, help="number of instances")
    parser_run.set_defaults(fn=stop_qemu)

    # parse args
    script_args, cmd_args = parser.parse_known_args()

    # dispatch command function
    fn = script_args.fn
    kwargs = vars(script_args)
    for key in ["cmd", "fn"]:
        del kwargs[key]
    fn(**kwargs, args=cmd_args)

