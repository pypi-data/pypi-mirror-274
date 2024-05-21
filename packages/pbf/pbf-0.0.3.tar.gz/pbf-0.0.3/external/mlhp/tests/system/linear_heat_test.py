# This file is part of the mlhp project. License: See LICENSE

import mlhp
import unittest

def makeRefinement( sourcePosition ):
    
    refinement1Radii = [0.096, 0.048, 0.048]
    refinement2Radii = [0.052, 0.016, 0.016]

    center1 = [sourcePosition[0] - 0.6 * refinement1Radii[0]] + sourcePosition[1:]
    center2 = [sourcePosition[0] - 0.3 * refinement2Radii[0]] + sourcePosition[1:]
    
    domain1 = mlhp.makeImplicitEllipsoid( center1, refinement1Radii )
    domain2 = mlhp.makeImplicitEllipsoid( center2, refinement2Radii )
    
    refinement1 = mlhp.refineInsideDomain( domain1, 1 )
    refinement2 = mlhp.refineInsideDomain( domain2, 2 )
    
    return mlhp.refinementOr( refinement1, refinement2 )
    
class LinearHeatTest ( unittest.TestCase ):
    def test_3D(self):
        
        D = 3
        theta = 0.5
        nsteps = 24
        
        lengths = [1.0, 0.4, 0.1]
        nelements = [10, 4, 1]
        degrees = [2, 2, 2]
        resolution = [2, 2, 2]
        
        duration = 1.0
        
        capacity = 1.0
        conductivity = 0.008
        sourceSigma = 0.02
        
        path = mlhp.makeAmLinearHeatPath( lengths )
        intensity = mlhp.makeAmLinearHeatIntensity( )
        
        initial = mlhp.makeConstantFunction( D, 0.0 )
        
        dirichletSide = [i for i in range( 2 * D - 1 )]
        
        source = mlhp.makeAmLinearHeatSource( D, path, intensity, sourceSigma )
            
        solution = mlhp.makeAmLinearHeatSolution( D, path, intensity, 
            capacity, conductivity, sourceSigma, duration / 10.0, 0.0 );

        # Time integration
        grid0 = mlhp.makeRefinedGrid( nelements, lengths )
        grid0.refine( makeRefinement( path( 0.0 ) ) )
        
        basis0 = mlhp.makeHpTrunkSpace( grid0, mlhp.LinearGrading( degrees ) )

        dofs0 = mlhp.projectOnto( basis0, initial )
        
        processors = [mlhp.makeSolutionProcessor( D, dofs0, "Temperature" ),
                      mlhp.makeFunctionProcessor( mlhp.sliceLast( solution, 0.0 ), "Analytical" ),
                      mlhp.makeFunctionProcessor( mlhp.sliceLast( source, 0.0 ), "Source" )]
                           
        postmesh = mlhp.createGridOnCells( resolution )
        writer = mlhp.VtuOutput( f'outputs/linear_heat_{0}' )
        
        mlhp.writeBasisOutput( basis0, postmesh, writer, processors )        
        
        dt = duration / nsteps
        ndof = 0
        integrals = [0.0, 0.0, 0.0]
        
        for istep in range( nsteps ):
            time0, time1 = istep * dt, ( istep + 1 ) * dt
            
            grid1 = mlhp.makeRefinedGrid( nelements, lengths );
            grid1.refine( makeRefinement( path( time1 ) ) );
            
            basis1 = mlhp.makeHpTrunkSpace( grid1, mlhp.LinearGrading( degrees ) );

            print( "Time step " + str(istep + 1) + " / " + str( nsteps ) +
                   " (" + str( basis1.ndof( ) ) + " number of unknowns)" );
               
            dirichlet = mlhp.integrateDirichletDofs( mlhp.sliceLast( solution, time1 ), basis1, dirichletSide )

            matrix = mlhp.allocateUnsymmetricSparseMatrix( basis1, dirichlet[0] );
            vector = mlhp.allocateVectorWithSameSize( matrix )
            
            integrand = mlhp.makeTransientPoissonIntegrand( mlhp.makeConstantFunction( D + 1, capacity ),
                mlhp.makeConstantFunction( D + 1, conductivity ), source, dofs0, [time0, time1], theta )
                         
            mlhp.integrateOnDomain( basis0, basis1, integrand, [matrix, vector], dirichletDofs=dirichlet )
            
            dofs1 = mlhp.inflateDofs( mlhp.makeCGSolver( )( matrix, vector ), dirichlet )
            
            # Error integration (excluding initial condition         
            l2ErrorIntegrand = mlhp.makeL2ErrorIntegrand( dofs1, mlhp.sliceLast( solution, time1 ) );
            l2Integrals = mlhp.makeScalars( 3 )
            
            mlhp.integrateOnDomain( basis1, l2ErrorIntegrand, l2Integrals )
            
            factor = dt if istep + 1 < nsteps else dt / 2.0
            
            integrals = [E + factor * Ec.get( ) for E, Ec in zip( integrals, l2Integrals )]
                     
            # Vtu postprocessing
            processors = [mlhp.makeSolutionProcessor( D, dofs1, "Temperature" ),
                          mlhp.makeFunctionProcessor( mlhp.sliceLast( solution, time1 ), "Analytical" ),
                          mlhp.makeFunctionProcessor( mlhp.sliceLast( source, time1 ), "Source" )]
            
            postmesh = mlhp.createGridOnCells( resolution )
            writer = mlhp.VtuOutput( f'outputs/linear_heat_{istep + 1}' )
                
            mlhp.writeBasisOutput( basis1, postmesh, writer, processors )             
            
            ndof += basis1.ndof( )
            dofs0 = dofs1
            basis0 = basis1
        
        self.assertEqual(ndof, 33436)
        self.assertAlmostEqual(integrals[0], 2.7342053949**2, delta=1e-8)
        self.assertAlmostEqual(integrals[1], 2.7532175961**2, delta=1e-8)
        self.assertAlmostEqual(integrals[2], 0.0644606778**2, delta=1e-7)
        self.assertAlmostEqual(integrals[2] / integrals[1], 0.0234128526**2, delta=1e-7)
        
