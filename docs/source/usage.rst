Usage
=====

.. _installation:

Installation
------------

To use self-righting-boat, first install it using git:

.. code-block:: console

 git clone git@github.com:Azmadax/self-righting-boat.git
To install the required dependencies, follow the steps below:

1. Install `uv` by following the official [installation guide](https://docs.astral.sh/uv/getting-started/installation).
2. Alternatively, run the command from root of repository:
   ```bash
   cd self-righting-boat
   make install-uv

Launching demo
----------------

To launch an example, run the following command from root of repository:
```bash
uv sync --package hydrostatic
uv run hydrostatic_2d_example.py
```
Alternatively, if you have make install, just run:
```bash
make demo
```

