"""
Generate a Spack site configuration for the Casper HPC system.

This script creates YAML configuration files (`packages.yaml`, `compilers.yaml`,
`modules.yaml`, and `config.yaml`) that define the system-wide Spack settings for Casper.

Configuration includes:
- **Compilers:** Registers GCC 12.2.0 with its system paths and associated modules.
- **Packages:**
  - Defines OpenMPI 4.1.6 as an external MPI provider.
  - Specifies external installations for `autoconf` and `ecflow`.
- **Modules:** Configures Lmod with specific autoload rules and exclusions.
- **Build Settings:** Sets the number of parallel build jobs.

Usage:
    Run this script to generate Spack site configuration files:
    ```
    python casper.py
    ```
"""

from pathlib import Path
from spack_site_generator import Site

if __name__ == "__main__":

    # Create a site configuration object for Casper
    site = Site(name="casper")

    # Define MPI provider (OpenMPI 4.1.6)
    site.packages.add_provider(
        provider_name="mpi",
        library_name="openmpi",
        library_version="4.1.6",
        buildable=False,  # Mark as an external, non-buildable package
    )

    # Add GCC 12.2.0 as a compiler option
    site.packages.add_compiler(name="gcc", version="12.2.0")

    # Define OpenMPI package configuration
    site.packages.add_package(
        name="openmpi",
        buildable=False,  # External package, not built by Spack
        spec="openmpi@4.1.6%gcc@12.2.0+cuda~cxx~cxx_exceptions~java+lustre~memchecker+pmi+static~wrapper-rpath fabrics=ucx schedulers=tm",
        prefix="/glade/u/apps/casper/23.10/spack/opt/spack/openmpi/4.1.6/gcc/12.2.0/yia4",  # Installation path
        modules=["openmpi/4.1.6", "ucx/1.14.1", "cuda/12.2.0"],  # Associated modules
        override=False,
    )

    # Add Autoconf as a buildable package with a predefined installation path
    site.packages.add_package(
        name="autoconf",
        buildable=True,  # Spack will build this package
        spec="autoconf@2.71",
        prefix="/glade/u/apps/casper/23.10/opt/view",
        modules=[],
        override=False,
    )

    # Add EcFlow as an external package with a specific installation path
    site.packages.add_package(
        name="ecflow",
        buildable=False,  # External package, not built by Spack
        spec="ecflow@5.8.4+ui+static_boost",
        prefix="/glade/work/epicufsrt/contrib/spack-stack/casper/ecflow-5.8.4",  # Installation path
        modules=["ecflow/5.8.4"],  # Associated module
        override=True,  # Ensure this package setting overrides others
    )

    # Define GCC 12.2.0 compiler configuration
    site.compilers.add_compiler(
        spec="gcc@12.2.0",
        paths={
            "cc": "/glade/u/apps/casper/23.10/spack/opt/spack/gcc/12.2.0/pucl/bin/gcc",
            "cxx": "/glade/u/apps/casper/23.10/spack/opt/spack/gcc/12.2.0/pucl/bin/g++",
            "f77": "/glade/u/apps/casper/23.10/spack/opt/spack/gcc/12.2.0/pucl/bin/gfortran",
            "fc": "/glade/u/apps/casper/23.10/spack/opt/spack/gcc/12.2.0/pucl/bin/gfortran",
        },
        operating_system="opensuse15",
        target="x86_64",
        modules=["gcc/12.2.0"],  # Load module before use
        flags={},
        environment={},
        extra_rpaths=[],
    )

    # Configure Lmod module system
    site.modules.add_module_type(
        module_type="lmod",
        autoload="run",  # Automatically load modules when dependent packages are loaded
        hash_length=0,  # Do not append hash to module names
        hide_implicits=True,  # Hide implicit dependencies from module list
        include=["python"],  # Only include certain modules
        exclude=["ecflow"],  # Exclude specific modules from being auto-loaded
    )

    # Set the number of parallel build jobs
    site.config.set_build_jobs(build_jobs=4)

    # Write the generated Spack configuration files to the current directory
    site.write(path=Path.cwd())
