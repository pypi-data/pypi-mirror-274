// This file is part of the mlhp project. License: See LICENSE

#ifndef MLHP_CORE_LOGGING_HPP
#define MLHP_CORE_LOGGING_HPP

#include "mlhp/core/coreexport.hpp"

#include <chrono>
#include <iostream>
#include <array>

namespace mlhp::utilities
{

inline auto tic( const std::string& msg = "" )
{
    std::cout << msg << std::flush;

    return std::chrono::high_resolution_clock::now( );
}

template<typename TimePoint>
inline double seconds( const TimePoint& t0,
                       const TimePoint& t1 )
{
    return std::chrono::duration_cast<std::chrono::duration<double>>( t1 - t0 ).count( );
}

template<typename TicType>
inline auto toc( TicType ticPoint,
                 const std::string& msg,
                 const std::string& postMsg = " s.\n" )
{
    auto now = std::chrono::high_resolution_clock::now( );

    std::cout << msg << seconds( ticPoint, now ) << postMsg << std::flush;

    return now;
}

template<typename TicType>
inline auto toc( TicType ticPoint )
{
    return seconds( ticPoint, std::chrono::high_resolution_clock::now( ) );
}

template<typename T, size_t D>
std::string toString( std::array<T, D> arr )
{
    if constexpr( D == 0 ) return "()";

    std::string result = "(" + std::to_string( arr[0] );

    for( size_t i = 1; i < D; ++i )
    {
        result += ", " + std::to_string( arr[i] );
    }

    return result + ")";
}

MLHP_EXPORT std::string thousandSeparator( std::uint64_t integer );

//! Converts result to fixed notation string with precision 1 or 2 if result < 10
MLHP_EXPORT std::string roundNumberString( double result );

//! Prints memory usage with suitable unit
MLHP_EXPORT std::string memoryUsageString( size_t bytes );

} // namespace mlhp::utilities

#endif // MLHP_CORE_LOGGING_HPP
