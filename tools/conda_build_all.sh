#!/bin/bash

cd ../

conda-build cspice/tools/conda.build

conda-build sofa/tools/conda.build

conda-build tudat/tools/conda.build

conda-build tudatpy/tools/conda.build

