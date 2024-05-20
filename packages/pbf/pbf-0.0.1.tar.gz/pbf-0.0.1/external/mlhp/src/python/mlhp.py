# This file is part of the mlhp project. License: See LICENSE

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
        
from pymlhpcore import *

def defineWithDimensionArg( function_ ):

    # Check whether function exists (hard code 3D for now)
    assert( eval( function_ + "3D" ) )

    def wrap( dimension, *args, **kwargs ):
        return eval( function_ + str( dimension ) + "D" )( *args, **kwargs )        
        
    globals( )[function_] = wrap

# For all these we generate versions with dimension appended, 
# like function -> function1, function2, function3, and so on.
defineWithDimensionList = [
    "makeSolutionProcessor", 
    "makeSolutionProcessor", 
    "makeL2BasisProjectionIntegrand",
    "makeStandardQuadrature",
    "makeConstantFunction", 
    "makeSingularSolution",
    "makeSingularSolutionSource",
    "makeSingularSolutionDerivatives",
    "makeAmLinearHeatSolution",
    "makeAmLinearHeatSource",
    "makeOffsetOrderDeterminor",
    "makeSmallStrainKinematics"
]

for function_ in defineWithDimensionList:
    defineWithDimensionArg( function_ )

def cg( matrix, rhs, preconditioner=None, maxit=None, tolerance=1e-8, residualNorms=False ):
    
    maximumNumberOfIterations = len( rhs ) if maxit is None else maxit
    
    M = makeMultiply( matrix ) if isinstance(matrix, AbsSparseMatrix) else matrix
    
    if preconditioner is None:
        P = makeNoPreconditioner( len( rhs ) )
    elif isinstance(preconditioner, AbsSparseMatrix):
        P = makeMultiply( preconditioner )
    else:
        P = preconditioner
     
    [solution, residuals] = internalCG( M, rhs, P, maximumNumberOfIterations, tolerance );
    
    return [solution, residuals] if residualNorms else solution

def makeScalars( n, value=0.0 ):
    return [ScalarDouble( value ) for _ in range( n )]
    
def writeBasisOutput(basis, postmesh=None, writer=VtuOutput("output.vtu"), processors=[]):
    kwargs = {'basis': basis, 'writer' : writer}
    
    if postmesh is not None:
        kwargs['postmesh'] = postmesh
    if len(processors) > 0:
        convert = lambda p : type(p).__name__[:-2] != 'ElementProcessor'
        kwargs['processors'] = [(convertToElementProcessor(p) if convert(p) else p) for p in processors]
            
    internalWriteBasisOutput(**kwargs)
 
def writeMeshOutput(mesh, postmesh=None, writer=VtuOutput("output.vtu"), processors=[]):
    kwargs = {'mesh': mesh, 'writer' : writer}
    
    if postmesh is not None:
        kwargs['postmesh'] = postmesh
    if len(processors) > 0:
        kwargs['processors'] = processors
            
    internalWriteMeshOutput(**kwargs)
 
del os, sys, path, defineWithDimensionList, function_
