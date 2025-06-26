#!/bin/bash

docker run -it --rm --volume $(pwd)/sandbox.cfg:/sandbox.cfg --volume $(pwd)/examples:/examples --name nsjail nsjail