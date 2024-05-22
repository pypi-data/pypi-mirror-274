// This file is part of the mlhp project. License: See LICENSE

#include "mlhp/core/quadrature.hpp"
#include "mlhp/core/compilermacros.hpp"
#include "mlhp/core/mapping.hpp"

#include <numeric>
#include <algorithm>
#include <memory>
#include <cmath>

namespace mlhp
{

MLHP_PURE std::array<double, 3> legendreRecursive( double x, size_t n, const std::vector<double>& c )
{
    double p1 = 1.0;
    double dp1 = 0.0;

    double p2 = x;
    double dp2 = 1.0;

    for( size_t i = 1; i < n; ++i )
    {
        double p0 = p1;
        double dp0 = dp1;

        p1 = p2;
        dp1 = dp2;

        p2 = x * p1 - c[i] * p0;
        dp2 = x * dp1 + p1 - c[i] * dp0;
    }

    return { p2, dp2, p1 };
}

std::array<double, 3> legendreRoot( double x, size_t n, const std::vector<double>& c )
{
    size_t maxstep = 10;
    double eps = 1e-15;

    double dp2 = 0.0;
    double p1 = 0.0;

    for( size_t i = 0; i < maxstep; ++i )
    {
        auto result = legendreRecursive( x, n, c );

        double p2 = result[0];

        dp2 = result[1];
        p1 = result[2];

        double d = p2 / dp2;

        x = x - d;

        if( std::abs( d ) <= eps * ( std::abs( x ) + 1.0 ) )
        {
            return { x, dp2, p1 };
        }
    }

    throw std::runtime_error( "Error in computation of Gauss-Legendre points." );
}

// Algorithm from:
// https://people.sc.fsu.edu/~jburkardt/m_src/quadrule/quadrule.html
// https://people.sc.fsu.edu/~jburkardt/m_src/quadrule/legendre_ss_compute.m
void gaussLegendrePoints( size_t order, QuadraturePoints1D& target )
{
    if( order != 0 )
    {
        auto& x = target[0];
        auto& w = target[1];

        x.resize( order, 0.0 );
        w.resize( order, 0.0 );

        std::vector<double> c( order, 0.0 );

        for( size_t j = 0; j < order; ++j )
        {
            double i = static_cast<double>( j ) + 1.0;

            c[j] = ( ( i - 1.0 ) * ( i - 1.0 ) ) / ( ( 2.0 * i - 1.0 ) * ( 2.0 * i - 3.0 ) );
        }

        double cc = 2.0 * std::accumulate( c.begin( ) + 1, c.end( ), 1.0, std::multiplies<double>{ } );

        double xtemp = 0.0;

        for( size_t i = 0; i < order; ++i )
        {
            if( i == 0 )
            {
                double r = 2.78 / ( 4.0 + order * order );

                xtemp = 1.0 - r;
            }
            else if( i == 1 )
            {
                double r = 1.0 + 0.06 * ( order - 8.0 ) / order;

                xtemp = xtemp - 4.1 * r * ( 1.0 - xtemp );
            }
            else if( i == 2 )
            {
                double r = 1.0 + 0.22 * ( order - 8.0 ) / order;

                xtemp = xtemp - 1.67 * r * ( x[0] - xtemp );
            }
            else if( i + 2 < order )
            {
                xtemp = 3.0 * x[i - 1] - 3.0 * x[i - 2] + x[i - 3];
            }
            else if( i + 2 == order )
            {
                double r = 1.0 / ( 1.0 + 0.639 * ( order - 4.0 ) / ( 1.0 + 0.71 * ( order - 4.0 ) ) );

                xtemp = xtemp + r * ( xtemp - x[i - 2] ) / 0.766;
            }
            else if( i + 1 == order )
            {
                double r = 1.0 / ( 1.0 + 0.22 * ( order - 8.0 ) / order );

                xtemp = xtemp + r * ( xtemp - x[i - 2] ) / 1.67;
            }

            auto result = legendreRoot( xtemp, order, c );

            xtemp = result[0];

            x[i] = xtemp;
            w[i] = cc / result[1] / result[2];
        }

        std::reverse( x.begin( ), x.end( ) );
        std::reverse( w.begin( ), w.end( ) );
    }
}

QuadraturePoints1D gaussLegendrePoints( size_t order )
{
    auto points = QuadraturePoints1D { };

    gaussLegendrePoints( order, points );

    return points;
}

QuadraturePointCache::QuadraturePointCache( const QuadratureRule1D& quadrature_ ) :
    quadrature { quadrature_ } 
{ }

QuadraturePointCache::QuadraturePointCache( ) :
    QuadraturePointCache ( static_cast<void (*)(size_t, QuadraturePoints1D&)>( &gaussLegendrePoints ) )
{ }

const QuadraturePoints1D& QuadraturePointCache::operator() ( size_t order )
{
    if( data.size( ) < order + 1 )
    {
        data.resize( order + 1 );
    }
    
    if( !data[order] )
    {
        data[order] = std::make_shared<QuadraturePoints1D>( );

        quadrature( order, *data[order] );
    }
    
    return *data[order];
}

template<size_t D>
void tensorProductQuadrature( std::array<size_t, D> orders,
                              CoordinateGrid<D>& rst,
                              QuadraturePointCache& cache )
{
    for( size_t axis = 0; axis < D; ++axis )
    {
        rst[axis] = cache( orders[axis] )[0];
    };
}

template<size_t D>
void tensorProductQuadrature( std::array<size_t, D> orders,
                              CoordinateGrid<D>& rst,
                              CoordinateGrid<D>& weights,
                              QuadraturePointCache& cache )
{
    for( size_t axis = 0; axis < D; ++axis )
    {
        auto& integrationPoints = cache( orders[axis] );
 
        rst[axis] = integrationPoints[0];
        weights[axis] = integrationPoints[1];
    };
}

template<size_t D> MLHP_EXPORT
void tensorProductQuadrature( std::array<size_t, D> orders,
                              CoordinateGrid<D>& rst,
                              std::vector<double>& weights,
                              QuadraturePointCache& cache )
{
    auto points = std::array<const QuadraturePoints1D*, D> { };

    for( size_t axis = 0; axis < D; ++axis )
    {
        points[axis] = &cache( orders[axis] );

        rst[axis] = points[axis]->at( 0 );
    }
        
    weights.resize( array::product( orders ) );

    nd::executeWithIndex( orders, [&]( std::array<size_t, D> ijk, size_t i )
    {
        weights[i] = 1.0;

        for( size_t axis = 0; axis < D; ++axis )
        {
            weights[i] *= points[axis]->at( 1 )[ijk[axis]];
        }
    } );
}

template<size_t D> MLHP_EXPORT
void tensorProductQuadrature( std::array<size_t, D> orders,
                              CoordinateList<D>& rst,
                              std::vector<double>& weights,
                              QuadraturePointCache& cache )
{
    auto npoints = array::product( orders );
    auto csize = rst.size( );
    auto wsize = weights.size( );
    auto points = std::array<const QuadraturePoints1D*, D> { };

    for( size_t axis = 0; axis < D; ++axis )
    {
        points[axis] = &cache( orders[axis] );
    }
        
    weights.resize( wsize + npoints );
    rst.resize( csize + npoints );

    nd::executeWithIndex( orders, [&]( auto ijk, auto i )
    {
        weights[wsize + i] = 1.0;

        for( size_t axis = 0; axis < D; ++axis )
        {
            rst[csize + i][axis] = points[axis]->at( 0 )[ijk[axis]];
            weights[wsize + i] *= points[axis]->at( 1 )[ijk[axis]];
        }
    } );
}

template<>// MLHP_EXPORT
void tensorProductQuadrature( std::array<size_t, 0>,
                              CoordinateList<0>& rst,
                              std::vector<double>& weights,
                              QuadraturePointCache& )
{
    rst.push_back( { } );
    weights.push_back( 1.0 );
}

namespace
{

template<size_t D>
void internalSimplexQuadrature( auto&& orders, auto&& cache, auto&& append )
{
    auto points = array::make<D>( &cache( orders[0] ) );
    auto transform = NCubeCollapsedToSimplex<D> { };

    for( size_t axis = 1; axis < D; ++axis )
    {
        points[axis] = &cache( orders[axis] );
    }

    nd::execute( orders, [&]( auto ijk )
    {
        auto rst = std::array<double, D> { };
        auto weight = 1.0;

        for( size_t axis = 0; axis < D; ++axis )
        {
            rst[axis] = points[axis]->at( 0 )[ijk[axis]];
            weight *= points[axis]->at( 1 )[ijk[axis]];
        }

        auto [xy, detJ] = map::withDetJ( transform, rst );

        append( xy, weight * detJ );
    } );
}

} // namespace simplex quadrature

template<size_t D>
void simplexQuadrature( std::array<size_t, D> orders,
                        CoordinateList<D>& rst,
                        std::vector<double>& weights,
                        QuadraturePointCache& cache )
{
    auto offset1 = rst.size( );
    auto offset2 = weights.size( );
    auto size = array::product( orders );

    rst.resize( offset1 + size );
    weights.resize( offset2 + size );

    auto index = size_t { 0 };    
    auto append = [&]( auto xyz, auto weight )
    {
        rst[offset1 + index] = xyz;
        weights[offset2 + index] = weight;

        index += 1;
    };

    internalSimplexQuadrature<D>( orders, cache, append );
}

template<>
void simplexQuadrature( std::array<size_t, 0>,
                        CoordinateList<0>& rst,
                        std::vector<double>& weights,
                        QuadraturePointCache& )
{
    rst.push_back( { } );
    weights.push_back( 1.0 );
}

template<size_t D> MLHP_EXPORT
void simplexQuadrature( std::array<size_t, D> orders,
                        CoordinateVectors<D>& rst,
                        std::vector<double>& weights,
                        QuadraturePointCache& cache )
{
    auto offset1 = rst[0].size( );
    auto offset2 = weights.size( );
    auto size = array::product( orders );

    for( size_t axis = 0; axis < D; ++axis )
    {
        MLHP_CHECK( rst[axis].size( ) == offset1, 
            "Inconsistent target vector sizes." );

        rst[axis].resize( offset1 + size );
    }

    weights.resize( offset2 + size );

    auto index = size_t { 0 };    
    auto append = [&]( auto xyz, auto weight )
    {
        for( size_t axis = 0; axis < D; ++axis )
        {
            rst[axis][offset1 + index] = xyz[axis];
        }

        weights[offset2 + index] = weight;

        index += 1;
    };

    internalSimplexQuadrature<D>( orders, cache, append );
}

void triangleTrapezoidalRule( CoordinateList<2>& coordinates,
                              std::vector<double>& weights )
{
    auto size1 = coordinates.size( );
    auto size2 = weights.size( );

    coordinates.resize( size1 + 3 );
    weights.resize( size2 + 3 );

    coordinates[size1 + 0] = { 0.0, 0.0 };
    coordinates[size1 + 1] = { 1.0, 0.0 };
    coordinates[size1 + 2] = { 0.0, 1.0 };

    weights[size2 + 0] = 1.0 / 6.0;
    weights[size2 + 1] = weights[size2];
    weights[size2 + 2] = weights[size2];
}

#define MLHP_INSTANTIATE_DIM( D )                                    \
                                                                     \
    template MLHP_EXPORT                                             \
    void tensorProductQuadrature( std::array<size_t, D> orders,      \
                                  CoordinateGrid<D>& rst,            \
                                  QuadraturePointCache& cache );     \
                                                                     \
    template MLHP_EXPORT                                             \
    void tensorProductQuadrature( std::array<size_t, D> orders,      \
                                  CoordinateGrid<D>& rst,            \
                                  CoordinateGrid<D>& weights,        \
                                  QuadraturePointCache& cache );     \
                                                                     \
    template MLHP_EXPORT                                             \
    void tensorProductQuadrature( std::array<size_t, D> orders,      \
                                  CoordinateGrid<D>& rst,            \
                                  std::vector<double>& weights,      \
                                  QuadraturePointCache& cache );     \
                                                                     \
    template MLHP_EXPORT                                             \
    void tensorProductQuadrature( std::array<size_t, D> orders,      \
                                  CoordinateList<D>& rst,            \
                                  std::vector<double>& weights,      \
                                  QuadraturePointCache& cache );     \
                                                                     \
    template MLHP_EXPORT                                             \
    void simplexQuadrature( std::array<size_t, D> orders,            \
                            CoordinateList<D>& rst,                  \
                            std::vector<double>& weights,            \
                            QuadraturePointCache& cache );           \
                                                                     \
    template MLHP_EXPORT                                             \
    void simplexQuadrature( std::array<size_t, D> orders,            \
                            CoordinateVectors<D>& rst,               \
                            std::vector<double>& weights,            \
                            QuadraturePointCache& cache );

    MLHP_DIMENSIONS_XMACRO_LIST
#undef MLHP_INSTANTIATE_DIM

} // mlhp
