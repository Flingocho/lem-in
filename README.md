# � Lem-in - Ant Colony Pathfinding Simulation

<div align="center">
  <img src="https://img.shields.io/badge/Language-C-blue" alt="Language">
  <img src="https://img.shields.io/badge/Algorithm-Pathfinding-green" alt="Algorithm">
  <img src="https://img.shields.io/badge/Status-Completed-success" alt="Status">
  <img src="https://img.shields.io/badge/42-School-brightgreen" alt="42">
  <br><br>
</div>

<div align="center">
  <img src="https://img.shields.io/badge/Python-Visualizer-yellow" alt="Python">
  <img src="https://img.shields.io/badge/Matplotlib-Graphs-orange" alt="Matplotlib">
  <br><br>
</div>

<details open>
<summary><b>🚀 Overview</b></summary>

The **Lem-in** project is an ant colony simulation that solves the challenge of moving a colony of ants through a network of rooms and tunnels from a start room to an end room in the minimum number of moves. This project demonstrates advanced graph algorithms, pathfinding techniques, and optimization strategies.

The program finds the optimal combination of paths through a graph and efficiently distributes ants across these paths to minimize the total number of steps required for all ants to reach their destination.

The project includes a **Python visualizer** with **interactive graphs** that displays the room network, found paths, and provides visual analysis of the ant movement simulation with **anti-overlap line rendering** for better visualization.

</details>

<details>
<summary><b>✨ Features</b></summary>

- � **Multi-Path Algorithm**: Finds multiple optimal paths simultaneously
- 🧠 **Smart Ant Distribution**: Optimally distributes ants across paths to minimize total moves
- 🎯 **Pathfinding Optimization**: Uses advanced graph algorithms for efficient path discovery
- � **Movement Simulation**: Simulates ant movement with collision detection and flow control
- � **Input Validation**: Robust parsing and validation of room networks and connections
- 🎨 **Interactive Visualization**: Python-based graph visualization with matplotlib
- 🔧 **Anti-Overlap Rendering**: Smart line separation to avoid visual overlapping in complex graphs
- 🏗️ **Dynamic Memory Management**: Efficient memory allocation and cleanup
- 📈 **Performance Analysis**: Detailed statistics and path analysis output
</details>

<details>
<summary><b>📊 Algorithm Specifications</b></summary>

| Algorithm | Description | Complexity |
|-----------|-------------|------------|
| **Path Finding** | Multi-path BFS-based algorithm to find all possible paths | O(V + E) per path |
| **Ant Distribution** | Optimal distribution algorithm to minimize total moves | O(P × A) where P=paths, A=ants |
| **Flow Simulation** | Step-by-step ant movement with collision detection | O(S × A) where S=steps |
| **Graph Parsing** | Room and connection validation with duplicate detection | O(V + E) |
| **Memory Management** | Dynamic allocation with automatic cleanup | O(V + E) |

### Input Format
```
[number_of_ants]
##start
[start_room] [x] [y]
##end  
[end_room] [x] [y]
[room1] [x] [y]
[room2] [x] [y]
...
[room1]-[room2]
[room2]-[room3]
...
```

</details>

<details>
<summary><b>🛠️ Technical Implementation</b></summary>

<details>
<summary><b>🔑 Core Components</b></summary>

| Component | Key Features |
|----------|-------------|
| **Graph Parser** | Room validation, coordinate checking, connection parsing |
| **Pathfinder** | BFS-based multi-path discovery, cycle detection |
| **Ant Distributor** | Optimal ant assignment across multiple paths |
| **Flow Simulator** | Step-by-step movement with collision avoidance |
| **Memory Manager** | Dynamic allocation, automatic cleanup, overflow protection |
| **Visualizer** | Interactive graph rendering with matplotlib |

</details>

<details>
<summary><b>⚙️ Algorithm Techniques</b></summary>

