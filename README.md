# Bus Stops Finder

## Description
Python algorithm to derive bus stop locations from crowdsourced geolocalized data.
The extracted bus stops are then viewable on a webGIS.

## Requirements
+ Python 2.7
+ pip
+ virtualenv (*recommended*)
* Node.js (and npm)

## Setup and Usage

**IMPORTANT**: Execute the following commands in the root folder of the project.

1. Create python virtual environment with `virtualenv .env`
2. Activate the virtual env with `.env\Scripts\activate` on Windows or `source .env/bin/activate` on Linux
3. Install all the required python dependencies with `pip install -r requirements_win.txt`on windows or  `pip install -r requirements_linux.txt`on linux [^requirements]
4. Run the Bus Stops Finder algorithm with `python main.py`
5. Follow the on-screen logging, until the proccess ends
6. Move to "website" folder with `cd website`
7. Install node dependencies, by executing `npm install`
8. Once npm has finished, start the node server with `node nodeServer.js`
9. Open [http:\\\\127.0.0.1:8080](http:\\127.0.0.1:8080) on your browser

[^requirements]:
Some dependencies in the requirements.txt might not be automatically resolved by pip.
In this case, it is needed to manually install them, following the module specific documentations.
For Windows, it is possible to download already built binaries from here [Unofficial Windows Binaries for Python Extension Packages](http://www.lfd.uci.edu/~gohlke/pythonlibs)
and then install them with `pip install path\to\the\package.whl` 
For Linux, a ready to install python dependency packages should be available in the distro repositories.


## Development and Testing

To prepare the development environment, just follow the first 3 steps of the [Setup and Usage](#setup-and-usage) paragraph.

For testing the project, activate your virtual env ( second step of [Setup and Usage](#setup-and-usage)) and then run the following:

> python -m unittest discover

## Credits
[OpenStreetMap](https://www.openstreetmap.org) for the webGIS base map and Bus stops and stations data.

[Overpass-Turbo](https://overpass-turbo.eu/) for the bus data export from OSM.
