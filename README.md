# Bank Teller Simulation

## Setting up
* You will need Python 2 with `scipy` and `matplotlib` packages installed. If you want to run tests, you'll need `pytest` as well. If you don't have the necessary packages already, you can follow these instructions:
* If you've previously tried and failed to install Miniconda, remove it with `rm -rf ~/miniconda2`, and remove any lines in your `.bashrc` that were added by the Miniconda installation (open it with `nano ~/.bashrc`).
* Download Miniconda installation script: `curl -o conda_install.sh https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh`
* Install: `bash conda_install.sh` and follow installation instructions. When you're prompted to add `conda` to your path, say yes.
* Apparently Miniconda won't be correctly set up at this point. Run `source ~/.bashrc` so that the `conda` command will be recognized. However when you get to the `conda activate scipy_env` step below you may get a warning that your shell is not configured correctly. When that happens, follow the instructions given to you there, and then run `source ~/.bashrc` again.
* The instructions I mentioned above may be to run this command `echo ". /root/miniconda2/etc/profile.d/conda.sh" >> ~/.bashrc` and then manually remove the line `export PATH="/root/miniconda2/bin:$PATH"` that was already in your `.bashrc`.
* Create a Python 2 environment with scipy, matplotlib, and pytest: `conda create -y -n scipy_env scipy matplotlib pytest python=2.7`
* Start using this environment: `conda activate scipy_env`
* Go to my project's folder.
* Refer to the **Running the simulation/tests** sections for info on how to use my project.
* When you're done: `conda deactivate` to stop using `scipy_env` and revert to your original Python installation.

## Running the simulation
* To run with a lunch break length of 0.75 with 2 tellers: `python bank_sim.py 0.75 2 --verbose` (and `--generate_plots` if you'd like to see plots as well)
* Run `bash run_all.sh` to run the simulation with each combination of parameters that was examined for this project.

## Running tests
* Run `python -m pytest` from the root directory of my project. Pytest will automatically look in `tests/` directory and run the tests there (requires `pytest` package).
* Plots generated by the tests will be saved to the `test_output/` directory.

## Output description
* The `sim_output/` directory has two subdirectories: `plots` and `statistics`.
* Each has information about two measures: the number of customers in line, and the customer waiting times.

### Text output
* Each text file contains the mean, median, and standard deviation for a measure.

### Plot output
* The two red rectangles represent the two rush periods (where the first rush period is also the lunch period for the tellers)
* Each blue rectangle represents the time when a teller was on their lunch break.