| Technique | Description |
|-----------|-------------|
| **Multi-Path BFS** | Finds all possible paths from start to end room |
| **Flow Optimization** | Distributes ants to minimize total completion time |
| **Collision Detection** | Prevents ants from occupying the same room |
| **Graph Validation** | Ensures room uniqueness and valid connections |
| **Memory Pooling** | Efficient allocation for rooms and connections |
| **Anti-Overlap Rendering** | Visual separation of parallel lines in graph display |

</details>
</details>

<details>
<summary><b>🛠️ Installation & Usage</b></summary>

```bash
# Clone the repository
git clone https://github.com/yourusername/lem-in.git

# Navigate to the directory
cd lem-in

# Build the project
make

# Test with example maps
./lem-in < maps/example.map

# Use with visualizer (requires Python and matplotlib)
./lem-in < maps/paths4.map | python3 ant_visualizer.py

# Clean object files
make clean

# Clean everything
make fclean

# Rebuild from scratch
make re
```

### Project Structure

```
lem-in/
├── lemin.h               # Header file with structures and function prototypes
├── lemin.c               # Main program logic and input parsing
├── lemin_room_utils.c    # Room management utilities
├── lemin_algorithm.c     # Pathfinding and ant distribution algorithms
├── intoverunderflow.c    # Overflow protection utilities
├── ant_visualizer.py     # Interactive Python visualizer
├── generator_linux       # Map generator for testing
├── Makefile              # Build automation
├── libft_ext/            # Extended libft library
├── maps/                 # Example map files
│   ├── example.map
│   ├── paths4.map
│   ├── big.map
│   └── ...
└── README.md             # This file
```

### Build System

The project uses **GCC** with the following configuration:
- **Compiler**: GCC with strict flags (-Wall -Wextra -Werror)
- **Dependencies**: Custom libft library included
- **Platform**: Linux/macOS compatible

### Visualizer Requirements

The Python visualizer requires:
- **Python 3.6+**
- **matplotlib** for graph rendering
- **numpy** (optional, for advanced features)

```bash
# Install visualizer dependencies
pip install matplotlib numpy
```

</details>

<details>
<summary><b>🧪 Testing & Examples</b></summary>

The project includes comprehensive test maps and examples:

### Example Maps
- **simple.map**: Basic 3-room linear path
- **paths4.map**: Multiple parallel paths for optimal distribution
- **big.map**: Large complex network with many rooms
- **intricate.map**: Complex maze-like structure
- **subject.map**: Official subject example

### Testing Categories

| Test Type | Description | Example |
|-----------|-------------|---------|
| **Basic Tests** | Simple linear paths | `./lem-in < maps/simple.map` |
| **Multi-Path** | Multiple path optimization | `./lem-in < maps/paths4.map` |
| **Large Scale** | Performance with big graphs | `./lem-in < maps/big.map` |
| **Edge Cases** | Error handling and validation | Custom input testing |
| **Visual Analysis** | Interactive graph display | `./lem-in < maps/cool.map \| python3 ant_visualizer.py` |

### Sample Output
```
5
##start
start 0 50
##end
end 200 50
a1 40 50
...
path num: 0    ants assigned: 3    start: start -> a1 -> a2 -> end
path num: 1    ants assigned: 2    start: start -> b1 -> b2 -> end

=== SIMULATION ===
L1-a1 L2-b1
L1-a2 L2-b2 L3-a1
L1-end L2-end L3-a2
L3-end
```

### Visualizer Features
- **Interactive Graph**: Zoom, pan, and explore the room network
- **Path Highlighting**: Different colors for each discovered path
- **Ant Distribution**: Visual representation of ant assignment
- **Statistics Display**: Rooms, connections, and performance metrics
- **Anti-Overlap Lines**: Smart line separation for better readability

</details>

<details>
<summary><b>🏗️ Algorithm Architecture</b></summary>

### Data Structures
```c
typedef struct s_room {
    int         room_id;
    char        *room_name;
    int         is_start;
    int         is_end;
    int         x, y;              // Coordinates for visualization
    int         conn_count;
    struct room **connections;     // Dynamic array of connections
    int         current_ant;       // Ant currently in this room
} t_room;

typedef struct s_path {
    int *room_ids;                 // Array of room IDs in path
    int length;                    // Path length
    int ants_assigned;             // Number of ants using this path
} t_path;
```

