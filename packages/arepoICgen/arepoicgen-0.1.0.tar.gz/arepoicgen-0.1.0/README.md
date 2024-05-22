# AREPO-icgen
Program for creating initial conditions for the AREPO code

The code works by calling generateICs(config, params), where config and params are dictionary objects that contain the settings to be used.
The config options are needed for all runs, but some parameters are only needed for particular configurations. Parameters that are not needed for a particular setup can be omitted.

#### Config Options

######################
# Initial grid setup #
######################

boxGrid    = Box of particles in an evenly spaced grid

boxRan     = Box of randomly spaced particles

sphereRan  = Sphere of randomly spaced particles

sphereGrid = Spherical volume cut of an evenly spaced grid of particles

"grid": *grid type*

####################
# Turbulence setup #
####################

turbFile = Turbulence from a 3D velocity cube file

static   = No turbulent velocities

"turbulence": *turbulence type*

If using turbFile, need to include a turbulence file along with its grid size:

"turbFile": *path/to/file*

"turbSize": *Size of the grid (64, 128, etc)*

##################
# Rotation Setup #
##################

rotation = Add rotation to the body

static   = No body rotation

"rotation": *rotation type*

#######################
# Low Density Padding #
#######################

True  = Pad the box outisde the cloud with low density particles

False = ... don't

"padding": *True/False*

###############
# File Output #
###############

arepo = Output a type 2 arepo datafile (broken)

hdf5  = Output a hdf5 (type 3) datafile

"output": *file type*

masses = Output masses

density = Output denisty as masses

"outVal": *output quantity*

True = Output a zero magnetic field for all particles [TESTING]

False = Don't use magnetic field

"bField": *magnetic field*

filename = Name you want the file to be called (no need for extension)

"filename": *filename*

#### Parameter Options

#######################
# Physical Dimensions #
#######################

Number of particles [no units]

"ngas": *number of particles*

Min x, max x, min y, max y, min z, max z [pc]

"bounds": [*xmin, xmax, ymin, ymax, zmin, zmax*]

Spherical cloud radius [pc] 

Only needed for spherical setups.

"radii": *cloud radius*

Total mass of the cloud [Msun]

"mass": *cloud mass*

###################
# Thermal Physics #
###################

Temperature of the cloud [K]

"temp": *cloud temperature*                       

Mean molecular weight of the cloud [no units]

"mu": *mu*                               

Virial parameter, ratio of KE to GPE [no units]

Only needed for clouds with turbulence. 

"virialParam": *ratio*     

####################
# Rotation Physics #
####################

Beta parameter, ratio of rotational KE to GPE [no units]

Only needed for clouds with rotation.

"beta": *beta value*

####################
# Box Padding Info #
####################

The x, y and z size of the box around the cloud, multiples of the cloud size [no units]

Only needed when padding the box with low density particles. 

"boxDims": [*x, y, z*]

How much hotter these particles should be compared to the cloud [no units]

"tempFactor": *amount*

###################
# Desired Density #
###################

The desired number density of the cloud [cm^-3]

Has to be consistent with the mass we've given above 

Only needed if outputting density as mass.

"density": *rho*

#### Example

An example config and parameter setup might look like below, for a uniform sphere of gas with rotation only:

```
config = {
    "grid": "sphereGrid",
    "turbulence": "static",
    "rotation": "rotation",
    "padding": True,
    "output": "hdf5",
    "outValue": "masses",
    "bField": False,
    "filename": "uniformSphere"
}

params = {
    "ngas": 200000,
    "bounds": [0, 0.4, 0, 0.4, 0, 0.4],
    "radii": 0.08,
    "mass": 5,
    "temp": 15,
    "mu": 1.4,
    "beta": 3,
    "boxDims": [5, 5, 5],
    "tempFactor": 2
}
```
