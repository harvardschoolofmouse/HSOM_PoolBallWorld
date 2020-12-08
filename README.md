# Harvard School of Mouse: Pool Ball World 
*(HSOM_PoolBallWorld)* Contains PyJulia, Julia, Gen, Python and Pygame dependencies for Pool Ball World


# Getting started
This repo is built on Julia 1.5.3 and Python 3.7.3 in a Conda virtual environment and validated on Mac OS 10.14 Mojave (MacBook Pro 2018). Process:

1. I followed the instructions here to install the latest stable build of Julia and Anaconda Navigator on 12/8/2020:
https://datatofish.com/add-julia-to-jupyter/

NB: When installing on Windows 7, additional steps (downloading Powershell 3 and running `Pkg.build("IJulia")` were necessary to get Julia kernel into Jupyter-Notebook.

2. I created a conda virtual environment in Bash using the following:

  `$ conda create -n gaming_environment python=3.7.3 anaconda`

  The virtual environment will keep code versions for this project isolated from the rest of the system. It has installed the Anaconda default libraries for python 3.7.3.

3. Next, activate the virtual environment

  `$ conda activate gaming_environment`

 You should see the Bash prompt change from:

  `(Base) Your-Computer:~`

 to

  `(gaming_environment) Your-Computer:~ User$`

 We will need to enter the virtual environment to run the programs in the Repo.


### Within the virtual environment: 

4. Install pygame. The -U tag will update to the latest versions:

  `$ python3 -m pip install -U pygame`

 I've read a lot of nightmare stories about this potentially not working. Run the example to test that all went well:

  `$ python3 -m pygame.examples.aliens`

5. Install PyJulia so that python and julia language can be run from the same jupyter-notebook kernel. This is done from within python.
(This page is helpful: https://pyjulia.readthedocs.io/en/latest/usage.html)

  `$ python`
  `>>> import julia`
  `>>> julia.install()`

 For me, this was not sufficient due to the Conda environment. When running in jupyter-notebook, I had to additionally add a code block at the top to import Julia to the notebook:

  `from julia.api import Julia
  jl = Julia(compiled_modules=False)`

6. Finally, we need to make a kernel for Jupyter-Notebook for our virtual environment. 

  `ipython kernel install --user --name gaming-environment --display-name "Python Gaming Environment"`

 This article was helpful for installing the `gaming-environment` virtual environment kernel in Jupyter-Notebook:
  https://support.esri.com/en/technical-article/000019210


### Running Jupyter-Notebook from the virtual environment:

Simply enter the virtual environment from Bash and enter the command

  `jupyter-notebook`
  
 to begin a session. You can then open the existing .ipynb files or create a new one with the virtual environment kernerl.


# Getting started with Pygame

I found this tutorial helpful:
https://www.youtube.com/watch?v=cJbnWZGX-XY&list=PL9ooVrP1hQOHY-BeYrKHDrHKphsJOyRyu&index=62