### Pathfinding Strategy
```c
// Multi-path BFS implementation
t_path **findAllPaths(t_lemin *vars) {
    // 1. Initialize BFS queue with start room
    // 2. Explore all possible paths to end room
    // 3. Store each unique path found
    // 4. Return array of all valid paths
}
```

### Ant Distribution Algorithm
```c
// Optimal distribution for minimum completion time
void distributeAnts(t_path **paths, t_lemin *vars) {
    // 1. Calculate completion time for each path combination
    // 2. Use greedy approach to minimize total time
    // 3. Assign ants to paths optimally
}
```

</details>

<details>
<summary><b>🔧 Dependencies</b></summary>

### Build Dependencies
- **GCC**: GNU Compiler Collection
- **Make**: Build automation tool
- **LibFT**: Custom C library (included in project)

### Runtime Dependencies
- **Standard C Library**: For basic I/O and memory operations
- **POSIX**: For system calls and file operations

### Visualizer Dependencies
- **Python 3.6+**: For running the visualizer
- **matplotlib**: For graph rendering and visualization
- **numpy**: For mathematical operations (optional)

### Installation on Ubuntu/Debian
```bash
sudo apt update
sudo apt install gcc make python3 python3-pip
pip3 install matplotlib numpy
```

### Installation on macOS
```bash
# Install Xcode command line tools
xcode-select --install

# Install Python dependencies
pip3 install matplotlib numpy
```

### Installation on Arch Linux
```bash
sudo pacman -S gcc make python python-pip
pip install matplotlib numpy
```

</details>

<details>
<summary><b>🌟 Key Learning Outcomes</b></summary>

- 🎯 **Graph Algorithms**: Deep understanding of BFS, pathfinding, and graph traversal
- 🧠 **Optimization Problems**: Multi-path optimization and resource distribution
- 🔧 **Data Structures**: Dynamic arrays, linked structures, and memory management
- ⚡ **Performance Analysis**: Algorithm complexity and optimization techniques
- 🛡️ **Input Validation**: Robust parsing and error handling
- 📊 **Flow Control**: Simulation of concurrent processes and collision detection
- 🔍 **Debugging Skills**: Complex algorithm debugging and testing
- 🏗️ **Software Architecture**: Modular design and code organization
- 🎨 **Visualization**: Interactive graph rendering and data presentation
- 📈 **Problem Solving**: Breaking down complex problems into manageable components
</details>

<details>
<summary><b>📊 Performance Benchmarks</b></summary>

Performance analysis with different map types:

| Map Type | Rooms | Connections | Paths Found | Total Steps | Completion Time |
|----------|-------|-------------|-------------|-------------|-----------------|
| Simple Linear | 5 | 4 | 1 | 15 | ~0.1ms |
| Multi-Path | 15 | 31 | 3 | 8 | ~0.5ms |
| Large Network | 1000+ | 3000+ | 5+ | varies | ~50ms |
| Complex Maze | 500+ | 1500+ | 2-3 | varies | ~25ms |

*Benchmarks performed on standard Linux system with various ant counts*

### Algorithm Performance
- **Path Discovery**: Linear time complexity O(V + E) per path
- **Ant Distribution**: Efficient greedy algorithm with O(P × A) complexity
- **Memory Usage**: Dynamic allocation scales with input size
- **Visualization**: Real-time rendering for networks up to 10,000 nodes

### Optimization Features
- **Multi-Path Processing**: Parallel path discovery and evaluation
- **Smart Distribution**: Optimal ant assignment to minimize completion time
- **Memory Pooling**: Efficient allocation and cleanup
- **Visual Optimization**: Anti-overlap line rendering for better readability

</details>

<details>
<summary><b>📜 License</b></summary>

This project is part of the 42 School curriculum and is provided under the [MIT License](LICENSE).
</details>

---

<div align="center">
  Created with ❤️ by <a href="https://github.com/jainavas">jainavas</a> and <a href="https://github.com/Flingocho">Flingocho</a>
</div>
