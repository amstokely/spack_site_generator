"""
This script generates YAML configuration files for Spack site configuration.
It defines packages, compilers, and module settings and writes them to
`packages.yaml`, `compilers.yaml`, and `modules.yaml`.

Modules:
    - `Packages`: Manages package configurations, including providers and build options.
    - `Compilers`: Defines compiler configurations, including paths and environment variables.
    - `Modules`: Configures module system settings.

Usage:
    Run the script directly to generate the configuration files:
    ```
    python basic.py
    ```
"""

from pathlib import Path

from spack_site_generator import Site

if __name__ == "__main__":

    site = Site(name="basic")

    # Define MPI provider
    site.packages.add_provider(
        provider_name="mpi",
        library_name="openmpi",
        library_version="5.0.5",
        buildable=False,
    )

    # Add compiler to package configuration
    site.packages.add_compiler(name="gcc", version="11.4.0")

    # Define OpenMPI package configuration
    site.packages.add_package(
        name="openmpi",
        spec="openmpi@5.0.5",
        buildable=False,
        prefix="/home/astokely/software/spack-stack/spack/opt/spack"
        "/linux-ubuntu22.04-skylake/gcc-11.4.0/openmpi-5.0.5-zaxpym3yhy72maxfltpgkwl7mpxztpjn",
        modules=["openmpi/5.0.5"],
        override=False,
    )

    # Add GCC compiler configuration
    site.compilers.add_compiler(
        spec="gcc@11.4.0",
        paths={
            "cc": "/usr/bin/gcc",
            "cxx": "/usr/bin/g++",
            "f77": "/usr/bin/gfortran",
            "fc": "/usr/bin/gfortran",
        },
        operating_system="ubuntu22.04",
        target="x86_64",
        flags={},
        modules=[],
        environment={},
        extra_rpaths=[],
    )

    # Configure Lmod module system
    site.modules.add_module_type(
        module_type="lmod", autoload="run", hash_length=0,
        hide_implicits=True,
        include=[], exclude=[],
    )

    site.write(
        path=Path.cwd(),
    )
