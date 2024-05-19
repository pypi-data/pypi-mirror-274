// This file is part of the mlhpbf project. License: See LICENSE

#include "mlhp/pbf.hpp"
#include "main_test.hpp"

namespace mlhp
{

TEST_CASE( "j2plasticity_test" )
{
    static constexpr size_t D = 3;

    auto density = []( double T ) -> std::array<double, 2>
    {
        return { 1.0, 0.0 };
    };

    auto cp = []( double T ) -> std::array<double, 2>
    {
        return { 1.0, 0.0 };
    };

    auto kappa = []( double T ) -> std::array<double, 2>
    {
        return { 1.0, 0.0 };
    };


    auto expCoeff = []( double T ) -> std::array<double, 2>
    {
        return { 1.0, 0.0 };
    };

    auto youngsModulus = []( double T ) -> std::array<double, 2>
    {
        return { 206.9, 0.0 };//{ 206.9 * Units::GPa, 0.0};
    };

    auto poissonsRatio = []( double T ) -> std::array<double, 2>
    {
        return { 0.29, 0.0};
    };

    auto yieldStress = []( double T ) -> std::array<double, 2>
    {
        return { 0.45, 0.0 }; // { 0.45 * Units::GPa, 0.0 };
    };

    auto hardening = []( double T ) -> std::array<double, 2>
    {
        return { 0.0, 0.0 }; // { 0.2, 0.0 };
    };

    Material steelMaterial =
    {
        .initialized = true,
        .name = "Steel",
        .density = density,
        .specificHeatCapacity = cp,
        .heatConductivity = kappa,
        .solidTemperature = 1290.0 * Units::C,
        .liquidTemperature = 1350.0 * Units::C,
        .latentHeatOfFusion = 2.8e5 * Units::J / Units::kg,
        .thermalExpansionCoefficient = expCoeff,
        .youngsModulus = youngsModulus,
        .poissonRatio = poissonsRatio,
        .yieldStress = yieldStress,
        .hardeningParameter = hardening,
        .plasticModelSelector = 0.0,
    };
    
    auto baseMeshTicks = std::array
    {
        std::vector { 0.0 * Units::mm, 0.3 * Units::mm, 0.5 * Units::mm, 0.7 * Units::mm,
                      0.9 * Units::mm, 1.2 * Units::mm, 1.5 * Units::mm, 2.0 * Units::mm, 
                      2.5 * Units::mm, 3.5 * Units::mm, 5.0 * Units::mm },
        std::vector { 0.0 * Units::mm, 0.2 * Units::mm, 0.4 * Units::mm, 0.7 * Units::mm, 
                      1.0 * Units::mm, 1.5 * Units::mm, 2.0 * Units::mm, 2.5 * Units::mm, 
                      3.0 * Units::mm, 3.5 * Units::mm, 4.0 * Units::mm, 4.5 * Units::mm, 
                      5.0 * Units::mm, 6.0 * Units::mm, 8.0 * Units::mm, 12.0 * Units::mm, 
                      15.0 * Units::mm },
        std::vector {-1.0 * Units::mm, 0.0 * Units::mm }
    };

    
    for( size_t axis = 0; axis < 2; ++axis )
    {
        for( int i = 0; i + 1 < baseMeshTicks[axis].size( ); i += 2 )
        {
            baseMeshTicks[axis].insert( baseMeshTicks[axis].begin( ) + i + 1, 
                0.5 * baseMeshTicks[axis][i] + 0.5 * baseMeshTicks[axis][i + 1] );
        }
    }

    for( size_t axis = 0; axis < 2; ++axis )
    {
        for( int i = 0; i + 1 < baseMeshTicks[axis].size( ); i += 2 )
        {
            baseMeshTicks[axis].insert( baseMeshTicks[axis].begin( ) + i + 1, 
                0.5 * baseMeshTicks[axis][i] + 0.5 * baseMeshTicks[axis][i + 1] );
        }
    }
    
    for( size_t axis = 0; axis < 2; ++axis )
    {
        for( int i = 0; i + 1 < baseMeshTicks[axis].size( ); i += 2 )
        {
            baseMeshTicks[axis].insert( baseMeshTicks[axis].begin( ) + i + 1, 
                0.5 * baseMeshTicks[axis][i] + 0.5 * baseMeshTicks[axis][i + 1] );
        }
    }

    auto baseGrid = std::make_shared<CartesianGrid<D>>( std::move( baseMeshTicks ) );

    auto general = ProblemSetup<D>
    {
        .buildChamber = baseGrid->boundingBox( ),
        .duration = 1.0,
        .baseplate = steelMaterial,
        .powder = steelMaterial,
        .baseGrid = baseGrid,
    };

    auto sharedSetup = std::make_shared<ProblemSetup<D>>( std::move( general ) );

    auto incrementalDisplacement = []( std::array<double, D + 1> xyzt )
    { 
        auto time = xyzt.back( );
        double maxDispl = 0.17 * Units::mm;

        return maxDispl * time;
    };

    auto fixedBoundaryLength = 0.5 * Units::mm;

    std::function implicitBoundaryFunction = [=](const std::array<double, D> xyz) -> bool
    {
        return xyz[0] < fixedBoundaryLength + std::numeric_limits<double>::epsilon( ) && xyz[1] < std::numeric_limits<double>::epsilon( );
    };

    size_t nseedpoints = 2;

    auto dirichletBoundaryFunction = [=]( size_t ifield, spatial::ScalarFunction<D + 1> function )
    {
        return [=]( const MechanicalState<D>& mstate )
        {
            auto meshCellFacesVct = mesh::facesInsideDomain( mstate.basis->mesh( ), implicitBoundaryFunction, nseedpoints );
            auto sliced = spatial::sliceLast<D + 1>( function, mstate.time );

            return boundary::boundaryDofs<D>( sliced, meshCellFacesVct, *mstate.basis, makeIntegrationOrderDeterminor<D>( ), ifield );
        };
    };

    auto homogeneousDirichlet = spatial::constantFunction<D + 1>( 0.0 );

    auto dirichlet = std::vector<MechanicalDirichletBC<D>>
    {
        dirichletBoundaryFunction( 1, homogeneousDirichlet ),
        makeDisplacementBC<D>( boundary::left, 0 ),
        makeDisplacementBC<D>( boundary::back, 1, incrementalDisplacement ),
        makeDisplacementBC<D>( boundary::top, 2 ),
        makeDisplacementBC<D>( boundary::bottom, 2 ),
    };

    auto levelFunction = [=]( std::array<double, D> xyz )
    {
        auto distance = spatial::distance<D>( { xyz[0], xyz[1] }, { fixedBoundaryLength } );
        auto level = std::max( std::round( 2.7 - 5.0 * distance ), 0.0 );
        level = 0;
        return static_cast<RefinementLevel>( level );
    };

    MechanicalRefinement<D> refineTowardsDirichletBoundary = [=]( auto&& ... ) -> RefinementFunction<D>
    {
        return refineWithLevelFunction<D>( levelFunction, nseedpoints );
    };

    auto mechanical = MechanicalProblem<D>
    {
        .general = sharedSetup,
        .refinement = refineTowardsDirichletBoundary,
        .degree = 1,
        .dirichlet = dirichlet,
        //.residual = { makeTractionBC<D>( boundary::back, std::array { 0.0, 0.002, 0.0 } ) },
        .postprocess = makeMechanicalPostprocessing<D>( "outputs/mlhpbf_tests/j2plasticity_", 1 )
    };

    auto computeReactionForce = [&]( const MechanicalDirichletBC<D>& condition, 
                                     const MechanicalState<D>& state )
    {
        auto boundaryDofIndices = condition( state ).first;
        auto boundaryDofMask = algorithm::indexMask( boundaryDofIndices, state.basis->ndof( ) );
        auto kinematics = makeSmallStrainKinematics<D>( );

        constexpr size_t N = 6;
        constexpr size_t D = 3;

        auto evaluate = [&]( const BasisFunctionEvaluation<D>& shapes,
                             const LocationMap& locationMap, 
                             AlignedDoubleVectors& targets, 
                             AlignedDoubleVector& tmp,
                             double weightDetJ )
        {
            auto ndof = shapes.ndof( );;
            auto ndofpadded = shapes.ndofpadded( );

            tmp.resize( N * ndofpadded );

            std::fill( tmp.begin( ), tmp.end( ), 0.0 );

            auto B = memory::assumeAlignedNoalias( tmp.data( ) );
            auto strainOperator = std::span( B, N * ndofpadded );

            // Compute B matrix from shape function evaluation
            kinematics.evaluate( shapes, std::span<double> { }, std::span<double> { }, strainOperator );

            auto stress = state.history( shapes.elementIndex( ), shapes.rst( ) ).stress;
            
            for( size_t i = 0; i < ndof; i++ )
            {
                if( boundaryDofMask[locationMap[i]] )
                {
                    for( size_t j = 0; j < N; j++)
                    {
                        targets[0][0] -= B[j * ndofpadded + i] * stress[j] * weightDetJ;
                    }
                }
            }
        };

        auto types = std::vector { AssemblyType::Scalar };
        auto domainIntegrand = DomainIntegrand<D> { DiffOrders::FirstDerivatives, types, evaluate };
        auto target = 0.0;

        integrateOnDomain<D>( *state.basis, domainIntegrand, { target } );

        return target;
    };

    mechanical.postprocess = [&]( const MechanicalProblem<D>& mechanical,
                                  const MechanicalState<D>& state )
    {
        makeMechanicalPostprocessing<D>( "outputs/mlhpbf_tests/j2plasticity_", 1  )( mechanical, state );

        auto R = computeReactionForce( dirichlet[0], state );
        auto sigmaBar = 2.0 * R;

        std::cout << "    Reaction force: " << sigmaBar / steelMaterial.yieldStress( 0.0 )[0] << std::endl;
    };

    auto history0 = initializeHistory<D>( sharedSetup->baseGrid, 0.0 * Units::mm, 0 );
    auto timestep = 1.0 / 150.0;
    //auto timestep = 1.0;

    computeMechanicalProblem( mechanical, std::move( history0 ), timestep );
}

} // namespace mlhp
