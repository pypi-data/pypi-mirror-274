// This file is part of the mlhpbf project. License: See LICENSE

#ifndef MLHPBF_THERMAL_HPP
#define MLHPBF_THERMAL_HPP

#include "laser.hpp"

namespace mlhp
{

template<size_t D>
struct ThermalState
{
    size_t index;
    double time;

    std::shared_ptr<MultilevelHpBasis<D>> basis;
    std::shared_ptr<AbsHierarchicalGrid<D>> grid;
    std::vector<double> dofs;
    ThermoplasticHistory<D> history;
};

template<size_t D> 
struct ThermalProblem;

template<size_t D>
using ThermalRefinement = std::function<RefinementFunction<D>( const ThermalProblem<D>& thermal,
                                                               const ThermalState<D>& state0,
                                                               const ThermalState<D>& state1 )>;

template<size_t D>
using ThermalPostprocessing = std::function<void( const ThermalProblem<D>& thermal,
                                                  const ThermalState<D>& state )>;

template<size_t D>
using ThermalDirichletBC = std::function<DofIndicesValuesPair( const ThermalState<D>& state )>;

template<size_t D>
using VolumeSource = spatial::ScalarFunction<D + 1>;

template<size_t D>
using HeatFlux = spatial::ScalarFunction<D>;

template<size_t D>
struct ThermalProblem
{
    std::shared_ptr<ProblemSetup<D>> general;

    double ambientTemperature = 25.0 * Units::C;

    //double emissivity = 0.0;// 0.47;
    //double convectionCoefficient = 0.0; //1e-5 * W / ( mm * mm * C );

    ThermalRefinement<D> refinement = makeUniformRefinement<D>( 0 );
    size_t degree = 1;
    double timeStep;

    std::variant<VolumeSource<D>, HeatFlux<D>> source = spatial::constantFunction<D + 1>( 0.0 );

    std::vector<ThermalDirichletBC<D>> dirichlet = { };

    // Otherwise just set Dirichlet dofs
    bool imposeDirichletInInitialCondition = true; 

    auto initialState( ThermoplasticHistory<D>&& history0 ) const;

    auto step( const ThermalState<D>& state0,
               double dt ) const;

