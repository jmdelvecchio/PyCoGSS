The `utils` directory holds executable Python files (`.py`) that when executed bring up dialog boxes for you to click to select the folders you want to grab things from.

Right now it makes jpegs or merges Planet strips from all the `.tif` files in a directory, so don't mix and match scenes or kinds of imagery (e.g. RGB and NDVI).

Right now the merged Planet strips are named after the date of the imagery plus a random number tacked on in case we get imagery from the same date. Also right now, the Planet tile size is hard-coded to 1024 pixels. I want to have user input change that. 