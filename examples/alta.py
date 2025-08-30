"""
Example: Generating a Spack site configuration for a Linux desktop ("alta")

This example shows how to configure a simple desktop system with GCC 11.4.0
and OpenMPI 5.0.5. The `extra_attributes` block is required because the fftw
recipe expected the `openmpi` package to expose a `headers` property, which
is no longer defined for OpenMPI v5+ in Spack. This highlights the value of
using spack_site_generator: instead of hand-editing YAML files to patch in
missing attributes, you can describe the site once in Python and auto-generate
the configuration.
"""

from pathlib import Path
from spack_site_generator import Site

if __name__ == "__main__":

    # Create a site configuration object for a Linux desktop ("alta")
    site = Site(name="alta")

    # Define MPI provider (OpenMPI 5.0.5, external system install)
    site.packages.add_provider(
        provider_name="mpi",
        library_name="openmpi",
        library_version="5.0.5",
        buildable=False,
    )

    # Add GCC 11.4.0 as a compiler option
    site.packages.add_compiler(name="gcc", version="11.4.0")

    # Define OpenMPI package configuration
    # NOTE: extra_attributes is required here because the fftw recipe
    # expected `openmpi` to provide a `headers` property, which is no
    # longer defined for OpenMPI v5+ in Spack. This illustrates why a
    # Python library like spack_site_generator is useful—it automates
    # these YAML tweaks instead of forcing manual edits.
    site.packages.add_package(
        name="openmpi",
        buildable=False,
        spec="openmpi@5.0.5%gcc@11.4.0",
        prefix="/home/astokely/software/spack-stack/spack/opt/spack/linux-ubuntu22.04-skylake/gcc-11.4.0/openmpi-5.0.5-zaxpym3yhy72maxfltpgkwl7mpxztpjn",
        modules=["openmpi/5.0.5"],
        extra_attributes={
            "headers": "/home/astokely/software/spack-stack/spack/opt/spack/linux-ubuntu22.04-skylake/gcc-11.4.0/openmpi-5.0.5-zaxpym3yhy72maxfltpgkwl7mpxztpjn/include",
            "libs": "/home/astokely/software/spack-stack/spack/opt/spack/linux-ubuntu22.04-skylake/gcc-11.4.0/openmpi-5.0.5-zaxpym3yhy72maxfltpgkwl7mpxztpjn/lib/libmpi.so",
        },
        override=False,
    )

    # Define GCC 11.4.0 compiler configuration
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
        modules=[],
        flags={},
        environment={},
        extra_rpaths=[],
    )

    # Configure Lmod module system
    site.modules.add_module_type(
        module_type="lmod",
        autoload="run",
        hash_length=0,
        hide_implicits=True,
        include=["python", "openmpi"],
        exclude=[],
    )

    # Set the number of parallel build jobs
    site.config.set_build_jobs(build_jobs=8)

    # Write the generated Spack configuration files to the current directory
    site.write(path=Path.cwd())