    ThermalPostprocessing<D> postprocess = utilities::doNothing( );
};

template<size_t D>
ThermalDirichletBC<D> makeTemperatureBC( size_t iface, spatial::ScalarFunction<D + 1> function )
{
    return [=]( const ThermalState<D>& tstate )
    {
        auto sliced = spatial::sliceLast<D + 1>( function, tstate.time );

        return boundary::boundaryDofs( sliced, *tstate.basis, { iface } );
    };
}

template<size_t D>
ThermalDirichletBC<D> makeTemperatureBC( size_t iface, double value = 0.0 )
{
    return makeTemperatureBC<D>( iface, spatial::constantFunction<D + 1>( value ) );
}

template<size_t D> inline
auto ThermalProblem<D>::initialState( ThermoplasticHistory<D>&& history0 ) const
{
    auto createBasisAndComputeDofs = [this]( ThermalState<D>& state, 
                                             const RefinementFunction<D>& refine )
    {
        auto initialTemperature = spatial::constantFunction<D>( ambientTemperature );

        state.grid = makeRefinedGrid<D>( general->baseGrid );
        state.grid->refine( refine );

        state.basis = makeHpBasis<typename ProblemSetup<D>::AnsatzSpace>( state.grid, degree );

        auto components = std::vector<DofIndicesValuesPair> { };

        for( auto& condition : dirichlet )
        {
            components.push_back( condition( state ) );
        }

        auto dirichletDofs = boundary::combine( components );

        if( imposeDirichletInInitialCondition )
        {
            auto integrand = makeL2ProjectionIntegrand<D>( initialTemperature );
            auto matrix = allocateMatrix<linalg::UnsymmetricSparseMatrix>( *state.basis, dirichletDofs.first );
            auto rhs = std::vector<double>( matrix.size1( ), 0.0 );

            integrateOnDomain( *state.basis, integrand, { matrix, rhs }, dirichletDofs );

            state.dofs = boundary::inflate( linalg::makeCGSolver( )( matrix, rhs ), dirichletDofs );
        }
        else
        {
            state.dofs = projectOnto( *state.basis, initialTemperature );
            state.dofs = boundary::inflate( algorithm::remove( state.dofs, dirichletDofs.first ), dirichletDofs );
        }
    };


    auto state0a = ThermalState<D> { 0, 0.0 };
    state0a.history = std::move( history0 );

    createBasisAndComputeDofs( state0a, makeUniformRefinement<D>( )( ) );

    auto state0b = ThermalState<D> { 0, 0.0 };
    state0b.history = state0a.history;

    createBasisAndComputeDofs( state0b, refinement( *this, state0a, state0b ) );

    return state0b;
}

template<size_t D> inline
auto makeThermalInitializationIntegrand( auto& materials,
                                         const spatial::ScalarFunction<D + 1>& source,
                                         const ThermoplasticHistory<D>& history0,
                                         const std::vector<double>& dofs0,
                                         double time0,
                                         double deltaT,
                                         double theta )
{
    auto evaluate = [=, &history0]( const LocationMap& locationMap0,
                                    const LocationMap&,
                                    const BasisFunctionEvaluation<D>& shapes0,
                                    const BasisFunctionEvaluation<D>& shapes1,
                                    AlignedDoubleVectors& targets,
                                    double weightDetJ )
    {
        auto ndof = shapes1.ndof( );
        auto nblocks = shapes1.nblocks( );
        auto ndofpadded = shapes1.ndofpadded( );

        auto N = shapes1.noalias( 0, 0 );
        auto dN = shapes1.noalias( 0, 1 );

        auto history = history0( shapes1.xyz( ) );

        MLHP_CHECK( history != nullptr, "No history found." );

        auto& material = materialFor( materials, history->materialType );
        
        auto u0 = evaluateSolution( shapes0, locationMap0, dofs0 );
        auto du0 = evaluateGradient( shapes0, locationMap0, dofs0 );

        auto [k0, dk0] = material.heatConductivity( u0 );

        auto kscaling0 = array::make<D>( 1.0 );
        auto sourceTheta = 0.0;

        if( theta != 1.0  )
        {
            sourceTheta += ( 1.0 - theta ) * source( array::insert( shapes1.xyz( ), D, time0 ) );
        }

        if( theta != 0.0  )
        {
            sourceTheta += theta * source( array::insert( shapes1.xyz( ), D, time0 + deltaT ) );
        }

        auto conductivities0 = array::multiply( kscaling0, k0 * ( 1.0 - theta ) );        
        auto flux = array::multiply( conductivities0, du0 );

        linalg::elementRhs( targets[0].data( ), ndof, nblocks, [&]( size_t i )
        {
            double value = -N[i] * sourceTheta;

            for( size_t axis = 0; axis < D; ++axis )
            {
                value += dN[axis * ndofpadded + i] * flux[axis];
            }

            return value * weightDetJ;
        } );
    };

    auto types = std::vector { AssemblyType::Vector };

    return BasisProjectionIntegrand<D>( types, DiffOrders::FirstDerivatives, evaluate );
}

template<size_t D> inline
auto makeEvaluationFunction( const std::shared_ptr<const AbsBasis<D>>& basis,
                             const std::vector<double>& dofs )
{
    auto create = basis->mesh( ).createBackwardMappingFactory( );

    // Data needed on each thread for solution evaluation 
    struct Cache
    {
        std::vector<DofIndex> locationMap;
        std::unique_ptr<AbsBackwardMapping<D>> backwardMapping;
        BasisFunctionEvaluation<D> shapes;
        BasisEvaluationCache<D> basisCache;
    };

    // Claim basis ownership and copy dofs
    return [=, createBackwardMapping = std::move(create)]( std::array<double, D> xyz )
    {
        thread_local std::unique_ptr<Cache> cache;

        // Create new cache if it doesn't exist or was allocated for a different basis
        //if( !cache || &cache->backwardMapping->mesh( ) != &basis->mesh( ) || 
        //    cache->backwardMapping->mesh( ).ncells( ) != basis->nelements( ) )
        {
            cache = std::make_unique<Cache>( );
            cache->backwardMapping = createBackwardMapping( );
            cache->basisCache = basis->createEvaluationCache( );
        }

        auto value = 0.0;

        // Find element index and local coordinates
        if( auto result = cache->backwardMapping->map( xyz ); result )
        {
            utilities::resize0( cache->locationMap );

            auto [ielement, rst] = *result;

            // Obtain location map and evaluate basis functions
            basis->locationMap( ielement, cache->locationMap );
            basis->prepareEvaluation( ielement, 0, cache->shapes, cache->basisCache );
            basis->evaluateSinglePoint( rst, cache->shapes, cache->basisCache );

            // Compute product of basis functions with element dofs
            value = evaluateSolution( cache->shapes, cache->locationMap, dofs );
        }
        
        return value;
    };
}

template<size_t D> inline
auto makeTimeSteppingThermalIntegrand( auto& materials,
                                       const ThermoplasticHistory<D>& historyContainer,
                                       const std::vector<double>& projectedDofs0,
                                       const std::vector<double>& dofs1,
                                       double dt,
                                       double theta )
{
    auto evaluate = [=, &historyContainer, &dofs1]( const BasisFunctionEvaluation<D>& shapes,
                                                    const LocationMap& locationMap, 
                                                    AlignedDoubleVectors& targets, 
                                                    AlignedDoubleVector&,
                                                    double weightDetJ )
    {
        auto ndof = shapes.ndof( );
        auto nblocks = shapes.nblocks( );
        auto ndofpadded = shapes.ndofpadded( );

        auto N = shapes.noalias( 0, 0 );
        auto dN = shapes.noalias( 0, 1 );

        auto u0 = evaluateSolution( shapes, locationMap, projectedDofs0 );
        auto u1 = evaluateSolution( shapes, locationMap, dofs1 );
        auto du1 = evaluateGradient( shapes, locationMap, dofs1 );

        auto history = historyContainer( shapes.xyz( ) );

        MLHP_CHECK( history != nullptr, "No history found." );

        auto& material = materialFor( materials, history->materialType );

        auto [rho0, drho0] = material.density( u0 );
        auto [rho1, drho1] = material.density( u1 );

        auto [c0, dc0] = material.specificHeatCapacity( u0 );
        auto [c1, dc1] = material.specificHeatCapacity( u1 );
        auto [k1, dk1] = material.heatConductivity( u1 );
        auto [L0, dL0, ddL0] = evaluatePhaseTransition( material, u0 );
        auto [L1, dL1, ddL1] = evaluatePhaseTransition( material, u1 );

        auto kscaling1 = array::make<D>( 1.0 );
        auto cTheta = ( 1.0 - theta ) * c0 * rho0 + theta * c1 * rho1;
        auto mass = ( cTheta + theta * ( dc1 * rho1 + c1 * drho1 ) * ( u1 - u0 ) + dL1 ) / dt;

        auto conductivities1 = array::multiply( kscaling1, k1 * theta );

        linalg::symmetricElementLhs( targets[0].data( ), ndof, nblocks, [&]( size_t i, size_t j )
        {
            auto value = N[i] * N[j] * mass;

            for( size_t axis = 0; axis < D; ++axis )
            {
                value += dN[axis * ndofpadded + i] * dN[axis * ndofpadded + j] * conductivities1[axis];

            } // component

            return value * weightDetJ;
        } );

        auto dc = cTheta * ( u1 - u0 ) / dt;
        auto dL = ( L1 - L0 ) / dt;

        auto fluxes = array::multiply( conductivities1, du1 );

        linalg::elementRhs( targets[1].data( ), ndof, nblocks, [&]( size_t i )
        {
            double value = N[i] * ( dc + dL );

            for( size_t axis = 0; axis < D; ++axis )
            {
                value += dN[axis * ndofpadded + i] * fluxes[axis];
            }

            return value * weightDetJ;
        } );
    };

    auto types = std::vector { AssemblyType::SymmetricMatrix, AssemblyType::Vector };

    return DomainIntegrand<D>( DiffOrders::FirstDerivatives, types, evaluate );
}

using NonlinearFlux = std::function<std::array<double, 2>( double T )>;

template<size_t D> inline
auto makeNonlinearFluxIntegrand( const NonlinearFlux& flux,
                                 const std::vector<double>& dofs )
{
    auto evaluate = [=]( const BasisFunctionEvaluation<D>& shapes,
                         const LocationMap& locationMap,
                         std::array<double, D> /* normal */,
                         AlignedDoubleVectors& targets,
                         double weightDetJ )
    {
        auto u = evaluateSolution( shapes, locationMap, dofs );

        auto [f, df] = flux( u );

        auto N = shapes.noalias( 0, 0 );
        auto ndof = shapes.ndof( );
        auto nblocks = shapes.nblocks( );

        auto left = df * weightDetJ;
        auto right = f * weightDetJ;

        linalg::symmetricElementLhs( targets[0].data( ), ndof, nblocks, 
                                     [&]( size_t idof, size_t jdof )
        { 
            return N[idof] * N[jdof] * left;
        } );

        linalg::elementRhs( targets[1].data( ), ndof, nblocks, [&]( size_t idof )
        { 
            return N[idof] * right;
        } );
    };

    auto types = std::vector { AssemblyType::SymmetricMatrix, AssemblyType::Vector };

    return SurfaceIntegrand<D>( types, DiffOrders::Shapes, evaluate );
}

template<size_t D> inline
auto makeConvectionRadiationIntegrand( const std::vector<double>& dofs, 
                                       double emissivity,
                                       double conductivity,
                                       double ambientTemperature,
                                       double theta )
{
    MLHP_CHECK( theta == 1.0, "Yep." );

    auto S = 5.670374419e-8 * Units::W / ( std::pow( Units::m, 2 ) * std::pow( Units::C, 4 ) );

    auto flux = [=]( double T ) -> std::array<double, 2>
    {
        auto dT = T - ambientTemperature;
        auto pT = T + ambientTemperature;

        auto f = conductivity * dT + S * emissivity * dT * dT * pT * pT;
        auto df = conductivity + S * emissivity * 2.0 * dT * pT * ( pT + dT );
        
        return { f, df };
    };

    return makeNonlinearFluxIntegrand<D>( flux, dofs );
}

template<size_t D>
auto makeSteadyStateThermalIntegrand( auto& materials,
                                      const spatial::ScalarFunction<D>& sourceFunction,
                                      const ThermoplasticHistory<D>& historyContainer,
                                      const std::vector<double>& dofs,
                                      std::array<double, D> laserVelocity )
{

    auto evaluate = [=, &historyContainer, &dofs]( const BasisFunctionEvaluation<D>& shapes,
                                const LocationMap& locationMap,
                                AlignedDoubleVectors& targets, 
                                AlignedDoubleVector&, 
                                double weightDetJ )
    {
        auto ndof = shapes.ndof( );
        auto nblocks = shapes.nblocks( );
        auto ndofpadded = shapes.ndofpadded( );

        auto N = shapes.noalias( 0, 0 );
        auto dN = shapes.noalias( 0, 1 );

        auto u = evaluateSolution( shapes, locationMap, dofs );
        auto du = evaluateGradient( shapes, locationMap, dofs );

        auto history = historyContainer( shapes.xyz( ) );

        MLHP_CHECK( history != nullptr, "No history found." );

        auto& material = materialFor( materials, history->materialType );

        auto [rho, drho] = material.density( u );
        auto [c, dc] = material.specificHeatCapacity( u );
        auto [k, dk] = material.heatConductivity( u );
        auto [L, dL, ddL] = evaluatePhaseTransition( material, u );

        auto m = c * rho + L * rho;
        auto dm = dc * rho + c * drho + dL * rho + L * drho;
        auto source = sourceFunction( shapes.xyz( ) );

        linalg::unsymmetricElementLhs( targets[0].data( ), ndof, nblocks, [&]( size_t i, size_t j )
        {
            auto advection = 0.0;
            auto diffusion = 0.0;
                        
            for( size_t axis = 0; axis < D; ++axis )
            {
                auto dNj = dN[axis * ndofpadded + j];

                advection += N[i] * laserVelocity[axis] * ( m * dNj + dm * du[axis] * N[j] );
            }

            for( size_t axis = 0; axis < D; ++axis )
            {
                auto dNi = dN[axis * ndofpadded + i];
                auto dNj = dN[axis * ndofpadded + j];

                diffusion += dNi * ( k * dNj + dk * du[axis] * N[j] );
            }

            return ( diffusion - advection ) * weightDetJ;
        } );

        linalg::elementRhs( targets[1].data( ), ndof, nblocks, [&]( size_t i )
        {
            auto advection = 0.0;
            auto diffusion = 0.0;
            
            for( size_t axis = 0; axis < D; ++axis )
            {
                advection += N[i] * ( laserVelocity[axis] * m * du[axis] );
            }

            for( size_t axis = 0; axis < D; ++axis )
            {
                diffusion += dN[axis * ndofpadded + i] * k * du[axis];
            }

            return ( diffusion - advection - N[i] * source ) * weightDetJ;
        } );
    };

    auto types = std::vector { AssemblyType::UnsymmetricMatrix, AssemblyType::Vector };

    return DomainIntegrand<D>( DiffOrders::FirstDerivatives, types, evaluate );
}

template<size_t D> inline
auto ThermalProblem<D>::step( const ThermalState<D>& state0,
                              double dt ) const
{
    // Initialize new state
    auto state1 = ThermalState<D> { state0.index + 1, state0.time + dt };

    state1.history = state0.history;
    state1.grid = makeRefinedGrid<D>( general->baseGrid );
    state1.grid->refine( refinement( *this, state0, state1 ) );
    state1.basis = makeHpBasis<typename ProblemSetup<D>::AnsatzSpace>( state1.grid, degree );
    
    std::cout << "    thermal problem: " << state1.basis->nelements() <<
        " elements, " << state1.basis->ndof() << " dofs" << std::endl;
    
    // Prepare Dirichlet dofs
    auto components = std::vector<DofIndicesValuesPair> { };

    for( auto& condition : dirichlet )
    {
        components.push_back( condition( state1 ) );
    }

    auto dirichletDofs = boundary::combine( components );
    
    // Project solution to new discretization
    auto solve = linalg::makeCGSolver( );

    {
        auto M = allocateMatrix<linalg::UnsymmetricSparseMatrix>( *state1.basis );
        auto d = std::vector<double>( M.size1( ), 0.0 );

        auto l2Integrand = makeL2BasisProjectionIntegrand<D>( state0.dofs );
        
        integrateOnDomain( *state0.basis, *state1.basis, l2Integrand, { M, d },
            StandardQuadrature<D> { }, makeIntegrationOrderDeterminor<D>( 1 ) );

        state1.dofs = solve( M, d );
    }

    auto projectedDofs0 = state1.dofs;

    // Prepare for Newton iterations
    auto df = allocateMatrix<linalg::UnsymmetricSparseMatrix>( *state1.basis, dirichletDofs.first );
    auto f = std::vector<double>( df.size1( ), 0.0 );
    auto f0 = std::vector<double>( df.size1( ), 0.0 );
    auto dirichletIncrement = dirichletDofs;

    auto theta = 1.0;

    MLHP_CHECK( std::holds_alternative<VolumeSource<D>>( source ), "Heat flux." );

    VolumeSource<D> volumeSource = std::get<0>( source );

    auto projectionIntegrand = makeThermalInitializationIntegrand<D>( *general, volumeSource, 
        state0.history, state0.dofs, state0.time, dt, theta );

    integrateOnDomain( *state0.basis, *state1.basis, projectionIntegrand, { f0 }, dirichletDofs );
    
    auto norm0 = 0.0;
    std::cout << "    || F || --> " << std::flush;

    // Newton-Raphson iterations
    for( size_t i = 0; i < 40; ++i )
    {
        std::copy( f0.begin( ), f0.end( ), f.begin( ) );
        std::fill( df.data( ), df.data( ) + df.nnz( ), 0.0 );
              
        for( size_t idof = 0; idof < dirichletDofs.first.size( ); ++idof )
        {
            dirichletIncrement.second[idof] = -dirichletDofs.second[idof] +
                state1.dofs[dirichletDofs.first[idof]];
        }    

        auto domainIntegrand = makeTimeSteppingThermalIntegrand<D>( *general, 
            state1.history, projectedDofs0, state1.dofs, state1.time - state0.time, theta );

        //auto surfaceDistributor = boundary::QuadratureOnMeshFaces<D>( *tgrid1, { boundary::top }, degree + 1 );
        //auto boundaryIntegrand = makeConvectionRadiationIntegrand<D>( tdofs1, 
        //    emissivity, convectionCoefficient, ambientTemperature, theta );

        auto quadrature = makeIntegrationOrderDeterminor<D>( 1 ); // p + 1 
        auto partitioner = StandardQuadrature<D> { };
        auto materialGridPartitioner = MeshProjectionQuadrature<D>( *state1.history.grid, partitioner );

        integrateOnDomain( *state1.basis, domainIntegrand, { df, f }, materialGridPartitioner, quadrature, dirichletIncrement );

        double norm1 = std::sqrt( std::inner_product( f.begin( ), f.end( ), f.begin( ), 0.0 ) );

        norm0 = i == 0 ? norm1 : norm0;

        std::cout << std::scientific << std::setprecision( 2 ) << norm1 << " " << std::flush;

        auto dx = boundary::inflate( solve( df, f ), dirichletIncrement );

        std::transform( state1.dofs.begin( ), state1.dofs.end( ), dx.begin( ), state1.dofs.begin( ), std::minus<double> { } );
                    
        if( i == 0 )
		    state1.history = updateHistory( state0.history, *state1.basis, state1.dofs );

        if( norm1 / norm0 <= 1e-6 || norm1 < 1e-11 ) break;
        if( ( i + 1 ) % 6 == 0 ) std::cout << "\n                ";
    }

    std::cout << std::endl;

    return state1;
}

template<size_t D> inline
auto makeThermalPostprocessing( const std::string& filebase,
                                size_t vtuinterval,
                                bool writeHistory = true )
{
    auto postprocess = [=]( const ThermalProblem<D>& thermal,
                            const ThermalState<D>& state )
    {
        if( state.index % vtuinterval == 0 )
        {
            MLHP_CHECK( std::holds_alternative<VolumeSource<D>>( thermal.source ), "Heat flux." );

            auto tprocessors = std::tuple
            {
                makeSolutionProcessor<D>( state.dofs, "Temperature" ),
                makeFunctionProcessor<D>( spatial::sliceLast( std::get<0>( thermal.source ), state.time ), "Source" ),
                //laser::makeRefinementLevelFunctionPostprocessor<D>( thermal.general->laserTrack, thermal.refinement, state.time )
            };
     
            auto meshProvider = createGridOnCells( array::makeSizes<D>( thermal.degree ) );
            auto toutput = PVtuOutput { filebase + "thermal_" + std::to_string( state.index / vtuinterval ) };

            writeOutput( *state.basis, meshProvider, std::move( tprocessors ), toutput );
     
            if( writeHistory )
            {
                auto converted = std::vector<std::vector<double>>( 1, 
                    std::vector<double>( state.history.data.size( ) ) );

                for( CellIndex icell = 0; icell < state.history.data.size( ); ++ icell )
                {
                    converted[0][icell] = static_cast<double>( state.history.data[icell].materialType );
                }

                auto hprocessors = std::tuple
                {
                    makeCellDataProcessor<D>( converted[0], "MaterialType" ),
                };

                auto materialMeshProvider = createGridOnCells( array::makeSizes<D>( 1 ), 
                    PostprocessTopologies::Volumes );

                auto houtput = PVtuOutput { filebase + "material_" + std::to_string( state.index / vtuinterval ) };
            
                writeOutput( *state.history.grid, materialMeshProvider, std::move( hprocessors ), houtput );
            }
        }
    };

    return ThermalPostprocessing<D> { std::move( postprocess ) };
}

template<size_t D> inline
auto computeThermalProblem( const ThermalProblem<D>& thermal,
                            ThermoplasticHistory<D>&& history0 )
{
    auto duration = thermal.general->duration;

    auto nsteps = static_cast<size_t>( std::ceil( duration / thermal.timeStep ) );
    auto dt = duration / nsteps;

    std::cout << "Integrating thermal problem:" << std::endl;
    std::cout << "    duration        = " << duration << std::endl;
    std::cout << "    number of steps = " << nsteps << std::endl;
    std::cout << "    step size       = " << dt << std::endl;
    std::cout << "    base mesh size  = " << thermal.general->baseGrid->ncells( ) << std::endl;

    auto tstate0 = thermal.initialState( std::move( history0 ) );

    thermal.postprocess( thermal, tstate0 );

    for( size_t istep = 0; istep < nsteps; ++istep )
    {
        std::cout << "Time step " << istep + 1 << " / " << nsteps << std::endl;

        auto tstate1 = thermal.step( tstate0, dt );

        thermal.postprocess( thermal, tstate1 );

        tstate0 = std::move( tstate1 );
    } 

    return tstate0;
}

} // namespace mlhp

#endif // MLHPBF_THERMAL_HPP
