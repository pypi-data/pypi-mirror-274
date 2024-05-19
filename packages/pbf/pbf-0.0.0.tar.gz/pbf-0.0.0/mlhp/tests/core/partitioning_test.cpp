// This file is part of the mlhp project. License: See LICENSE

#include "tests/core/core_test.hpp"

#include "mlhp/core/partitioning.hpp"
#include "mlhp/core/implicit.hpp"
#include "mlhp/core/quadrature.hpp"
#include "mlhp/core/arrayfunctions.hpp"
#include "mlhp/core/mesh.hpp"

#include <numbers>

namespace mlhp
{
namespace
{

template<size_t D>
auto createTestMesh( std::array<double, D> corner1, 
                     std::array<double, D> corner2 )
{
    auto mesh = makeCartesianGrid<D>( array::makeSizes<D>( 1 ), array::subtract( corner2, corner1 ), corner1 );

    auto mapping = mesh->createMapping( );
    
    mesh->prepareMapping( 0, mapping );

    return std::pair { mesh, std::move( mapping ) };
}

} // namespace

TEST_CASE( "makeCartesianMappingSplitter_test" )
{
    auto mapping = CartesianMapping<3> { {{ { 5.0, -2.0, 4.0 }, { 7.0, 1.0, 5.0 } }} };
    auto generator = makeCartesianMappingSplitter<3>( mapping, { 3, 2, 4 } );

    auto J0 = std::array { 1.0, 0.0, 0.0, 
                           0.0, 1.5, 0.0,
                           0.0, 0.0, 0.5 };

    CHECK( spatial::distance<3>( mapping( { } ), { 6.0, -0.5, 4.5 } ) < 1e-8 ); 
    CHECK( spatial::distance( mapping.J( { } ), J0 ) < 1e-8 );
    CHECK( mapping.detJ( { } ) == Approx( 2.0 * 3.0 * 1.0 / 8.0 ).epsilon( 1e-8 ) );

    using IjkRstXyz = std::tuple<std::array<size_t, 3>, std::array<double, 3>, std::array<double, 3>>;

    auto tests = std::vector<IjkRstXyz>
    {
        { { 0, 0, 0 }, { -1.0, -1.0, -1.0 }, { 5.0, -2.0, 4.0 } },
        { { 0, 0, 0 }, { 1.0, 0.5, -0.5 }, { 5.0 + 2.0 / 3.0, -0.875, 4.0625 } },
        { { 1, 0, 1 }, { -0.5, -0.5, 0.5 }, { 5.0 + 2.0 / 3.0 + 1.0 / 6.0, -1.625, 4.4375 } },
        { { 1, 1, 2 }, { 0.0, 1.0, -1.0 }, { 6.0, 1.0, 4.5 } },
        { { 2, 1, 3 }, { 1.0, 1.0, 1.0 }, { 7.0, 1.0, 5.0 } }
    };

    for( auto [ijk, rst, xyz] : tests )
    {
        CHECK( spatial::distance<3>( generator( ijk ).map( rst ), xyz ) < 1e-8 ); 
    }

    auto computedDetJ = generator( { 1, 1, 2 } ).detJ( { 0.5, -0.3, 1.0 } );
    auto expectedDetJ = 2.0 / 3.0 * 3.0 / 2.0 * 1.0 / 4.0 / 8.0;

    CHECK( computedDetJ == Approx( expectedDetJ ).epsilon( 1e-8 ) );
}

TEST_CASE( "SpaceTreeQuadrature_test" )
{
    auto circle = implicit::sphere<2>( { 1.2, 0.6 }, 0.16 );

    double epsilonFCM = 1.27e-4;

    SpaceTreeQuadrature<2> quadrature( circle, epsilonFCM, 3 );

    auto cache = quadrature.initialize( );

    CoordinateGrid<2> rstTarget;
    CoordinateList<2> xyzTarget;
    std::vector<double> weightsTarget;
    
    std::vector<std::array<double, 2>> expectedRst
    {
        { -0.5,   -0.5   }, { -0.75,   0.25  },  
        { -0.875,  0.625 }, { -0.875,  0.875 }, { -0.625,  0.625 }, { -0.625,  0.875 }, 
        { -0.375,  0.125 }, { -0.375,  0.375 }, { -0.125,  0.125 }, { -0.125,  0.375 }, 
        { -0.375,  0.625 }, { -0.375,  0.875 }, { -0.125,  0.625 }, { -0.125,  0.875 }, 
        {  0.25,  -0.75  },
        {  0.125, -0.375 }, {  0.125, -0.125 }, {  0.375, -0.375 }, {  0.375, -0.125 },
        {  0.625, -0.875 }, {  0.625, -0.625 }, {  0.875, -0.875 }, {  0.875, -0.625 },
        {  0.625, -0.375 }, {  0.625, -0.125 }, {  0.875, -0.375 }, {  0.875, -0.125 },
        {  0.125,  0.125 }, {  0.125,  0.375 }, {  0.375,  0.125 }, {  0.375,  0.375 },
        {  0.25,   0.75  }, {  0.75,   0.25  }, {  0.75,   0.75  },
    };

    auto expectedLocalDeterminants = std::vector<double> ( 34, 0.015625 );

    expectedLocalDeterminants[0] *= 16.0;
    expectedLocalDeterminants[1] *= 4.0;
    expectedLocalDeterminants[14] *= 4.0;
    expectedLocalDeterminants[31] *= 4.0;
    expectedLocalDeterminants[32] *= 4.0;
    expectedLocalDeterminants[33] *= 4.0;

    double tolerance = 1e-12;

    {
        auto [mesh, mapping] = createTestMesh<2>( { 1.2, 0.6 }, { 1.4, 0.8 } );

        size_t numberOfPartitions;

        REQUIRE_NOTHROW( numberOfPartitions = quadrature.partition( mapping, cache ) );

        REQUIRE( numberOfPartitions == 34 );

        double rootDetJAndWeight = 0.01 * ( 8.0 / 9.0 ) * ( 8.0 / 9.0 );

        for( size_t i = 0; i < 34; ++i )
        {
            REQUIRE_NOTHROW( quadrature.distribute( i, { 3, 3 }, rstTarget, xyzTarget, weightsTarget, cache ) );

            REQUIRE( rstTarget[0].size( ) == 3 );
            REQUIRE( rstTarget[1].size( ) == 3 );
            REQUIRE( xyzTarget.size( ) == 3 * 3 );

            auto expectedXyz = mapping( expectedRst[i] );
            double alphaFCM = circle( expectedXyz ) ? 1.0 : epsilonFCM;

            // check mid point of 3x3 gauss rule which is at (0, 0)
            CHECK( rstTarget[0][1] == Approx( expectedRst[i][0] ).epsilon( tolerance ) );
            CHECK( rstTarget[1][1] == Approx( expectedRst[i][1] ).epsilon( tolerance ) );
            CHECK( xyzTarget[4][0] == Approx( expectedXyz[0] ).epsilon( tolerance ) );
            CHECK( xyzTarget[4][1] == Approx( expectedXyz[1] ).epsilon( tolerance ) );
            CHECK( weightsTarget[4] == Approx( rootDetJAndWeight * expectedLocalDeterminants[i] * alphaFCM ).epsilon( tolerance ) );
        }
    }
        
} // SpaceTreeQuadrature_test

namespace partitionertest
{

template<size_t D>
double volumeUsingSpaceTree( const ImplicitFunction<D>& function, 
                             const MeshMapping<D>& mapping, 
                             std::array<size_t, D> orders,
                             size_t depth, double alphaFCM )
{

    SpaceTreeQuadrature<D> quadrature( function, alphaFCM, depth );

    auto cache = quadrature.initialize( );

    CoordinateGrid<D> rstTarget;
    CoordinateList<D> xyzTarget;
    std::vector<double> weightsTarget;

    size_t numberOfPartitions = 0;
    
    REQUIRE_NOTHROW( numberOfPartitions = quadrature.partition( mapping, cache ) );

    REQUIRE( numberOfPartitions > 0 );
     
    double integral = 0.0;

    for( size_t iPartition = 0; iPartition < numberOfPartitions; ++iPartition )
    {
        REQUIRE_NOTHROW( quadrature.distribute( iPartition, orders, rstTarget, xyzTarget, weightsTarget, cache ) );

        for( size_t i = 0; i < array::product( orders ); ++i )
        {
            integral += weightsTarget[i];
        }
    }

    return integral;
}

} // namespace partitionertest

TEST_CASE( "MomentFittingQuadrature_test" )
{
    double tolerance = 1e-12;

    std::array<double, 3> corner1 = { 2.0, 1.0, 3.0 };
    std::array<double, 3> corner2 = { 3.0, 2.0, 4.0 };

    auto sphere1 = implicit::sphere<3>( { 2.8, 1.8, 3.0 }, 0.2 );
    auto sphere2 = implicit::sphere<3>( { 2.0, 1.0, 3.0 }, 0.5 );

    auto spheres = implicit::add( sphere1, sphere2 );

    size_t depth = 3;
    double alphaFCM = 1e-3;//3.2e-5;

    MomentFittingQuadrature<3> quadrature( spheres, alphaFCM, depth, false );

    CoordinateGrid<3> rstTarget;
    CoordinateList<3> xyzTarget;
    std::vector<double> weightsTarget;

    std::array<size_t, 3> orders { 4, 2, 3 };

    auto cache = quadrature.initialize( );
    
    auto [mesh, mapping] = createTestMesh<3>( corner1, corner2 );
    
    for( size_t i = 0; i < 3; ++i )
    {
        size_t numberOfCells;
                
        REQUIRE_NOTHROW( numberOfCells = quadrature.partition( mapping, cache ) );

        REQUIRE( numberOfCells == 1 );

        REQUIRE_NOTHROW( quadrature.distribute( 0, orders, rstTarget, xyzTarget, weightsTarget, cache ) );

        auto strides = nd::stridesFor( orders );

        for( size_t axis = 0; axis < 3; ++axis )
        {
            auto gaussPoints = gaussLegendrePoints( orders[axis] )[0];

            REQUIRE( rstTarget[axis].size( ) == orders[axis] );
            CHECK( std::equal( rstTarget[axis].begin( ), rstTarget[axis].end( ), gaussPoints.begin( ) ) );

            auto map = [&]( double r ) { return ( r + 1.0 ) / 2.0 * ( corner2[axis] - corner1[axis] ) + corner1[axis]; };

            // Test map to global for a few points
            CHECK( xyzTarget[0][axis] == Approx( map( gaussPoints[0] ) ).epsilon( tolerance ) );
             
            for( size_t axis2 = 0; axis2 < 3; ++axis2 )
            {
                CHECK( xyzTarget[strides[axis2]][axis] == Approx( map( gaussPoints[axis == axis2] ) ).epsilon( tolerance ) );
            }

            CHECK( xyzTarget.back( )[axis] == Approx( map( gaussPoints.back( ) ) ).epsilon( tolerance ) );
        }
    }

    double volume = 0.0;

    for( size_t i = 0; i < array::product( orders ); ++i )
    {
        volume += weightsTarget[i];

    } // for i

    double spaceTreeVolume = partitionertest::volumeUsingSpaceTree<3>( spheres, mapping, orders, depth, alphaFCM );
    double exactVolume = ( 1.0 - alphaFCM ) * 4.0 / 3.0 * std::numbers::pi * ( 0.2 * 0.2 * 0.2 / 2.0 + 0.5 * 0.5 * 0.5 / 8.0 ) + alphaFCM;
    
    CHECK( spaceTreeVolume == Approx( exactVolume ).epsilon( 5e-3 ) );
    CHECK( volume == Approx( spaceTreeVolume ).epsilon( tolerance ) );
}

TEST_CASE( "StandardQuadrature_test" )
{
    StandardQuadrature<2> quadrature;

    auto cache = quadrature.initialize( );

    CoordinateGrid<2> rstTarget;
    CoordinateList<2> xyzTarget;
    std::vector<double> weightsTarget;
    
    CoordinateGrid<2> expectedRst, expectedWeights;

    std::array<size_t, 2> orders { 4, 3 };

    auto quadratureCache = QuadraturePointCache { };

    tensorProductQuadrature( orders, expectedRst, expectedWeights, quadratureCache );

    double tolerance = 1e-12;

    // Try 3 times
    for( size_t dummy = 0; dummy < 3; ++dummy )
    {
        auto testmesh = createTestMesh<2>( { 1.2, 0.6 }, { 1.4, 0.8 } );
        auto mesh = std::get<0>( testmesh );
        auto mapping = std::move( std::get<1>( testmesh ) );

        size_t numberOfPartitions;

        REQUIRE_NOTHROW( numberOfPartitions = quadrature.partition( mapping, cache ) );

        REQUIRE( numberOfPartitions == 1 );

        REQUIRE_NOTHROW( quadrature.distribute( 0, orders, rstTarget, xyzTarget, weightsTarget, cache ) );

        for( size_t axis = 0; axis < 2; ++axis )
        {
            for( size_t i = 0; i < orders[axis]; ++i )
            {
                CHECK( rstTarget[axis][i] == Approx( expectedRst[axis][i] ).epsilon( tolerance ) );
            }
        }

        nd::executeWithIndex( orders, [&]( std::array<size_t, 2> ijk, size_t index )
        { 
            double expectedWeight = array::product( array::extract( expectedWeights, ijk ) ) * 0.01;
            auto expectedXyz = mapping( array::extract( expectedRst, ijk ) );

            CHECK( weightsTarget[index] == Approx( expectedWeight ).epsilon( tolerance ) );

            for( size_t axis = 0; axis < 2; ++axis )
            {
                CHECK( xyzTarget[index][axis] == Approx( expectedXyz[axis] ).epsilon( tolerance ) );
            }
        } );
    }
}

} // namespace mlhp
