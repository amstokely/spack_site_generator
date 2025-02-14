# Spack Site Generator

**spack_site_generator** is a Python package that automates the creation of
**site-specific YAML configuration files** for
[Spack](https://spack.readthedocs.io/). It simplifies defining **compilers,
package preferences, module settings, and global configurations**, ensuring
consistency across installations.

## Features

- **Compilers:** Define compiler versions, paths, and associated modules.
- **Packages:** Configure package providers, external installations, and
  build options.
- **Modules:** Customize module system settings for Lmod or Tcl.
- **Global Configuration:** Set build jobs, cache paths, and stage directories.
- **Automatic YAML Generation:** Write site configuration files in Spack’s
  expected format.

---

## HPC Environments

Every HPC system is unique, and Spack needs to account for site-specific
quirks such as wrapper compiler scripts, custom MPI implementations, or
proprietary drivers. Because of this, the generated YAML configuration files
may not work perfectly out of the box on all machines. However, they serve
as a strong starting point and typically remove about 90% of the boilerplate
needed when setting up Spack on complex HPC systems.

---

## Installation

Clone this repository and install the package:

```sh
git clone https://github.com/amstokely/spack_site_generator.git
cd spack_site_generator
pip install .
```

---

## Usage

See the [examples directory](examples) for detailed usage examples.
