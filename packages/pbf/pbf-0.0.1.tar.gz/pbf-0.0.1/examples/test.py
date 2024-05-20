import pbf

IN625 = pbf.makeMaterial("IN625")
#IN625 = pbf.readMaterialFile("materials/IN625.json")

laserD4Sigma = 0.170
laserSpeed = 800.0
laserPower = 180.0
layerHeight = 0.0

x0 = 0.25;
x1 = 0.75;
dur = ( x1 - x0 ) / laserSpeed

elementSize = 0.12 * laserD4Sigma;
timestep = 0.2 * laserD4Sigma / laserSpeed;
        
laserTrack = [pbf.LaserPosition(xyz=[x0, 0.0, layerHeight], time=0.0, power=laserPower),
              pbf.LaserPosition(xyz=[x1, 0.0, layerHeight], time=dur, power=laserPower)]

laserBeam = pbf.gaussianBeam(sigma=laserD4Sigma / 4, absorptivity=0.32)
heatSource = pbf.volumeSource(laserTrack, laserBeam, depthSigma=0.045)

domainMin = [0.0, -0.3, -0.3]
domainMax = [1.0, 0.3, layerHeight]

filebase = "outputs/single_track"
grid = pbf.createMesh(domainMin, domainMax, elementSize, layerHeight)

tsetup = pbf.ThermalProblem( )
tsetup.addPostprocessor(pbf.thermalVtuOutput(filebase))
tsetup.setMaterials({"powder" : IN625, "structure" : IN625, "baseplate" : IN625, "air" : IN625})
tsetup.addDirichletBC(pbf.temperatureBC(4, tsetup.ambientTemperature))
tsetup.addSource(heatSource) 

tstate0 = pbf.makeThermalState(tsetup, grid)

pbf.computeThermalProblem(tsetup, tstate0, timestep, 3 * dur)
