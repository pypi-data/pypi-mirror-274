// This file is part of the mlhp project. License: See LICENSE

#ifndef MLHP_CORE_UTILITIES_HPP
#define MLHP_CORE_UTILITIES_HPP

#include "mlhp/core/compilermacros.hpp"
#include "mlhp/core/coreexport.hpp"

#include <vector>
#include <array>
#include <string>
#include <iostream>
#include <stdexcept>
#include <any>
#include <functional>
#include <span>

namespace mlhp::utilities
{

// ================== Concepts ===================
    
template<typename T> 
concept DoubleCastable = ( static_cast<double>( T { } ), true );

// Following https://stackoverflow.com/a/51032862
template<typename, template<typename...> typename>
inline constexpr bool is_specialization = false;

template<template<typename...> typename T, typename... Args>
inline constexpr bool is_specialization<T<Args...>, T> = true;

template<typename T> 
inline constexpr bool is_stdarray_specialization = false;

template<typename T, size_t N> 
inline constexpr bool is_stdarray_specialization<std::array<T, N>> = true;

template<typename T> 
inline constexpr bool is_stdpair_specialization = false;

template<typename T1, typename T2> 
inline constexpr bool is_stdpair_specialization<std::pair<T1, T2>> = true;

template<typename T> 
concept StdVector = is_specialization<T, std::vector>;

template<typename T> 
concept StdArray = is_stdarray_specialization<T>;

template<typename T, typename V> 
concept StdVectorOf = StdVector<T> && std::is_same_v<V, typename T::value_type>;

template<typename T, typename V> 
concept StdArrayOf = StdArray<T> && std::is_same_v<V, typename T::value_type>;

// ================ Simple math ==================

template<typename T>
constexpr T integerPow( T base, size_t exponent );

template<typename T>
constexpr T binaryPow( size_t exponent );

// interpolate at given x between (x0, y0) and (x1, y1)
double interpolate( double x0, double y0, double x1, double y1, double x );

// maps to [0, 1]
double mapToLocal0( double begin, double end, double x );

// maps to [-1, 1]
double mapToLocal1( double begin, double end, double x );

// =============== Vector function ===============

template<typename T>
void scaleVector( std::vector<T>& vec, const T& value );

template<typename Target, typename SourceVector>
auto convertVector( SourceVector&& source );

template<typename T>
void addVectorsInplace( std::vector<T>& v1, const std::vector<T>& v2 );

// E.g. parameters (0.5, 1.5, 3) return [0.5, 1.0, 1.5]
std::vector<double> linspace( double min, double max, size_t n );

// Find internal interval in increasing sequence of coordinates.
// For example:
//     positions = [1.0, 2.0, 3.0], x = 0.5 --> returns 0
//     positions = [1.0, 2.0, 3.0], x = 1.5 --> returns 0
//     positions = [1.0, 2.0, 3.0], x = 2.5 --> returns 1
//     positions = [1.0, 2.0, 3.0], x = 3.5 --> returns 1
MLHP_PURE size_t findInterval( const std::vector<double>& positions, double x );

template<typename T>
std::vector<T> linearizeVectors( const std::vector<std::vector<T>>& vectors );

template<typename T, std::integral Index1, std::integral Index2>
auto linearizedSpan( const std::pair<std::vector<Index1>, std::vector<T>>& linearized, 
                     Index2 index );

template<typename IndexType>
auto allocateLinearizationIndices( size_t size );

template<typename IndexType>
auto sumLinearizationIndices( std::vector<IndexType>& indices );

template<typename DataType, typename IndexType>
auto sumAndAllocateData( std::vector<IndexType>& indices, DataType value = 0 );

template<typename T> inline
auto& resize0( std::vector<T>& vector );

template<typename T, size_t N> inline
auto& resize0( std::array<std::vector<T>, N>& vectors );

template<typename... T>
void resize0( T&&... vectors );

template<typename T>
void clearMemory( std::vector<T>& vector );

template<typename... Args>
size_t vectorInternalMemory( const std::vector<Args>&... vec );

// ==================== Other ====================

// Divides [0, size) into chunks. The index range from each chunk 
// can be computed using chunkRange below.
// * Returns [actual nchunks, actual minimum chunk size, first index of small block]
// * If size < approximateNChunks, then the number of chunks is set to size.
// * If size < minimumChunkSize, then one chunk with size is created.
template<std::integral Int>
auto divideIntoChunks( Int size, Int approximateNChunks, Int minimumChunkSize = 1 );

// Returns [begin, end) of given chunk according to the result of divideIntoChunks
template<std::integral Int>
auto chunkRange( Int iChunk, std::array<Int, 3> data );

template<typename Container, std::integral IndexType>
auto begin( Container& container, IndexType index = 0 );

template<std::integral IndexType>
std::ptrdiff_t ptrdiff( IndexType index );

template<typename Iterator1, typename Iterator2> MLHP_PURE
auto floatingPointEqual( Iterator1 begin1, Iterator1 end1, Iterator2 begin2, double tolerance );

class DefaultVirtualDestructor
{
protected:
    virtual ~DefaultVirtualDestructor( ) = default;
   
