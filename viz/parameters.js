// Parameters that were controlled by the UI
var INITIAL_SIZE = 250,
    INITIAL_WIND = [30.0, 30.0],
    INITIAL_CHOPPINESS = 4;

// Tiling factor (how many tiles are added either side of the original tile)
var TILES = 1.5;

// Visual parameters
var CLEAR_COLOR = [10.0, 1.0, 1.0, 1.0],
    GEOMETRY_ORIGIN = [-1000.0, -1000.0],
    SUN_DIRECTION = [-1.0, 1.0, 1.0], //points towards the sun, y is up
    OCEAN_COLOR = [0.004, 0.016, 0.047],
    SKY_COLOR = [3.2, 9.6, 12.8],
    EXPOSURE = 0.45, //exposure used for tone remapping

    GEOMETRY_RESOLUTION = 128, //resolution of the mesh (lower for more performance)
    GEOMETRY_SIZE = 2000,
    RESOLUTION = 512; //resolution of the wave simulation (can only be 512 or 128)

// Camera parameters

var CAMERA_DISTANCE = 1000,
    ORBIT_POINT = [200.0, 0.0, 600.0],
    INITIAL_AZIMUTH = 0.0,
    INITIAL_ELEVATION = 0.7,
    MIN_AZIMUTH = -0.2,
    MAX_AZIMUTH = 0.5,
    MIN_ELEVATION = 0.4,
    MAX_ELEVATION = 0.8,

    FOV = (60 / 180) * Math.PI, //field of view in radians

    NEAR = 1, //near clip plane
    FAR = 10000; //far clip plane
