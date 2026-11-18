# Need Input — ROS2 Robot Controller

## Project Structure

- **robot_control** — State logic (Teleop, Autonomy, Mode Switch)
- **robot_fsm** — State decisions and transitions
- **robot_serial** — Robot data and Arduino communication

## Setup

### GitHub

Clone the repository:

git clone <repository-url>
cd Need_Input

Pull the latest changes:

git pull origin main

### Normal Docker Setup

Make sure Docker is installed and running.

Build the Docker image:

./build.sh

Run the appropriate script for your operating system:

**macOS:**

./run-macos.sh

**Linux:**

./run-linux.sh

**Windows (WSL2):**

./run-wsl2.sh

## Development

Once inside the Docker container, build the ROS2 workspace:

cd /ros_ws
colcon build --symlink-install
source install/setup.bash

All ROS2 packages are located in `src/`:

- `src/robot_control/`
- `src/robot_fsm/` -Victor
- `src/robot_serial/`