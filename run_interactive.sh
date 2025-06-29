#!/bin/bash

docker run -it --rm --volume $(pwd)/policy.kafel:/policy.kafel --volume $(pwd)/sandbox.cfg:/sandbox.cfg --volume $(pwd)/examples:/examples --volume $(pwd)/data:/data --name nsjail playground