# SAMI : Autonomous Robot Navigation with Motion Capture

## 1. Overview

SAMI is a robotics project focused on autonomous navigation of a Lego EV3 robot using an OptiTrack motion capture system. It implements a full control pipeline — from real-time position tracking to motor command generation with an emphasis on understanding path planning, feedback control, and robot-PC communication.

---

## 2. Results

- The robot successfully navigates a set of user-defined waypoints in a motion-capture arena
- The pipeline demonstrates stable real-time control at 10 Hz
- End-to-end system: from camera tracking to motor actuation over TCP
- The 2-opt TSP optimization consistently reduces total travel distance compared to a naive ordering of waypoints
- The feedback controller converges reliably under standard arena conditions; performance degrades at high speeds (PWM > 80) due to mechanical slip

---

## 3. Method

### Motion capture

- Position and orientation (yaw) of the robot are tracked in real time via OptiTrack cameras using the NatNet protocol
- Data is received over UDP and parsed by a custom NatNet client

### Path planning

- Waypoints are optimized using a **Travelling Salesman Problem** (TSP) heuristic:
  - Nearest Neighbor algorithm for an initial solution
  - 2-opt local search to remove crossing segments
- The robot visits waypoints in the computed order

### Control

- A nonlinear feedback controller computes left and right motor speeds at each time step
- Control law is based on the angular and linear error between the robot's current pose and the next waypoint
- Commands are sent as `MOV <left> <right>;` strings over TCP at 10 Hz

### Communication

- **PC side**: TCP client sends motor commands and reads OptiTrack data
- **Robot side**: TCP server running on the EV3 receives and interprets commands
- Command format: `MOV`, `NOP`, `BIP`, `WIN`, `ERE`

---

## 4. Data

- `data.txt`: raw position and sensor logs from test sessions
- `speed_data_pwm80.txt`: motor speed measurements at PWM = 80
- `performance_test_1.txt`: timing and accuracy results from a navigation test
- `PC/Tests/streamData/`: NatNet binary stream samples used for unit testing

---

## 5. Project Structure

```
SAMI/
├── PC/                          # PC-side code
│   ├── PC.py                    # Main control loop (TSP + feedback controller)
│   ├── TCPClient.py             # TCP client to communicate with robot
│   ├── testopti.py              # OptiTrack connection test
│   ├── config.ini               # OptiTrack configuration
│   ├── src/                     # NatNet client library
│   │   ├── Natnet_Client.py
│   │   ├── NatNetDataModel.py
│   │   ├── NatNetMessages.py
│   │   ├── NatNetPacket.py
│   │   ├── mocap_node.py
│   │   ├── common.py
│   │   └── debug.py
│   ├── Tests/                   # Unit tests for NatNet parsing
│   │   ├── testNatNet.py
│   │   ├── testNatnetClient.py
│   │   ├── testNode.py
│   │   ├── testCommon.py
│   │   ├── testAll.py
│   │   └── streamData/          # Binary NatNet stream samples
│   └── doc/                     # Hardware documentation and diagrams
├── Robot/
│   └── Robot.py                 # EV3 robot: TCP server + motor driver
├── lessons/                     # Teaching resources
│   ├── panel.py                 # Tkinter GUI for manual motor control
│   ├── robot_server.py          # Simplified TCP server (pedagogical)
│   ├── test_camera.py           # Camera test script
│   └── optitrack-master/        # OptiTrack library and examples
├── example_usage.py             # Standalone usage example
├── math_utils.py                # Mathematical utilities
└── README.md
```

---

## 6. Notes

This project emphasizes a practical implementation of autonomous robot control, combining motion capture tracking, path optimization, and real-time feedback. The NatNet client is a custom implementation of the OptiTrack NatNet SDK protocol, built from scratch to understand the underlying communication layer.
