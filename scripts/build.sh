#!/usr/bin/bash

docker run -it -v $(pwd):/tmp/host -u $(id -u) -w /tmp/host/ --entrypoint /bin/bash node:14 -c ./scripts/bundle.sh
