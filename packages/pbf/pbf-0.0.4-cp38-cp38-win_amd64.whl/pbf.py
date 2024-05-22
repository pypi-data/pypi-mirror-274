# This file is part of the mlhpbf project. License: See LICENSE
import os, sys

try:
    # mlhp.py script folder
    path = os.path.abspath( os.path.dirname(sys.argv[0]) );
    
    # Try to open path/mlhpPythonPath containing the python module path. This
    # file is written as post build command after compiling pymlhpcore.
    with open( os.path.join( path, 'mlhpPythonPath' ), 'r') as f:
        sys.path.append( os.path.normpath( f.read( ).splitlines( )[0] ) )
        
except IOError: 
    pass
        
from pymlhpbf import *

import mlhp
import math
from dataclasses import dataclass

vtudefault="RawBinary"

#def makePowder(material, 

def temperatureBC(faceIndex, temperature):
    def process(thermalProblem, tstate):
        sliced = mlhp.sliceLast(process.function, tstate.time)
        return mlhp.integrateDirichletDofs(sliced, tstate.basis, [process.iface])
    
    process.function=mlhp.makeConstantFunction(4, temperature)
    process.iface=faceIndex
    
    return process

def thermalVtuOutput(filebase, interval=1, writemode=vtudefault):
    def process(thermalProblem, tstate):
        if tstate.index % process.interval == 0:
            processors = [mlhp.makeFunctionProcessor(mlhp.sliceLast(f, tstate.time), 
                "VolumeSource" + str(i)) for i, f in enumerate(thermalProblem.volumeSources)]
            processors += [mlhp.makeSolutionProcessor(3, tstate.dofs, "Temperature")]
            postmesh = mlhp.createGridOnCells([thermalProblem.degree]*3)
            writer = mlhp.PVtuOutput(filename=process.path + "_thermal_" + 
                str(tstate.index // process.interval), writemode=writemode)
            mlhp.writeBasisOutput(tstate.basis, postmesh, writer, processors)
    
    process.path=filebase
    process.interval=interval
    
    return process

def materialVtuOutput(filebase, interval=1, writemode=vtudefault):
    def process(thermalProblem, tstate):
        if tstate.index % process.interval == 0:
            processors = [mlhp.makeCellDataProcessor(3, tstate.history.data( ), "MaterialState")]
            postmesh = mlhp.createGridOnCells([thermalProblem.degree]*3, mlhp.PostprocessTopologies.Volumes)
            writer = mlhp.PVtuOutput(filename=process.path + "_material_" + 
                str(tstate.index // process.interval), writemode=writemode)
            mlhp.writeMeshOutput(tstate.history.grid( ), postmesh, writer, processors)
    
    process.path=filebase
    process.interval=interval
    
    return process
    
def thermalEvaluator(state):
    return internalThermalEvaluator(state.basis, state.dofs)

def meltingTemperature(material, phi=0.5):
    return (1.0 - phi) * material.solidTemperature + phi * material.liquidTemperature

def meltPoolContourOutput(output, interval=1, resolution=None, writemode=vtudefault):
    def process(thermalProblem, tstate):
        if tstate.index % process.interval == 0:
            threshold = meltingTemperature(thermalProblem.materials["structure"])
            function = mlhp.implicitThreshold(thermalEvaluator(tstate), threshold)
            postmesh = mlhp.createMarchingCubesBoundary(function, 
                [thermalProblem.degree]*3 if resolution is None else resolution)
            writer = mlhp.DataAccumulator( )   
            if isinstance(process.output, str):
                writer = mlhp.PVtuOutput(filename=process.output + "_meltpool_" + 
                    str(tstate.index // process.interval), writemode=writemode)
            mlhp.writeMeshOutput(tstate.mesh, postmesh, writer, [])
            if not isinstance(process.output, str):
                process.output(writer.mesh( ) )

    process.output=output
    process.interval=interval
    
    return process
 
def meltPoolBoundsPrinter(interval=1, resolution=None):
    def meltPoolBoundsCallback( mesh ):
        points = mesh.points( )
        bounds = [[1e50, 1e50, 1e50], [-1e50, -1e50, -1e50]]
        for ipoint in range(int(len(points)/3)):
            for icoord in range(3):
                bounds[0][icoord] = min(bounds[0][icoord], points[3*ipoint + icoord])
                bounds[1][icoord] = max(bounds[1][icoord], points[3*ipoint + icoord])
        print(f"    melt pool bounds: {[max(u - l, 0.0) for l, u in zip(*bounds)]}")
    return meltPoolContourOutput(meltPoolBoundsCallback, interval, resolution)
   
class ThermalProblem:
    def __init__(self):
        self.dirichlet   = []
        self.residual    = []
        self.postprocess = []
        self.degree = 1
        self.ambientTemperature = 25.0
        self.volumeSources = []
        
    def addPostprocessor(self, postprocessor):
        self.postprocess.append(postprocessor)
        
    def addDirichletBC(self, condition):
        self.dirichlet.append(condition)
        
    def addSource(self, source):
        self.volumeSources.append(source)
        
    def setMaterials(self, materials):
        self.materials = materials  
        
@dataclass
class State:
    time: float
    index: int
    mesh: None
    basis: None
    dofs: None
    history: None
    
def makeThermalState(thermalProblem, mesh, part=None, srefinement=0, powderHeight=0.0, time=0.0, index=0):
    domain = part if part is not None else mlhp.implicitHalfspace([0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
    history = initializeHistory(mesh, domain, srefinement, powderHeight, nseedpoints=4)
    refinedMesh = mlhp.makeRefinedGrid(mesh)
    basis = mlhp.makeHpTrunkSpace(refinedMesh, thermalProblem.degree)
    dofs = mlhp.projectOnto(basis, mlhp.makeConstantFunction(3, thermalProblem.ambientTemperature))
    
    return State(time, index, refinedMesh, basis, dofs, history)
    
def thermalTimeStep(thermalProblem, tstate0, deltaT):
    tstate1 = State(time    = tstate0.time + deltaT,
                    index   = tstate0.index + 1,
                    mesh    = tstate0.mesh,
                    basis   = tstate0.basis,
                    dofs    = None,
                    history = tstate0.history)
    
    print(f"    thermal problem: {tstate1.basis.nelements( )} elements, {tstate1.basis.ndof( )} dofs")
    
    # Gather dirichlet dofs
    dirichletDofs = mlhp.combineDirichletDofs([f(thermalProblem, tstate1) for f in thermalProblem.dirichlet])
    
    # Project solution from previous state
    K = mlhp.allocateUnsymmetricSparseMatrix(tstate1.basis)
    F = mlhp.allocateVectorWithSameSize(K)

    l2Integrand = mlhp.makeL2BasisProjectionIntegrand( 3, tstate0.dofs )

    mlhp.integrateOnDomain(tstate0.basis, tstate1.basis, l2Integrand, [K, F])

    solve = mlhp.makeCGSolver(1e-12)
    tstate1.dofs = solve(K, F)
    projectedDofs0 = tstate1.dofs
    
    del K, F
    
    # Prepare nonlinear iterations
    K = mlhp.allocateUnsymmetricSparseMatrix(tstate1.basis, dirichletDofs[0])
    F = mlhp.allocateVectorWithSameSize(K)
    F0 = mlhp.allocateVectorWithSameSize(K)
    
    theta = 1.0
    
    projectionIntegrand = makeThermalInitializationIntegrand( thermalProblem.materials, 
        thermalProblem.volumeSources, tstate0.history, tstate0.dofs, tstate0.time, deltaT, theta )
        
    mlhp.integrateOnDomain( tstate0.basis, tstate1.basis, projectionIntegrand, [F0], dirichletDofs=dirichletDofs )
    
    norm0 = 0.0
    print("    || F || --> ",end="", flush=True);

    # Newton-Raphson iterations
    for i in range(40):
        F = mlhp.copy(F0);
        mlhp.fill(K, 0.0 );
        
        dirichletIncrement = computeDirichletIncrement(dirichletDofs, tstate1.dofs, -1.0)
        
        domainIntegrand = makeTimeSteppingThermalIntegrand( thermalProblem.materials, 
            tstate1.history, projectedDofs0, tstate1.dofs, tstate1.time - tstate0.time, theta )

        quadrature = mlhp.makeMeshProjectionQuadrature(tstate1.history.grid( ))
        
        mlhp.integrateOnDomain(tstate1.basis, domainIntegrand, [K, F], 
            quadrature=quadrature, dirichletDofs=dirichletIncrement)

        norm1 = mlhp.norm(F)
        norm0 = norm1 if i == 0 else norm0

        print(f"{norm1:.2e} ", end="", flush=True)
        
        dx = mlhp.inflateDofs(solve( K, F ), dirichletIncrement)
        
        tstate1.dofs = mlhp.add(tstate1.dofs, dx, -1.0)
        
        if i == 0:
            tstate1.history = updateHistory(tstate0.history, tstate1.basis, tstate1.dofs, 
                meltingTemperature(thermalProblem.materials["structure"]) )
        
        if norm1 / norm0 <= 1e-6 or norm1 < 1e-11:
            break;
        if ( i + 1 ) % 6 == 0: 
            print("\n                ", end="", flush=True)
        
    print("", flush=True)
    
    return tstate1
    
def computeThermalProblem( thermalProblem, tstate0, deltaT, duration ):
    nsteps = int( math.ceil( duration / deltaT ) );
    realDT = duration / nsteps;
    
    print(f"Integrating thermal problem:", flush=True)
    print(f"    duration        = {duration}", flush=True)
    print(f"    number of steps = {nsteps}", flush=True)
    print(f"    step size       = {realDT}", flush=True)
    print(f"    base mesh size  = {tstate0.mesh.ncells()}", flush=True)

    for pp in thermalProblem.postprocess:
        pp(thermalProblem, tstate0)

    for istep in range(nsteps):
        print(f"Time step {istep + 1} / {nsteps}", flush=True)
        
        tstate1 = thermalTimeStep(thermalProblem, tstate0, realDT)

        for pp in thermalProblem.postprocess:
            pp(thermalProblem, tstate1)

        tstate0 = tstate1;

    return tstate0

def computeSteadyStateThermal(thermalProblem, tstate, laserVelocity):

    # Gather dirichlet dofs
    dirichletDofs = mlhp.combineDirichletDofs([f(thermalProblem, tstate) for f in thermalProblem.dirichlet])

    # Prepare for nonlinear iterations
    K = mlhp.allocateUnsymmetricSparseMatrix(tstate.basis, dirichletDofs[0])
    F = mlhp.allocateVectorWithSameSize(K)
    tstate.dofs = mlhp.DoubleVector(tstate.basis.ndof( ), 0.0)

    slicedSources = [mlhp.sliceLast(f, tstate.time) for f in thermalProblem.volumeSources]

    norm0 = 1.0
    print("    || F || --> ",end="", flush=True);

    for i in range(40):
        mlhp.fill(F, 0.0);
        mlhp.fill(K, 0.0);
        
        dirichletIncrement = computeDirichletIncrement(dirichletDofs, tstate.dofs, -1.0)
        
        domainIntegrand = makeSteadyStateThermalIntegrand(thermalProblem.materials, 
            slicedSources, tstate.history, tstate.dofs, laserVelocity)

        quadrature = mlhp.makeMeshProjectionQuadrature(tstate.history.grid( ))
        
        mlhp.integrateOnDomain(tstate.basis, domainIntegrand, [K, F], 
            quadrature=quadrature, dirichletDofs=dirichletIncrement)

        norm1 = mlhp.norm(F)
        norm0 = norm1 if i == 0 else norm0

        print(f"{norm1:.2e} ", end="", flush=True)
        
        P = mlhp.makeAdditiveSchwarzPreconditioner(K, tstate.basis, dirichletIncrement[0])
        dx = mlhp.bicgstab(K, F, preconditioner=P, maxit=1000, tolerance=1e-12)
        dx = mlhp.inflateDofs(dx, dirichletIncrement)

        tstate.dofs = mlhp.add(tstate.dofs, dx, -1.0)
        
        if norm1 / norm0 <= 1e-6 or norm1 < 1e-11:
            break;
        if ( i + 1 ) % 6 == 0: 
            print("\n                ", end="", flush=True)
        
    print("", flush=True)
    
    for pp in thermalProblem.postprocess:
        pp(thermalProblem, tstate)
    
del os, sys, path
from mlhp import *
