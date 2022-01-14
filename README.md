# Xilinx Zynq UltraScale+ MPSoC ZCU106

This repository contains support for Xilinx ZCU106 development and running Xilinx QEMU in docker containers.
The `xilinx-qemu` submodule is a fork of the Xilinx QEMU repository (https://github.com/Xilinx/qemu). It was
forked to allow any code modifications, model development, etc. This repository uses the Xilinx QEMU code
directly and executes in QEMU rather than launching with the
[Xilinx PetaLinux](https://www.xilinx.com/products/design-tools/embedded-software/petalinux-sdk) tools.
PetaLinux provides a powerful high level development environment with full QEMU support but provides much more
functionality than is necessary for execution in docker, so it was decided for maximum flexibility to
simply run QEMU directly. For more information on Xilinx QEMU, see the
[QEMU User Documentation](https://xilinx-wiki.atlassian.net/wiki/spaces/A/pages/821395464/QEMU+User+Documentation).

## Development Environment

This repository includes support for generating an Ubuntu MATE 20.04 LTS virtual machine (VM) development
environment, which is the recommended workflow. [Vagrant](https://www.vagrantup.com) is used to generate the
virtual machine and execute the [Ansible](https://www.ansible.com) provisioner to setup the environment. The
following commands can be executed from the root repository directory to generate the virtual machine:

```sh
$ vagrant up
```

> **NOTE:** Ansible provisioning files are all located in the `ansible` directory

## ZCU106 Emulation

The QEMU ZCU106 emulation requires two instances of QEMU that communicate via shared memory:

* Main ARM emulation (aarch64)
* Platform Management Unit (PMU) (microblazeel)

Each of the QEMU instances are run in a separate docker container. The repository includes support for both
a QEMU build/development docker image and a lightweight runtime image. Docker compose is used to simplify
launching both docker containers as a single unit.

The main `scripts/qemu.py` launcher script was created to simplify building/running and simply wraps docker
and QEMU to hide the complexity from non power users. This script supports building the Xilinx QEMU code
and running the emulation. Run the following command to print help:

```sh
$ ./scripts/qemu.py -h
```

### Building

Prior to running the emulation, the Xilinx QEMU code must be built. The following commands will build QEMU
and prompt the user to build the development docker image if it doesn't exist. The script installs QEMU in
the `xilinx-qemu/build` directory if the user wishes to run directly on the host for development. The script
also uses a docker volume to cache the build directory so subsequent builds are incremental. The docker build
script sets up default configure flags to disable all unnecesary components to speed up building.

```sh
$ ./scripts/qemu.py build configure
$ ./scripts/qemu.py build make
```

> **NOTE:** It is only necessary to run the `configure` command once

> **NOTE:** Additional arguments to the `configure` and `make` commands will be forwarded to QEMU

### Running

In order to run, the user must first place all required images in the `zcu106/images` directory. These files
are currently kept separate from the repo due to the large size. The simplest way to get all of the required
images is to simply copy everything from the ZCU106 Board Support Package (BSP):

```sh
$ cp -r <ZCU106_BSP>/pre-built/linux/images/* <REPO_ROOT>/zcu106/images/
```

After building QEMU and installing the images, the emulation can be launched via the following command:

```sh
$ ./scripts/qemu.py run
```

This will start the docker container and open a terminal attached to the main container to allow the user
to interact with the guest OS.

Note that the `-n` flag can be used to start multiple instances of the board emulation.

In order to stop the emulation, the user must execute the following command to clean up all resources:

```sh
$ ./scripts/qemu.py clean
```

> **NOTE:** In order to properly cleanup the user must specify the same `-n` flag as used in the run command

