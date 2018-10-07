# Holodeck Worlds
Holodeck comes with a series of pre-built and packaged worlds that are available for download and use. 
These can be installed with `holodeck.install("package_name")`.

## Available Packages
To better understand the contents of each world, take a look at the config file that is installed with each world. It follows the [config file format](https://github.com/BYU-PCCL/holodeck/wiki/The-Config-File-Format). For details on the tasks contained in each world and additional notes, see below:

### DefaultWorlds
Package name: "DefaultWorlds"

The default worlds contain several basic maps for general use. The maps are:


AndroidPlayground
- Task: Distance
     * Main Agent: UavAgent ("uav0")
 
CyberPunkCity
- Task: Proximity
     * Main Agent: UavAgent ("uav0")
     * To Follow: NavAgent ("nav0")
     * Only within sight: True
 
Europeanforest
- Task: Proximity
     * Main Agent: UavAgent ("uav0")
     * Target: Barn Door
 
MazeWorld
- Task: Maze
     * Main Agent: DiscreteSphereAgent ("sphere0")
     * Target: Far wall
 
RedwoodForest
- Task: Distance
     * Main Agent: UavAgent ("uav0")
 
 InfiniteForest
- Task: Distance
     * Main Agent: UavAgent ("uav0") 
 
UrbanCity
- Task: Distance
     * Main Agent: UavAgent ("uav0")
