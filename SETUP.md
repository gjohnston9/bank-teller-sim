* Download Miniconda installation script: `curl -o conda_install.sh https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh`
* Install: `bash conda_install.sh`
* Follow installation instructions.
* Create a Python 2 environment with scipy, matplotlib, and pytest: `~/miniconda2/bin/conda create -y -n scipy_env scipy matplotlib pytest python=2.7`
* Start using this environment `source ~/miniconda2/bin/activate scipy_env`
* Go to my project's folder: `cd bank-teller-sim`
* Run the simulation: `python bank_sim.py 0.75 2`
* To run tests: `python -m pytest` (Pytest will automatically look in tests/ directory and run `test_engine.py` and `test_simulation.py`)
* When you're done: `source ~/miniconda2/bin/deactivate` to stop using `scipy_env` and revert to your system's Python installation.