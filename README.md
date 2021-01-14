# Harvard School of Mouse: Pool Ball World 
*(HSOM_PoolBallWorld)* Contains PyJulia, Julia, Gen, Python and Pygame dependencies for Pool Ball World


# Getting started
This repo is built on Julia 1.5.3 and Python 3.7.3 in a Conda virtual environment and validated on Mac OS 10.14 Mojave (MacBook Pro 2018). Process:

1. I followed the instructions here to install the latest stable build of Julia and Anaconda Navigator on 12/8/2020:
https://datatofish.com/add-julia-to-jupyter/

NB: When installing on Windows 7, additional steps (downloading Powershell 3 and running `Pkg.build("IJulia")` were necessary to get Julia kernel into Jupyter-Notebook.

2. I created a conda virtual environment in Bash using the following:

  `$ conda create -n gaming_environment python=3.7.3 anaconda`

  The virtual environment will keep code versions for this project isolated from the rest of the system. It has installed the Anaconda default libraries for python 3.7.3. This page was useful: https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/#:~:text=A%20virtual%20environment%20is%20a,without%20affecting%20other%20Python%20projects.

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
  
  If using virtual env:
  `$ python3 -m pip install julia`
  
  Else:
  `$ python3 -m pip install --user julia`

  Then:
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


It turns out Pygame does not have a physics engine! (as I learned after many hours of fussing) You will also need Pymunk for the elastic collisions to work properly

#### Installing Pymunk

This site has useful docs:
https://docs.conda.io/projects/conda/en/latest/commands/install.html

1. Enter the virtual environment (or install directly to the environment with `-n gaming_environment`) and conda install pymunk

`$ conda install -c conda-forge -n gaming_environment pymunk`


# Possible errors

I have run into some errors trying to get julia to align with the anaconda virtual environment's python version. There's some snaffu getting PyCall, PyJulia and Conda to interact properly. You may see:

`using PyPlot
INTEL MKL ERROR: dlopen(/opt/anaconda3/lib/libmkl_intel_thread.dylib, 9): Library not loaded: @rpath/libiomp5.dylib
  Referenced from: /opt/anaconda3/lib/libmkl_intel_thread.dylib
  Reason: image not found.
Intel MKL FATAL ERROR: Cannot load libmkl_intel_thread.dylib.`

If so, you can solve this by putting the path to the desired python file as the desired environment. 

`julia> ENV["PYTHON"] = /pathtopython...`

Or, to fix and revert to the original julia in-built python version, you can use

`julia> ENV["PYTHON"] = ""`

You then need to rebuild PyCall:

`julia> using Pkg
... Pkg.build("PyCall")`

And then quit julia, python etc and restart the terminal/notebook kernel. If it doesn't work at first, close everything and try again.



# Working files

The Pool Ball World simulation can be run visually from `pool_ball_world_physics_visual.py`
The light version (no visualization, just simulation): `pool_ball_world_physics_engine.py`

Follow along with Generative model validation and testing in the *.ipynb's!