    explicit DefaultVirtualDestructor( ) = default;
    explicit DefaultVirtualDestructor( const DefaultVirtualDestructor& ) = default;
    explicit DefaultVirtualDestructor( DefaultVirtualDestructor&& ) = default;

    DefaultVirtualDestructor& operator=( const DefaultVirtualDestructor& ) = default;
    DefaultVirtualDestructor& operator=( DefaultVirtualDestructor&& ) = default;
};

// Tag template parameter to make unique type
struct TypeErasedCache : public DefaultVirtualDestructor
{
    explicit TypeErasedCache( ) = default;

    template<typename T>
    TypeErasedCache( T&& obj ) : cache( std::forward<T>( obj ) ) { }

    template<typename T>
    auto& cast( ) { return std::any_cast<T&>( cache ); }

    template<typename T>
    const auto& cast( ) const { return std::any_cast<const T&>( cache ); }

    std::any cache;
};

template<typename>
class UniqueTypeErasedCache final : public TypeErasedCache
{
    using TypeErasedCache::TypeErasedCache;
};

template<typename IndexType, typename ReturnType, typename... Args>
auto makeIndexRangeFunction( IndexType size,
                             const std::function<ReturnType( IndexType, Args... )>& evaluate );

template<typename IndexType, typename ObjectType, typename Return, typename... Args>
auto makeIndexRangeFunction( IndexType size, 
                             const ObjectType& object, 
                             Return( ObjectType::* function )( IndexType, Args... ) const );

constexpr auto doNothing( ) { return []( auto&&... ) noexcept { }; }

template<typename T>
constexpr auto returnEmpty( ) { return []( auto&&... ) noexcept { return T { }; }; }

template<typename T>
constexpr auto returnValue( T&& obj ) 
{ 
    return [obj = std::forward<T>( obj )]( auto&&... ) noexcept { return obj; }; 
}


} // namespace mlhp::utilities

// ================ Macro checks =================

// Defined and initialized in logging.cpp
MLHP_EXPORT extern bool MLHP_DISABLE_EXCEPTION_LOGS;

#ifdef _MSC_VER 
    #define MLHP_LOG_EXCEPTION( message ) if( !MLHP_DISABLE_EXCEPTION_LOGS ) std::cout << "MLHP check failed in " << __FUNCTION__ << ".\nMessage: " << ( message ) << std::endl
#endif

#ifndef MLHP_LOG_EXCEPTION
    #define MLHP_LOG_EXCEPTION( message )
#endif

#define MLHP_CHECK( expression, message ) if( !( expression ) ) \
{                                                               \
    MLHP_LOG_EXCEPTION( message );                              \
    throw std::runtime_error( message );                        \
}

#ifndef MLHP_DEBUG_CHECKS
#define MLHP_CHECK_DBG( expression, message )
#else
#define MLHP_CHECK_DBG( expression, message ) MLHP_CHECK( expression, message )
#endif

#define MLHP_EXPECTS( expression ) MLHP_CHECK( expression, "Violated precondition." )
#define MLHP_EXPECTS_DBG( expression ) MLHP_CHECK_DBG( expression, "Violated precondition." )

#define MLHP_THROW( message ) throw std::runtime_error( message )
#define MLHP_NOT_IMPLEMENTED MLHP_THROW( "Function \"" + std::string { __FUNCTION__ } + "\" is not implemented." )

#include "mlhp/core/utilities_impl.hpp"

#endif // MLHP_CORE_UTILITIES_HPP
