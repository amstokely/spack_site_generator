# Spack Site Generator

**spack_site_generator** is a Python package that automates the creation of **site-specific YAML configuration files** for [Spack](https://spack.readthedocs.io/). It simplifies defining **compilers, package preferences, module settings, and global configurations**, ensuring consistency across installations.

## Features

- **Compilers:** Define compiler versions, paths, and associated modules.
- **Packages:** Configure package providers, external installations, and build options.
- **Modules:** Customize module system settings for Lmod or Tcl.
- **Global Configuration:** Set build jobs, cache paths, and stage directories.
- **Automatic YAML Generation:** Write site configuration files in Spack’s expected format.

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
See the [examples](examples/) directory for detailed usage examples.

---
