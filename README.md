# livox_hpm_ros2
Livox High Precision Mapping (ROS2 Version)

Tested with Humble and Jazzy.

## Deps
- `ros-jazzy-desktop`
- `ros-dev-tools`
- `ros-jazzy-pcl-ros`

## Clone the repository

```shell
git clone git@github.com:iharuspex/livox_hpm_ws_ros2.git
git submodule update --init --recursive
```

## Build command (with `compile_commands.json` creation)

```shell
colcon build --symlink-install --parallel-workers 4 --cmake-args -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_BUILD_TYPE=Debug
```
