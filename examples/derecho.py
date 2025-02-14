"""
Generate a Spack site configuration for the Derecho HPC system.

This script creates YAML configuration files (`packages.yaml`, `compilers.yaml`,
`modules.yaml`, and `config.yaml`) that define the system-wide Spack settings
for Derecho.

Configuration includes:
- **MPI Provider:** Registers Cray MPICH 8.1.25 as the external MPI provider.
- **Packages:** Adds external, non-buildable definitions for:
    - `cray-mpich@8.1.25` with its required modules.
    - `parallel-netcdf@1.12.3` as an external installation.
    - `netcdf-c@4.9.2` with a fixed prefix.
    - `netcdf-fortran@4.6.1` with a fixed prefix.
    - `netcdf-cxx4@4.3.1` with a fixed prefix.
- **Compilers:** Registers GCC 12.2.0 with explicit paths, modules, and
  environment variables.
- **Modules:** Configures the Lmod module system with autoload rules, hidden
  implicits, and inclusion filters.
- **Build Settings:** Sets the number of parallel build jobs to 3.

⚠️ Note:
Derecho is a very complex Cray system, and its MPI setup is unconventional.
The `mpicc` and `mpifort` commands are not real compiler wrapper binaries but
bash scripts. These scripts intercept and adjust compiler flags before invoking
a private, internal MPI implementation that is not directly exposed. In
addition, Derecho uses a closed-source Cray libfabric driver, which complicates
portability. Because of these quirks, the generated YAML files will almost
certainly require manual edits to function properly. However, this script
produces a consistent, properly formatted set of YAMLs that serve as an
excellent starting point for building a Spack site configuration on Derecho.

Usage:
    Run this script to generate Spack site configuration files:

        python derecho.py
"""

from pathlib import Path
from spack_site_generator import Site

if __name__ == "__main__":
    # Create a site configuration object for Derecho
    site = Site(name="derecho")

    # -------------------------------------------------------------------------
    # MPI provider: Cray MPICH 8.1.25 (non-buildable external)
    # -------------------------------------------------------------------------
    site.packages.add_provider(
        provider_name="mpi",
        library_name="cray-mpich",
        library_version="8.1.25",
        buildable=False,
    )

    site.packages.add_package(
        name="cray-mpich",
        buildable=False,
        prefix="",
        spec="cray-mpich@8.1.25%gcc@12.2.0 +wrappers",
        modules=[
            "craype/2.7.20",
            "cray-mpich/8.1.25",
            "libfabric/1.15.2.0",
            "cray-pals/1.2.11",
        ],
        override=False,
    )

    # -------------------------------------------------------------------------
    # Parallel I/O and NetCDF stack (external installations)
    # -------------------------------------------------------------------------
    site.packages.add_package(
        name="parallel-netcdf",
        buildable=False,
        prefix="",
        spec="parallel-netcdf@1.12.3",
        modules=[
            "ncarenv/23.09",
            "gcc/12.2.0",
            "cray-mpich/8.1.25",
            "parallel-netcdf/1.12.3",
        ],
        override=False,
    )

    site.packages.add_package(
        name="netcdf-c",
        buildable=False,
        prefix="/glade/u/apps/derecho/23.09/spack/opt/spack/netcdf/4.9.2/packages/netcdf-c/4.9.2/gcc/12.2.0/3gy6",
        spec="netcdf-c@4.9.2",
        modules=["ncarenv/23.09", "gcc/12.2.0", "netcdf/4.9.2"],
        override=False,
    )

    site.packages.add_package(
        name="netcdf-fortran",
        buildable=False,
        prefix="/glade/u/apps/derecho/23.09/spack/opt/spack/netcdf/4.9.2/packages/netcdf-fortran/4.6.1/gcc/12.2.0/7czy",
        spec="netcdf-fortran@4.6.1",
        modules=["ncarenv/23.09", "gcc/12.2.0", "netcdf/4.9.2"],
        override=False,
    )

    site.packages.add_package(
        name="netcdf-cxx4",
        buildable=False,
        prefix="/glade/u/apps/derecho/23.09/spack/opt/spack/netcdf/4.9.2/packages/netcdf-cxx4/4.3.1/gcc/12.2.0/i4z2",
        spec="netcdf-cxx4@4.3.1",
        modules=["ncarenv/23.09", "gcc/12.2.0", "netcdf/4.9.2"],
        override=False,
    )

    # -------------------------------------------------------------------------
    # Compiler: GCC 12.2.0 (with Cray-provided paths and modules)
    # -------------------------------------------------------------------------
    site.compilers.add_compiler(
        spec="gcc@12.2.0",
        paths={
            "cc": "/opt/cray/pe/gcc/12.2.0/bin/gcc",
            "cxx": "/opt/cray/pe/gcc/12.2.0/bin/g++",
            "f77": "/opt/cray/pe/gcc/12.2.0/bin/gfortran",
            "fc": "/opt/cray/pe/gcc/12.2.0/bin/gfortran",
        },
        operating_system="sles15",
        target="x86_64",
        modules=["ncarenv/23.09", "gcc/12.2.0"],
        flags={},
        environment={"set": {"FI_CXI_RX_MATCH_MODE": "hybrid"}},
        extra_rpaths=[],
    )

    # -------------------------------------------------------------------------
    # Module system: Lmod configuration
    # -------------------------------------------------------------------------
    site.modules.add_module_type(
        module_type="lmod",
        autoload="run",
        hide_implicits=True,
        hash_length=8,
        include=["cray-mpich", "python"],
        exclude=[],
    )

    # -------------------------------------------------------------------------
    # Build settings
    # -------------------------------------------------------------------------
    site.config.set_build_jobs(build_jobs=3)

    # -------------------------------------------------------------------------
    # Write generated YAML files to current directory
    # -------------------------------------------------------------------------
    site.write(path=Path.cwd())
