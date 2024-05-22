import pbf

IN625 = pbf.makeMaterial("IN625")
#IN625 = pbf.readMaterialFile("materials/IN625.json")

laserD4Sigma = 0.170
laserSpeed = 800.0
laserPower = 280.0 * 1000.0
layerHeight = 0.05
domainHeight = 0.5

x0 = 0.25;
x1 = 0.75;
dur = ( x1 - x0 ) / laserSpeed

elementSize = 0.12 * laserD4Sigma;
timestep = 0.2 * laserD4Sigma / laserSpeed;
        
laserTrack = [pbf.LaserPosition(xyz=[x0, 0.0, domainHeight], time=0.0, power=laserPower),
              pbf.LaserPosition(xyz=[x1, 0.0, domainHeight], time=dur, power=laserPower)]

laserBeam = pbf.gaussianBeam(sigma=laserD4Sigma / 4, absorptivity=0.32)
heatSource = pbf.volumeSource(laserTrack, laserBeam, depthSigma=0.045)

domainMin = [0.0, -0.3, -0.3]
domainMax = [1.0, 0.3, domainHeight]

filebase = "outputs/stldomain"
grid = pbf.createMesh(domainMin, domainMax, elementSize, layerHeight)

tsetup = pbf.ThermalProblem( )
tsetup.addPostprocessor(pbf.thermalVtuOutput(filebase))
tsetup.addPostprocessor(pbf.meltPoolBoundsPrinter())
tsetup.addPostprocessor(pbf.materialVtuOutput(filebase))
tsetup.setMaterials({"powder" : IN625, "structure" : IN625, "baseplate" : IN625, "air" : IN625})
#tsetup.addDirichletBC(pbf.temperatureBC(4, tsetup.ambientTemperature))
tsetup.addSource(heatSource) 

triangulation = pbf.readStl("stldomain.stl")
scale = pbf.scaling([0.05, 0.05, 0.05])
move = pbf.translation([0.5, 0.0, 0.25])
domain = pbf.implicitTriangulation(triangulation)
domain = pbf.implicitTransformation(domain, pbf.concatenate([scale, move]))

tstate0 = pbf.makeThermalState(tsetup, grid, part=domain, powderHeight=domainHeight, srefinement=3)

pbf.computeThermalProblem(tsetup, tstate0, timestep, dur)#3 * dur)

