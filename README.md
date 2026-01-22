# NEAT Self-Driving Car 🚗🧠

A 2D self-driving car simulation built with Python and Pygame, using the **NEAT (NeuroEvolution of Augmenting Topologies)** algorithm to train neural networks to drive automatically.

## 🌟 Features

- **Neuroevolution**: Cars learn to drive from scratch using genetic algorithms (NEAT).
- **10 Unique Tracks**: Includes loops, chicanes, mazes, and open fields.
- **Interactive UI**: Switch between tracks instantly using on-screen buttons (1-10).
- **Advanced Sensing**: Cars use **8 ray-casting sensors** to see in 360 degrees.
- **Robust Physics**:
  - Accurate **Line-Segment Collision Detection** (no wall clipping).
  - Friction and acceleration mechanics.
- **Visual Feedback**: Real-time rendering of sensor rays (Green = Safe, Red = Obstacle).

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/royswastik07/RL-CAR.git
   cd neat-self-driving-car
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install pygame neat-python
   ```

## 🎮 How to Run

Run the main simulation script:

```bash
python main.py
```

### Controls
- **Track Switching**: Click the buttons **1 through 10** at the top of the window to change the track layout.
  - *Note: Switching tracks will reset the current generation to restart training on the new terrain.*

## 🧠 How it Works

1. **Input**: The car has 8 sensors that measure distance to the nearest wall in 8 directions (0°, 45°, 90°, etc.).
2. **Processing**: These 8 inputs are fed into a Neural Network (evolved by NEAT).
3. **Output**: The network outputs 2 values:
   - **Steering**: Left or Right.
   - **Throttle**: Accelerate or Decelerate.
4. **Evolution**:
   - Each generation consists of 50 cars.
   - Cars that travel further without crashing get a higher **fitness score**.
   - The best performing cars "mate" and mutate to create the next generation.
   - Over time, they learn optimal driving strategies.

## 📂 Project Structure

- `main.py`: Entry point. Handles the game loop, UI, and NEAT training integration.
- `car.py`: Physics engine, movement logic, and collision detection.
- `track.py`: Definitions for the 10 different track layouts.
- `sensors.py`: Ray-casting logic and visual rendering of sensor beams.
- `config-neat.txt`: Configuration parameters for the genetic algorithm (population size, mutation rates, etc.).

Its a testing project fullly vibe coded (Dont encourage to vibe code though )
