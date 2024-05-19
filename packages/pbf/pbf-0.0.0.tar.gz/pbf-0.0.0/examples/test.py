import pbf

IN625 = pbf.readMaterialFile("materials/IN625.json")

min = [0.0, 0.0, 0.0]
max = [1.0, 1.0, 1.0]

elementSize = 0.1
layerHeight = 0.1

filebase = "outputs/test"
grid = pbf.createMesh( min, max, elementSize, layerHeight )

tsetup = pbf.ThermalProblem( )
tsetup.addPostprocessor(pbf.thermalVtuOutput(filebase))
tsetup.setMaterials({"powder" : IN625, "structure" : IN625, "baseplate" : IN625, "air" : IN625})
tsetup.addDirichletBC(pbf.temperatureBC(4, tsetup.ambientTemperature))

tstate0 = pbf.makeThermalState(tsetup, grid)

pbf.computeThermalProblem(tsetup, tstate0, 0.1, 2.0)
