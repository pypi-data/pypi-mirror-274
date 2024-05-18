#!/bin/sh

set -eu

PREFIX=${PREFIX:-py3}

if [[ -z "${NAME}" ]]; then
    echo "NAME variable must be set!"
    exit 1
fi

if [ $(uname -s) = "Darwin" ]; then
    LC_ALL=C find . -type f ! -name init.sh -exec sed -i '' "s/blank[_\-]project/${NAME}/g" {} +
else
    find . -type f ! -name init.sh -exec sed -i 's/blank[_\-]project/${NAME}/g' {} +
fi

mv blank_project/ $NAME
echo "A new blank project '${PREFIX}-${NAME}' is prepared."
echo "! Don't forget remove init.sh !"
