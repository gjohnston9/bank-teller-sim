# Bank Teller Simulation

## Setting up
* You will need Python 2 with the `scipy` library installed. If you want to generate plots of simulation output (using the `--generate_plots` flag), you'll need `matplotlib`. If you want to run tests, you'll need `pytest` (and `matplotlib` since the tests generate pdf plots). If you don't have the necessary libraries already, you can follow these instructions:
* Download Miniconda installation script: `curl -o conda_install.sh https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh`
* Install: `bash conda_install.sh` and follow installation instructions.
* Create a Python 2 environment with scipy, matplotlib, and pytest: `~/miniconda2/bin/conda create -y -n scipy_env scipy matplotlib pytest python=2.7`
* Start using this environment: `source ~/miniconda2/bin/activate scipy_env`
* Go to my project's folder: `cd bank-teller-sim`
* Refer to **Running the program** section for info on running the simulation.
* When you're done: `source ~/miniconda2/bin/deactivate` to stop using `scipy_env` and revert to your original Python installation.

## Running the program
* To run with a lunch break length of 0.75 with 2 tellers: `python bank_sim.py 0.75 2 --verbose` (and `--generate_plots` if you'd like to see plots as well)
* Run `bash run_all.sh` to run the simulation with each combination of parameters that was examined for this project.

## Running tests
* Run `python -m pytest` from the root directory of this project. Pytest will automatically look in `tests/` directory and run the tests there (requires `matplotlib` and `pytest` libraries).
* Plots generated by the tests will be saved to the `test_output/` directory.

## Output description
* The `sim_output/` directory has two subdirectories: `plots` and `statistics`.
* Each has information about two measures: the number of customers in line, and the customer waiting times.

### Text output
* Each text file contains the mean, median, and standard deviation for a measure.

### Plot output
* The two red rectangles represent the two rush periods (where the first rush period is also the lunch period for the tellers)
* Each blue rectangle represents the time when a teller was on their lunch break.
