// This file is part of the mlhp project. License: See LICENSE

#include "tests/core/core_test.hpp"

#include "mlhp/core/sparse.hpp"
#include "mlhp/core/alias.hpp"
#include "mlhp/core/assembly.hpp"
#include "mlhp/core/memory.hpp"

namespace mlhp
{
namespace linalg
{

TEST_CASE( "test_gmres" )
{
    std::array<double, 16> data
    {
        1.0,  0.0,  3.0,  2.0,
        5.0,  3.0,  0.0,  3.0,
        0.0, -1.0,  2.0, -4.0,
       -2.0,  3.0,  0.0,  1.0
    };

    std::array<double, 4> rhs = { 1.0, 2.0, -3.0, 4.0 };

    std::array<std::array<double, 4>, 5> solutions
    {
        std::array<double, 4>{  0.169867690994452, -0.494238156209987, 1.000000000000000, 1.332052923602219 },
        std::array<double, 4>{ -0.201903700542658, -0.435649481089105, 0.983534452943718, 1.734330904883811 },
        std::array<double, 4>{ -0.307090130586031, -0.231010163115204, 1.236038540690432, 1.628899042266033 },
        std::array<double, 4>{ -0.453608247422680,  0.835051546391753, 0.092783505154639, 0.587628865979381 },
        std::array<double, 4>{ -0.453608247422680,  0.835051546391753, 0.092783505154639, 0.587628865979381 } // same
    };

//    std::array<double, 5> errors { 1.914854215512676, 1.230388913573920, 1.160505055753951, 1.141898479325880, 0.000000000000000 };

    auto multiplyA = [&]( const double* vector, double* target ) noexcept -> void
    {
        for( size_t i = 0; i < 4; ++i )
        {
            target[i] = 0.0;

            for( size_t j = 0; j < 4; ++j )
            {
                target[i] += data[i * 4 + j] * vector[j];
            }
        }
    };

    std::vector<double> computedErrors;

    for( size_t i = 4; i < 5; ++i )
    {
        size_t numberOfIterations = i + 1;

        std::array<double, 4> u = { 1.0, 1.0, 1.0, 1.0 }; // initial and target

        REQUIRE_NOTHROW( computedErrors = gmres( multiplyA, &rhs[0], &u[0], 4, numberOfIterations, 1e-10 ) );

        REQUIRE( computedErrors.size( ) == i + 1 );

        for( size_t j = 0; j < 4; ++j )
        {
            CHECK( u[j] == Approx( solutions[i][j] ).epsilon( 1e-10 ) );
        }
    }
}

TEST_CASE( "test_cg" )
{
    std::array<double, 16> data
    {
       1.0,  25.0,   0.0,   4.0,
      25.0,   9.0,   1.0,   9.0,
       0.0,   1.0,   4.0, -12.0,
       4.0,   9.0, -12.0,   1.0
    };

    std::vector<double> rhs = { 1.0, 2.0, -3.0, 4.0 };
    std::vector<double> solution { 0.03221482177350403, 0.014471337041767379, -0.2991165201237083,  0.1515004380455779 };

    auto multiplyA = [&]( const double* vector, double* target ) noexcept -> void
    {
        for( size_t i = 0; i < 4; ++i )
        {
            target[i] = 0.0;

            for( size_t j = 0; j < 4; ++j )
            {
                target[i] += data[i * 4 + j] * vector[j];
            }
        }
    };

    auto preconditioner = [&]( const double* vector, double* target ) -> void
    {
        std::copy( vector, vector + 4, target );
    };

    std::vector<double> target;

    auto errors = cg( multiplyA, rhs, target, preconditioner, 10, 1e-12 );

    double tolerance = 1e-10;

    REQUIRE( errors.size( ) == 5 );

    CHECK( errors[0] == Approx( 30.0 ).epsilon( tolerance ) );
    CHECK( errors[1] == Approx( 8.2731253087877 ).epsilon( tolerance ) );
    CHECK( errors[2] == Approx( 8.7510133208575 ).epsilon( tolerance ) );
    CHECK( errors[3] == Approx( 0.3245973156860 ).epsilon( tolerance ) );
    CHECK( errors[4] == Approx( 0.0 ).margin( tolerance ) );

    for( size_t i = 0; i < 4; ++i )
    {
        CHECK( target[i] == Approx( solution[i] ).epsilon( tolerance ) );
    }
}

TEST_CASE( "SymmetricSparseMatrix_test" )
{
    //  2.0 -0.5  0.0  0.0  0.8
    // -0.5  1.0  0.0  1.4  6.1
    //  0.0  0.0 -0.2  0.0 -4.9
    //  0.0  1.4  0.0  3.2  0.0
    //  0.8  6.1 -4.9  0.0  2.7

    linalg::SparseIndex indices[] { 0, 1, 4, 1, 3, 4, 2, 4, 3, 4 };
    linalg::SparsePtr indptr []   { 0,       3,       6,    8, 9, 10 };

    double data[] = { 2.0, -0.5, 0.8, 1.0, 1.4, 6.1, -0.2, -4.9, 3.2, 2.7 };

    SymmetricSparseMatrix matrix;

    matrix.claim( { indices, indptr, data }, 5, 5 );

    // Find
    CHECK( matrix.find( 2, 1 ) == nullptr );
    CHECK( matrix.find( 1, 2 ) == nullptr );

    REQUIRE( matrix.find( 1, 4 ) != nullptr );
    REQUIRE( matrix.find( 4, 1 ) != nullptr );

    CHECK( *matrix.find( 1, 4 ) == Approx( 6.1 ).epsilon( 1e-12 ) );
    CHECK( *matrix.find( 4, 1 ) == Approx( 6.1 ).epsilon( 1e-12 ) );

    // operator()
    CHECK( matrix( 3, 4 ) == 0.0 );
    CHECK( matrix( 4, 3 ) == 0.0 );

    CHECK( matrix( 2, 2 ) == Approx( -0.2 ).epsilon( 1e-12 ) );
    CHECK( matrix( 0, 4 ) == Approx(  0.8 ).epsilon( 1e-12 ) );
    CHECK( matrix( 4, 0 ) == Approx(  0.8 ).epsilon( 1e-12 ) );

    // Convert matrix
    auto converted1 = convertToUnsymmetric( matrix );
    auto converted2 = convertToSymmetric( converted1 );

    CHECK( converted1.size1( ) == 5 );
    CHECK( converted1.size2( ) == 5 );
    CHECK( converted2.size1( ) == 5 );
    CHECK( converted2.size2( ) == 5 );

    CHECK( converted1.nnz( ) == 15 );
    CHECK( converted2.nnz( ) == 10 );

    CHECK( std::equal( matrix.indices( ), matrix.indices( ) + 10, converted2.indices( ) ) );
    CHECK( std::equal( matrix.indptr( ), matrix.indptr( ) + 6, converted2.indptr( ) ) );
    CHECK( utilities::floatingPointEqual( matrix.data( ), matrix.data( ) + 10, converted2.data( ), 1e-12 ) );

    // Matrix vector multiplication
    std::vector<double> rhs { 4.3, 0.9, -3.8, 2.7, -5.1 };
    std::vector<double> result;

    REQUIRE_NOTHROW( result = matrix * rhs );

    std::vector<double> expectedResult = { 4.07, -28.58, 25.75, 9.9, 13.78 };

    REQUIRE( result.size( ) == 5 );

    CHECK( utilities::floatingPointEqual( result.begin( ), result.end( ), expectedResult.data( ), 1e-12 ) );

    matrix.release( );
}

TEST_CASE( "additiveSchwarzPreconditiner_test" )
{

    LocationMapVector locationMaps
    {
        { 3, 5, 2, 9 },
        { 2, 5, 1 },
        { 4, 7, 6, 8 },
        { 6, 3, 0, 2 },
        { 0, 7, 4, 9 }
    };

    std::vector<DofIndex> boundaryDofs = { 0, 4, 5 };

    auto matrix = allocateMatrix<UnsymmetricSparseMatrix>( locationMaps, boundaryDofs );

    CHECK( matrix.size1( ) == 7 );
    CHECK( matrix.size2( ) == 7 );
    CHECK( matrix.nnz( ) == 27 );

    double data[] =
    {
         0.64202513, -0.71780219,  0.73520574,  0.09422523,  0.64773527,  0.27863069,  
         0.09926103,  0.83820316, -0.15063977, -0.22692626, -0.25393631,  0.41522684, 
        -0.69547944,  0.6159814 ,  0.02996156, -0.99045522, -0.22174527,  0.02455323, 
        -0.13893814,  0.43454513, -0.10693943,  0.3213493 ,  0.00797774, -0.40185595,  
         0.10185092, -0.96199103,  0.4709358
    };

    std::copy( std::begin( data ), std::end( data ), matrix.data( ) );

    double expectedData[] =
    {
         0.16018508,  1.2202804,  -1.24986683,  1.7712951,   2.59201746,  0.18616924,
         0.7813684,   2.61182362, -0.33810382, -0.45193774, -0.55979437,  0.92256199,
        -0.59297582,  1.45431102, -3.3145493,   0.20974528,  0.17302143,  0.04518146,
         3.17605458, -1.01153099, -0.71418838, -2.09317093,  0.22652082, -0.12978111,
         1.41031782,  2.23931574,  2.96840753
    };

    auto generator = utilities::makeIndexRangeFunction( size_t { 5 }, std::function { 
        [&]( size_t index, std::vector<SparseIndex>& map )
    {
        map.resize( locationMaps[index].size( ) );

        std::copy( locationMaps[index].begin( ), 
                   locationMaps[index].end( ), map.begin( ) );
    } } );

    auto P = makeAdditiveSchwarzPreconditioner( matrix, generator, boundaryDofs, 10 );

    CHECK( P.size1( ) == 7 );
    CHECK( P.size2( ) == 7 );
    CHECK( P.nnz( ) == 27 );

    CHECK( std::equal( P.indices( ), P.indices( ) + P.nnz( ), matrix.indices( ) ) );
    CHECK( std::equal( P.indptr( ), P.indptr( ) + P.size1( ), matrix.indptr( ) ) );

    for( size_t i = 0; i < P.nnz( ); ++i )
    {
        CHECK( P.data( )[i] == Approx( expectedData[i] ).epsilon( 1e-7 ).margin( 1e-7 ) );
    }
}

} // namespace linalg
} // namespace mlhp
