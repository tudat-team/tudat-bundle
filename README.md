
[![Build Status](https://img.shields.io/travis/tudat-team/tudat-bundle/master.svg?logo=travis&style=for-the-badge)](https://travis-ci.org/tudat-team/tudat-bundle)
[![Build Status](https://img.shields.io/circleci/project/github/team-tudat/tudat-bundle/master.svg?style=for-the-badge&logo=circleci)](https://circleci.com/gh/team-tudat/tudat-bundle)



The Tudat bundle contains Tudat and a number of external libraries in a modular fashion. The TU Delft Astrodynamics Toolbox (Tudat) is a set of C++ software libraries for simulating various astrodynamics applications, for more info see [the Tudat website](http://tudat.tudelft.nl).

## Instructions
This document contains minimal information on how to build the Tudat bundle. For more information see documentation below.

### Building the project

1. Clone the repository on your computer (or fork and then clone)

        git clone https://github.com/tudat/tudatBundle.git

2. Enter the new directory

        cd tudatBundle

3. Checkout all the submodules (optionally you can clone only the necessary submodules)

        git submodule update --init --recursive

4. Make a new build directory and enter

        mkdir build && cd build

5. Initiate CMake for the project

        cmake ../

6. Build the project

        make

Note: it can happen that due to dependencies between the submodules the ```make``` process quits with an error (after building SPICE, for instance). In this case, please repeat steps 5 and 6 once or twice.

<a name="switching_apps">
### Switching on/off libraries and applications
</a>

By default only the SPICE library is build. You can enable/disable which libraries are build by manipulating special use switches:

1. Each library has such a switch, these are: ```USE_CSPICE```, ```USE_NRLMSISE```, ```USE_PAGMO```.

2. You can turn on or off such a switch as an argument to CMake. For instance, the following will disable SPICE, but enable the nrlmsise-00 atmopshere model:

        cmake ../ -DUSE_CSPICE=0 -DUSE_NRLMSISE=1

Detailed control and to specification of detailed build options for external libraries (like building of examples and tests) can be achieved by editing ```CMakeLists.txt```.

### Creating your own applications

1. Copy the ```templateApplication``` from ```tudatExampleApplications``` to tudatApplications and give it your own name:

        cp -R tudatExampleApplications/templateApplication tudatApplications/myApplication
        cd tudatApplications/myApplication
        mv TemplateApplication MyApplication

2. Add your project to the top-level ```CMakeLists.txt```, like so:

        add_subdirectory("${PROJECTROOT}/tudatApplications/myApplication/MyApplication")

3. Re-run cmake and make commands.

## Documentation

* [Tudat wiki](http://tudat.tudelft.nl/projects/tudat/wiki)

* [Doxygen](http://tudat.tudelft.nl/Doxygen/Tudat/docs/index.html)


## Development notes

* [Git Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)

* [IDE for Development](https://www.jetbrains.com/clion/)
