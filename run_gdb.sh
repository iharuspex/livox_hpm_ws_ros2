#!/bin/bash

source install/setup.bash

ctrl_c () {
    echo "Ctrl + C"
}

trap 'ctrl_c' SIGINT

source install/setup.bash
ros2 run --prefix 'gdbserver localhost:3000' livox_mapping livox_mapping_case
