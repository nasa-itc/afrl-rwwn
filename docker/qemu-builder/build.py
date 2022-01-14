#!/usr/bin/env python3

import sys
import shutil
import argparse
import subprocess
from pathlib import Path

QEMU_ROOT = Path("/qemu")
QEMU_SOURCE_DIR = Path(QEMU_ROOT, "src/xilinx-qemu")
QEMU_BUILD_DIR = Path(QEMU_ROOT, "build")
QEMU_INSTALL_DIR = Path(QEMU_SOURCE_DIR, "build")

def clean_dir(path):
    """clean directory"""
    if path.exists():
        # remove all files and subdirectories
        for item in path.iterdir():
            if item.is_file() or item.is_symlink():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
    else:
        # create directory
        path.mkdir()

def update_ownership(path, refpath=QEMU_SOURCE_DIR):
    """update path ownership to match reference path"""
    stat = refpath.stat()
    shutil.chown(path, user=stat.st_uid, group=stat.st_gid)
    for item in path.glob("**/*"):
        shutil.chown(item, user=stat.st_uid, group=stat.st_gid)

def run_qemu_configure(*args):
    """run qemu configure script"""
    # default qemu configure args for lightweight build
    default_args = (f"--prefix={QEMU_INSTALL_DIR}",
                    "--target-list=aarch64-softmmu,microblazeel-softmmu",
                    "--disable-blobs",
                    "--enable-plugins",
                    "--disable-docs",
                    "--enable-guest-agent",
                    "--enable-modules",
                    "--disable-gnutls",
                    "--disable-nettle",
                    "--enable-gcrypt",
                    "--disable-auth-pam",
                    "--disable-sdl",
                    "--disable-gtk",
                    "--disable-curses",
                    "--disable-vnc",
                    "--disable-cocoa",
                    "--disable-virtfs",
                    "--disable-xen",
                    "--disable-brlapi",
                    "--disable-curl",
                    "--enable-fdt",
                    "--disable-kvm",
                    "--disable-hax",
                    "--disable-hvf",
                    "--disable-whpx",
                    "--disable-rdma",
                    "--disable-pvrdma",
                    "--disable-spice",
                    "--disable-smartcard",
                    "--disable-tpm",
                    "--enable-tools",
                    "--disable-bochs",
                    "--disable-cloop",
                    "--disable-dmg",
                    "--disable-qcow1",
                    "--disable-vdi",
                    "--disable-vvfat",
                    "--disable-qed",
                    "--disable-parallels",
                    "--disable-sheepdog")

    # clean build/install directories
    clean_dir(QEMU_BUILD_DIR)
    clean_dir(QEMU_INSTALL_DIR)

    # update ownership on install directory to match source directory
    update_ownership(QEMU_INSTALL_DIR)

    # run configure script
    configure_path = str(QEMU_SOURCE_DIR / "configure")
    cmd = (configure_path,) + default_args + args
    subprocess.run(cmd, cwd=QEMU_BUILD_DIR)

def run_qemu_make(*args):
    """run make in qemu build directory"""
    # default args if none specified
    if not args:
        args = ("-j4",
                "install")

    # clean install directory
    clean_dir(QEMU_INSTALL_DIR)

    # run make
    cmd = ("make",) + args
    subprocess.run(cmd, cwd=QEMU_BUILD_DIR)

    # update ownership on install directory to match source directory
    update_ownership(QEMU_INSTALL_DIR)

if __name__ == "__main__":
    """qemu builder script"""
    # qemu builder subcommands to function map
    cmds = {"configure": run_qemu_configure,
            "make": run_qemu_make}
    # parse command line
    parser = argparse.ArgumentParser(description="qemu builder")
    parser.add_argument("cmd", choices=cmds, help="qemu build command")
    parser.add_argument("args", nargs=argparse.REMAINDER, help=argparse.SUPPRESS)
    args = parser.parse_args()

    # dispatch build command
    cmds[args.cmd](*args.args)


