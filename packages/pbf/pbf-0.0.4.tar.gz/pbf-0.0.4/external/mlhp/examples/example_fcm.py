import mlhp

D = 3

print( "1. Setting up mesh and basis", flush=True )

refinementDepth = 0
polynomialDegree = 2
nelements = [10] * D
lengths = [1.0] * D

alphaFCM = 1e-3 # needs better preconditioning

domain = mlhp.invert( mlhp.makeImplicitCube( [0.0,0.101,0.101], [1.0, 0.899, 0.899] ) )

strategy = mlhp.refineTowardsBoundary( domain, refinementDepth )

grid = mlhp.makeRefinedGrid( nelements, lengths )
grid.refine( strategy )

basis = mlhp.makeHpTensorSpace( grid, polynomialDegree, nfields=D )

print( "2. Computing dirichlet boundary conditions", flush=True )

dirichletFunction = mlhp.makeConstantFunction( D, 0.0 )

dirichlet = mlhp.integrateDirichletDofs( [dirichletFunction]*3, basis, [0] )

print( "3. Setting up physics", flush=True )

E = mlhp.makeConstantFunction( D, 200 * 1e9 )
nu = mlhp.makeConstantFunction( D, 0.3 )
rhs = mlhp.makeConstantFunction( D, [0.0, 0.0, 78.5 * 1e3] )

kinematics = mlhp.makeSmallStrainKinematics( D ) 
constitutive = mlhp.makeIsotropicElasticMaterial( E, nu )
integrand = mlhp.makeIntegrand( kinematics, constitutive, rhs )

print( "4. Allocating linear system", flush=True )

matrix = mlhp.allocateUnsymmetricSparseMatrix( basis, dirichlet[0] )
vector = mlhp.allocateVectorWithSameSize( matrix )

print( "5. Integrating linear system", flush=True )

quadrature = mlhp.makeMomentFittingQuadrature( domain, 
    depth=polynomialDegree + 1, epsilon=alphaFCM )

mlhp.integrateOnDomain( basis, integrand, [matrix, vector], 
    dirichletDofs=dirichlet, quadrature=quadrature )

print( "6. Solving linear system", flush=True )

P = mlhp.makeAdditiveSchwarzPreconditioner( matrix, basis, dirichlet[0] )
#P = mlhp.makeDiagonalPreconditioner( matrix )

interiorDofs, norms = mlhp.cg( matrix, vector, preconditioner=P, maxit=1000, residualNorms=True )

allDofs = mlhp.inflateDofs( interiorDofs, dirichlet )

print( "7. Postprocessing solution", flush=True )

processors = [mlhp.makeSolutionProcessor( D, allDofs, "Displacement" ),
              mlhp.makeFunctionProcessor( domain )]

postmesh = mlhp.createGridOnCells( [polynomialDegree + 3] * D )
writer = mlhp.PVtuOutput( filename="outputs/linear_elasticity" )
            
mlhp.writeBasisOutput( basis, postmesh, writer, processors )
