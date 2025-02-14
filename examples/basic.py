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

from spack_site_generator import Modules
from spack_site_generator import Packages
from spack_site_generator import Compilers

if __name__ == "__main__":
    # Initialize package configuration
    packages = Packages()

    # Define MPI provider
    packages.add_provider(
        provider_name="mpi",
        library_name="openmpi",
        library_version="5.0.5",
        buildable=False,
    )

    # Add compiler to package configuration
    packages.add_compiler(name="gcc", version="11.4.0")

    # Define OpenMPI package configuration
    packages.add_package(
        name="openmpi",
        spec="openmpi@5.0.5",
        buildable=False,
        prefix="/home/astokely/software/spack-stack/spack/opt/spack"
               "/linux-ubuntu22.04-skylake/gcc-11.4.0/openmpi-5.0.5-zaxpym3yhy72maxfltpgkwl7mpxztpjn",
        modules=["openmpi/5.0.5"],
    )

    # Write package configuration to file
    packages.write(filename="packages.yaml")

    # Initialize compiler configuration
    compilers = Compilers()

    # Add GCC compiler configuration
    compilers.add_compiler(
        spec="gcc@11.4.0",
        paths={
            "cc": "/usr/bin/gcc",
            "cxx": "/usr/bin/g++",
            "f77": "/usr/bin/gfortran",
            "fc": "/usr/bin/gfortran"
        },
        operating_system="ubuntu22.04",
        target="x86_64",
        flags={},
        modules=[],
        environment={},
        extra_rpaths=[]
    )

    # Write compiler configuration to file
    compilers.write(filename="compilers.yaml")

    # Initialize module configuration
    modules = Modules()

    # Configure Lmod module system
    modules.add_module_type(
        module_type="lmod",
        autoload="run",
        hash_length=0,
        hide_implicits=True
    )

    # Write module configuration to file
    modules.write(filename="modules.yaml")
