# svs-polygon-cropping
A plugin that supports .svs images and allows cropping polygonal segments out in .dzi format. 

## Required
Make sure your system has the following installed: <br>
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Conda](https://docs.conda.io/en/latest/miniconda.html)

## Setup
1. Git clone the repository. Open terminal on your system and type <br>
``` git clone https://github.com/czbiohub/svs-polygon-cropping.git ```
2. Go into the cloned directory and create a conda environment <br> ``` conda env create -f environment.yml ```
3. Activate the created conda environment. This environment contains all the dependencies required to run the code <br>``` conda activate svs-polygon-cropping ```
4. Register the napari plugin by running setup.py like so <br> ``` pip install -e . ```
5. Finally launch the napari app from command line <br> ``` napari  ```

## Usage
The gif below illustrates how to 
- activate the plugin using the `Plugin` option in the top menu bar  
- open an svs image by drag and drop  
- Create a shapes layer to start drawing the boundary around tissue of interest
- name and crop the area inside the boundary out into a .dzi file stored in a folder called he_crops located in the same folder as the input .svs image
- crop out more than one tissue by first deleting the first shape and then drawing another
 ![Alt Text](https://github.com/czbiohub/svs-polygon-cropping/blob/main/tabula.gif)
 
 ## Contact
 For any issues or feature requests reach out to [Snigdha Agarwal](snigdhaagarwal93@gmail.com)
