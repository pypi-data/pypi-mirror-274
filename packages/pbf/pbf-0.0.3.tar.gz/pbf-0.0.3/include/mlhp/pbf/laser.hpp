// This file is part of the mlhpbf project. License: See LICENSE

#ifndef MLHPBF_LASER_HPP
#define MLHPBF_LASER_HPP

#include "materials.hpp"
#include "history.hpp"
#include <iomanip>

namespace mlhp::laser
{

// Discrete point in laser path
template<size_t D>
struct Point
{
    std::array<double, D> xyz;
    double time;
    double power;
};

template<size_t D>
using LaserTrack = std::vector<Point<D>>;

// Discrete refinement point seen backwards from current time
struct Refinement
{
    double timeDelay;
    double sigma;
    double refinementLevel;
    double zfactor = 1.0;
};

template<size_t D> inline
auto makeTrack( const CoordinateList<D>& positions, double laserSpeed, double laserPower, double t0 = 0.0 )
{
    MLHP_CHECK( positions.size( ) >= 2, "At least two laser positions required." );

    LaserTrack<D> track { Point<D>{ positions.front( ), t0, laserPower } };

    for( size_t iposition = 0; iposition < positions.size( ); ++iposition )
    {
        double dx = spatial::distance( track.back( ).xyz, positions[iposition] );

        track.push_back( Point<D>{ positions[iposition], track.back( ).time + dx / laserSpeed, laserPower } );
    }

    return track;
}

template<size_t D> inline
auto interpolateTrack( const LaserTrack<D>& track, double time )
{
    if( time == track.back( ).time )
    {
        return std::make_tuple( track.back( ).xyz, track.back( ).power );
    }

    auto predicate = [&]( const auto& point )
    {
        return point.time > time;
    };

    auto point1 = std::find_if( track.begin( ), track.end( ), predicate );
    auto point0 = point1 - 1;

    MLHP_CHECK( point1 != track.begin( ) && point1 != track.end( ), "LaserPoint not found ??" );

    double tau = ( time - point0->time ) / ( point1->time - point0->time );

    auto power = point1->power; // tau * ( point1->power - point0->power ) + point0->power;

    auto xyz = tau * ( point1->xyz - point0->xyz ) + point0->xyz;

    return std::make_tuple( xyz, power );
}

template<size_t D> inline
auto gaussianBeamShape( double sigma, double absorptivity )
{
    return spatial::integralNormalizedGaussBell<D - 1>( { }, sigma, absorptivity );
}

template<size_t D> inline
auto volumeSource( const LaserTrack<D>& track, 
                   const spatial::ScalarFunction<D - 1>& beamShape, 
                   double depthSigma )
{
    std::function shapeZ = spatial::integralNormalizedGaussBell<1>( { }, depthSigma, 2.0 );

    std::function source = [=]( std::array<double, D + 1> xyzt )
    {
        auto [xyz, time] = array::peel( xyzt );

        if( time < track.front( ).time || time > track.back( ).time )
        {
            return 0.0;
        }

        auto [Pxyz, power] = interpolateTrack( track, time );
 
        auto [Pxy, Pz] = array::peel( Pxyz );
        auto [xy, z] = array::peel( xyz );
        auto depth = shapeZ( std::array { std::min( z - Pz, 0.0 ) } );

        return Pz >= z ? power * beamShape( xy - Pxy ) * depth : 0.0;
    };

    return source;
}

template<size_t D> inline
auto evaluateRefinements( const std::vector<Refinement>& refinements,
                          double delay, std::array<double, D> difference )
{
    double eps = 1e-8 * ( refinements.back( ).timeDelay - refinements.front( ).timeDelay );

    for( size_t irefinement = 0; irefinement + 1 < refinements.size( ); ++irefinement )
    {
        auto& refinement0 = refinements[irefinement];
        auto& refinement1 = refinements[irefinement + 1];

        if( delay < refinement1.timeDelay - eps )
        {
            // Map into current refinement segment
            auto tau = utilities::mapToLocal0( refinement0.timeDelay, refinement1.timeDelay, delay );

            // Interpolate sigma and level in current refinement segment
            auto sigma = ( 1.0 - tau ) * refinement0.sigma + tau * refinement1.sigma;
            auto zfactor = ( 1.0 - tau ) * refinement0.zfactor + tau * refinement1.zfactor;
            auto maxlevel = ( 1.0 - tau ) * refinement0.refinementLevel + tau * refinement1.refinementLevel;

            auto difference2 = difference;
   
            difference2.back( ) *= zfactor; 

            auto distanceSquared = spatial::normSquared( difference2 );

            // Evaluate exponential
            auto level = maxlevel * std::exp( -distanceSquared / ( 2.0 * sigma * sigma ) );

            return static_cast<RefinementLevel>( std::round( std::max( level, 0.0 ) ) );
        }
    }

    return RefinementLevel { 0 };
}

template<size_t D> inline
auto refinementLevelBasedOnLaserHistory( const LaserTrack<D>& track,
                                         const std::vector<Refinement>& refinements )
{
    auto delay0 = refinements.front( ).timeDelay;
    auto delay1 = refinements.back( ).timeDelay;

    return [=]( std::array<double, D + 1> xyzt )
    {
        auto [xyz, time] = array::peel( xyzt );

        RefinementLevel level = 0;

        // Loop over laser path segments
        for( size_t iSegment = 0; iSegment + 1 < track.size( ); ++iSegment )
        {
            auto& point0 = track[iSegment];
            auto& point1 = track[iSegment + 1];

            // Continue if segment is not yet active, or finished longer ago than delay
            if( point1.power > 0.0 && point0.time <= time + delay0 && point1.time >= time - delay1 )
            {
                // If second point of segment is in future, then interpolate with current time
                auto alpha = ( time + delay0 - point0.time ) / ( point1.time - point0.time );

                alpha = std::clamp( alpha, 0.0, 1.0 );

                auto xyz1 = ( 1.0 - alpha ) * point0.xyz + alpha * point1.xyz;

                auto [p, t] = spatial::closestPointOnSegment( point0.xyz, xyz1, xyz );

                t *= alpha;

                // Local coordinate of projection p along axis point0 - point1
                double tau = time - ( 1.0 - t ) * point0.time - t * point1.time;

                level = std::max( level, evaluateRefinements( refinements, tau, p - xyz ) );
            }
        }

        return level;
    };
}

// Refinement based on laser history sliced for given time (for time-stepping)
template<size_t D> inline
auto makeRefinement( const LaserTrack<D>& track,
                     const std::vector<Refinement>& refinements,
                     double time,
                     size_t nseedpoints = 7 )
{
    auto levelFunction = refinementLevelBasedOnLaserHistory( track, refinements );

    auto slicedLevelFunction = [=]( std::array<double, D> xyz )
    {
        return levelFunction( array::insert( xyz, D, time ) );
    };

    return refineWithLevelFunction<D>( slicedLevelFunction, nseedpoints );
}

// Refinement based on laser history as D + 1 dimensional function (for space-time)
template<size_t D> inline
auto makeRefinement( const LaserTrack<D>& track,
                     const std::vector<Refinement>& refinements,
                     size_t nseedpoints = 5 )
{
    auto levelFunction = refinementLevelBasedOnLaserHistory( track, refinements );

    return refineWithLevelFunction<D + 1>( levelFunction, nseedpoints );
}

// Postprocess for time slice (for time-stepping)
template<size_t D> inline
auto makeRefinementLevelFunctionPostprocessor( const LaserTrack<D>& track,
                                               const std::vector<Refinement>& refinements,
                                               double time )
{
    auto depthInt = refinementLevelBasedOnLaserHistory<D>( track, refinements );

    auto slicedDepth = [=]( std::array<double, D> xyz )
    {
        return static_cast<double>( depthInt( array::insert( xyz, D, time ) ) );
    };

    return makeFunctionProcessor<D>( std::function { slicedDepth }, "RefinementLevel" );
}

// Postprocess volumetrically (for space-time, will be sliced later)
template<size_t D> inline
auto makeRefinementLevelFunctionPostprocessor( const LaserTrack<D>& track,
                                               const std::vector<Refinement>& refinements )
{
    auto depthInt = refinementLevelBasedOnLaserHistory<D>( track, refinements );

    auto slicedDouble = [=]( std::array<double, D + 1> xyzt ) { return static_cast<double>( depthInt( xyzt ) ); };

    return makeFunctionPostprocessor<D + 1>( std::function { slicedDouble }, "RefinementLevel" );
}

inline auto hatchedRectanglePositions( std::array<double, 3> center, double width, double height, double trackDistance )
{
    static constexpr size_t D = 3;

    auto laserPositions = CoordinateList<D> { };

    auto append = [&]( double x, double y )
    {
        laserPositions.push_back( { x, y, center[2] } );
    };

    // Frame
    append( center[0] - width / 2.0, center[1] + height / 2.0 );
    append( center[0] - width / 2.0, center[1] - height / 2.0 ); 
    append( center[0] + width / 2.0, center[1] - height / 2.0 ); 
    append( center[0] + width / 2.0, center[1] + height / 2.0 ); 
    append( center[0] - width / 2.0, center[1] + height / 2.0 ); 

    // Interior
    double xmin = center[0] - width / 2.0;
    double ymin = center[1] - height / 2.0;
    double xmax = center[0] + width / 2.0;
    double ymax = center[1] + height / 2.0;

    auto ntracks = static_cast<size_t>( std::ceil( ( width + height ) / ( std::sqrt( 2.0 ) * trackDistance ) ) );
    auto increment = ( width + height ) / ntracks;

    MLHP_CHECK( ntracks > 2, "No inside tracks." );

    // Tracks
    for( size_t itrack = 1; itrack < ntracks; ++itrack )
    {
        auto t = itrack * increment;

        // Bottom left and top right points
        append( std::max( xmax - t, xmin ), std::max( ymin - width + t, ymin ) );
        append( std::min( xmax + height - t, xmax ), std::min( ymin + t, ymax ) );

        if( itrack % 2 != 0 )
        {
            std::iter_swap( laserPositions.end( ) - 1, laserPositions.end( ) - 2 );
        }
    }

    return laserPositions;
}

inline auto hatchedRectangleTrack( const CoordinateList<3>& positions, double power, double speed, double dwell0, double dwell1 )
{
    MLHP_CHECK( positions.size( ) > 6, "Invalid number of points.");

    auto track = laser::LaserTrack<3>{ laser::Point<3>{ positions.front( ), 0.0, power } };

    for( size_t iposition = 1; iposition < 5; ++iposition )
    {
        double dx = spatial::distance( track.back( ).xyz, positions[iposition] );

        track.push_back( laser::Point<3>{ positions[iposition], track.back( ).time + dx / speed, power } );
        track.push_back( laser::Point<3>{ positions[iposition], track.back( ).time + dwell0, 0.0 } );
    }

    track.pop_back( );

    for( size_t iposition = 6; iposition < positions.size( ); iposition += 2 )
    {
        double dx = spatial::distance( positions[iposition - 1], positions[iposition] );

        track.push_back( laser::Point<3>{ positions[iposition - 1], track.back( ).time + dwell1, 0.0 } );
        track.push_back( laser::Point<3>{ positions[iposition], track.back( ).time + dx / speed, power } );
    }

    return track;
}


} // namespace mlhp::laser

