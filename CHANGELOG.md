
## Holodeck 0.2.0 Changes
* Updated Unreal Engine Version from 4.17 to 4.21
* Added ability to set the position and velocity with the set state command
* Can now turn sensors on and off and adjust how often cameras capture new frames (ticks per frame)
* Fixed some Unreal to Metric unit conversion issues. 
* Made deep copy of sensor info from buffers the default
* Fixed "Mmap length greater than file size issue
* Added option to change the number of physics / simulation frames per unreal second (Default is 30)
* Added low, medium, high rendering options
* Added headless option on linux
* Created new "TurtleBot" Agent. It is similar to the sphere agent but can apply forces to objects in the world. 
