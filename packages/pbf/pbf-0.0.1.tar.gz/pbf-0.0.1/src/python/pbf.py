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

def temperatureBC(faceIndex, temperature):
    def process(thermalProblem, tstate):
        sliced = mlhp.sliceLast(process.function, tstate.time)
        return mlhp.integrateDirichletDofs(sliced, tstate.basis, [process.iface])
    
    process.function=mlhp.makeConstantFunction(4, temperature)
    process.iface=faceIndex
    
    return process

def thermalVtuOutput(filebase, vtuInterval=1):
    def process(thermalProblem, tstate):
        if tstate.index % process.interval == 0:
            processors = [mlhp.makeFunctionProcessor(mlhp.sliceLast(f, tstate.time), 
                "VolumeSource" + str(i)) for i, f in enumerate(thermalProblem.volumeSources)]
            processors += [mlhp.makeSolutionProcessor(3, tstate.dofs, "Temperature")]
            postmesh = mlhp.createGridOnCells([thermalProblem.degree]*3)
            writer = mlhp.PVtuOutput(filename=process.path + "_thermal_" + str(tstate.index // process.interval))
            mlhp.writeBasisOutput(tstate.basis, postmesh, writer, processors)

    process.path=filebase
    process.interval=vtuInterval
    
    return process
    
    
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
    
def makeThermalState(thermalProblem, mesh, srefinement=0, powderHeight=0.0, time=0.0, index=0):
    history = initializeHistory(mesh, srefinement, powderHeight)
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
    
    # Gather dirichlet dofs
    dirichletDofs = mlhp.combineDirichletDofs([f(thermalProblem, tstate1) for f in thermalProblem.dirichlet])
    solve = mlhp.makeCGSolver(1e-12)
    
    # Project solution from previous state
    K = mlhp.allocateUnsymmetricSparseMatrix(tstate1.basis)
    F = mlhp.allocateVectorWithSameSize(K)

    l2Integrand = mlhp.makeL2BasisProjectionIntegrand( 3, tstate0.dofs )

    mlhp.integrateOnDomain(tstate0.basis, tstate1.basis, l2Integrand, [K, F])

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

        quadrature = mlhp.makeMeshProjectionQuadrature(tstate1.history.grid)
        
        mlhp.integrateOnDomain(tstate1.basis, domainIntegrand, [K, F], dirichletDofs=dirichletIncrement )

        norm1 = mlhp.norm(F)
        norm0 = norm1 if i == 0 else norm0

        print(f"{norm1:.2e} ", end="", flush=True)
        
        dx = mlhp.inflateDofs(solve( K, F ), dirichletIncrement)
        
        tstate1.dofs = mlhp.add(tstate1.dofs, dx, -1.0)
        
        #if i == 0:
		#    state1.history = updateHistory( state0.history, *state1.basis, state1.dofs );
        
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

del os, sys, path