namespace mlhp
{

template<size_t D> inline
auto makeLaserBasedRefinement( const laser::LaserTrack<D>& track, 
                               double laserD4Sigma, 
                               size_t depth )
{
     auto refinement = std::vector
    {
        laser::Refinement { 0.00 * Units::ms, laserD4Sigma + 0.01 * Units::mm, depth + 0.4, 0.5 },
        laser::Refinement { 0.60 * Units::ms, laserD4Sigma + 0.07 * Units::mm, depth - 0.5, 0.5 },
        laser::Refinement { 6.00 * Units::ms, laserD4Sigma + 0.40 * Units::mm, depth - 1.5, 0.8 },
        laser::Refinement { 30.0 * Units::ms, laserD4Sigma + 0.90 * Units::mm, depth - 2.5, 1.0 },
        laser::Refinement { 0.10 * Units::s,  laserD4Sigma + 1.10 * Units::mm, depth - 3.0, 1.0 },
    };

    return [=]( auto& problem, auto&, auto& state1 )
    {
        return laser::makeRefinement<D>( track, refinement, state1.time, problem.degree + 1 );
    };
}

template<size_t D> inline
auto makeUniformRefinement( RefinementLevel level = 0 )
{
    return [=]( auto&&... )
    {
        return refineUniformly<D>( level );
    };
}

template<size_t D> inline
auto createBaseMeshTicks( spatial::BoundingBox<D> buildChamber,
                          double rootElementSize,
                          double layerHeight,
                          double zfactor = 0.7 )
{
    auto basePlate = 0.0;
    auto ticks = CoordinateGrid<3> { }; 
   
    for( size_t axis = 0; axis + 1 < D; ++axis )
    {
        auto nelements = static_cast<size_t>( std::max( ( buildChamber[1][axis] - buildChamber[0][axis] ) / rootElementSize, 1.0 ) );

        ticks[axis] = utilities::linspace( buildChamber[0][axis], buildChamber[1][axis], nelements + 1 );
    }

    rootElementSize *= zfactor;

    if( buildChamber[0].back( ) < basePlate )
    {
        auto nelements = static_cast<size_t>( std::max( ( basePlate - buildChamber[0].back( ) ) / rootElementSize, 1.0 ) );

        ticks.back( ) = utilities::linspace( buildChamber[0].back( ), basePlate, nelements + 1 );
    }
    
    auto dz = buildChamber[1].back( ) - buildChamber[0].back( );

    if( layerHeight < std::numeric_limits<double>::epsilon( ) * dz )
    {
        return ticks;
    }

    // Try to align or "snap" the mesh to the layer height as coarse as possible
    for( size_t power = 0; ; ++power )
    {
        auto testsize = rootElementSize / utilities::binaryPow<size_t>( power );
        auto ninlayer = std::llround( layerHeight / testsize );
        
        if( ninlayer && std::abs( testsize - layerHeight / ninlayer ) < 0.125 * testsize )
        {
            rootElementSize = layerHeight / ninlayer * utilities::binaryPow<size_t>( power );

            break;
        }
    }

    // Append base elements until above buildChamber
    for( auto z = basePlate; z < buildChamber[1].back( ) - 0.1 * Units::um; z += rootElementSize )
    {
        ticks.back( ).push_back( z + rootElementSize );
    }

    return ticks;
}

template<size_t D>
struct ProblemSetup
{
    using AnsatzSpace = TrunkSpace;

    spatial::BoundingBox<D> buildChamber;

    double duration;

    Material baseplate;
    Material structure;
    Material powder;
    Material air;

    CartesianGridSharedPtr<D> baseGrid;
};

auto& materialFor( auto& problem, MaterialType type )
{
    const Material* material = nullptr;

    if( type == MaterialType::Air       ) material = &problem.air;
    if( type == MaterialType::BasePlate ) material = &problem.baseplate;
    if( type == MaterialType::Powder    ) material = &problem.powder;
    if( type == MaterialType::Structure ) material = &problem.structure;

    MLHP_CHECK( material, "Unknown material type." );

    MLHP_CHECK( material->initialized, "Material with type index " +
        std::to_string( static_cast<int>( type ) ) + " is uninitialized." );

    return *material;
}

template<size_t D> inline
void printTrack( const laser::LaserTrack<D>& track )
{
    std::cout << "import numpy" << std::endl;
    std::cout << "import matplotlib.pyplot as plt" << std::endl;
    std::cout << "data = numpy.array([";

    for( auto [xyz, time, power] : track )
    {
        std::cout << "[";
        for( auto value : xyz )
        {
            std::cout << value << ", ";
        }

        std::cout << time << ", " << power << "]," << std::endl;
    }
    std::cout << "])" << std::endl;

    std::cout << "x, y = data[:, 0], data[:, 1]" << std::endl;
    std::cout << "time, power = data[:, " << D << "], data[:, " << D + 1 << "]" << std::endl;

    std::cout << "plt.plot(x, y)" << std::endl;
    //std::cout << "plt.plot([0.0, 2.4, 2.4, 0.0, 0.0], [0.0, 0.0, 2.4, 2.4, 0.0], 'black' )" << std::endl;
    std::cout << "plt.axis('equal')" << std::endl;
    std::cout << "plt.show()" << std::endl;
}

} // namespace mlhp

#endif // MLHPBF_LASER_HPP
