// This file is part of the mlhp project. License: See LICENSE

#ifndef MLHP_CORE_SPATIAL_HPP
#define MLHP_CORE_SPATIAL_HPP

#include "mlhp/core/alias.hpp"
#include "mlhp/core/coreexport.hpp"

namespace mlhp::spatial
{

// ========= General functions =========

template<size_t D> constexpr
auto dot( std::array<double, D> v1, 
          std::array<double, D> v2 );

template<size_t D1, size_t D2>
auto dot( std::span<double, D1> v1, 
          std::span<double, D2> v2 );

template<size_t N>
auto norm( const std::array<double, N>& arr );

template<size_t D>
auto normalize( std::array<double, D> v );

template<size_t N>
auto interpolate( std::array<double, N> v1,
                  std::array<double, N> v2,
                  double t );

template<size_t N>
auto distance( const std::array<double, N>& arr1,
               const std::array<double, N>& arr2 );

template<size_t N>
constexpr auto normSquared( const std::array<double, N>& arr );

template<size_t N>
constexpr auto distanceSquared( const std::array<double, N>& arr1,
                                const std::array<double, N>& arr2 );

//! Cross product
constexpr auto cross( std::array<double, 3> v1,
                      std::array<double, 3> v2 );

template<size_t N> 
constexpr auto standardBasisVector( size_t axis );

//! Returns { point, coordinate }
template<size_t D> 
constexpr auto projectOntoLine( std::array<double, D> line0,
                                std::array<double, D> line1,
                                std::array<double, D> point );

//! Returns { point, coordinate } with coordinate constrained to [0, 1]
template<size_t D>
constexpr auto closestPointOnSegment( std::array<double, D> line0,
                                      std::array<double, D> line1,
                                      std::array<double, D> point );

//! Target size must be two times polygon size. Returns span in target.
//! Side == false --> left side, Side == true --> right side
template<size_t D> MLHP_EXPORT
CoordinateSpan<D> clipPolygon( CoordinateConstSpan<D> polygon,
                               CoordinateSpan<D> target,
                               size_t axis, double position, bool side );

//! Target size must be three times polygon size. Returns span in target. 
template<size_t D> MLHP_EXPORT
CoordinateSpan<D> clipPolygon( CoordinateConstSpan<D> polygon, 
                               CoordinateSpan<D> target,
                               const BoundingBox<D>& bounds );

//auto clipLine( const std::array<double, D> rayOrigin,
//               const std::array<double, D> rayDirection,
//               const BoundingBox<D>& bounds );
//
//template<size_t D> 
//auto clipRay( const std::array<double, D> rayOrigin,
//              const std::array<double, D> rayDirection,
//              const BoundingBox<D>& bounds );

//! Finds some orthonormal vectors n1 and n2 that span the plane defined by normal
MLHP_EXPORT MLHP_PURE
std::array<std::array<double, 3>, 2> findPlaneVectors( std::array<double, 3> normal );

template<size_t D>
using MultilinearShapes = std::array<double, utilities::binaryPow<size_t>( D )>;

template<size_t L, size_t G>
using MultilinearCornersSpan = std::span<const std::array<double, G>, utilities::binaryPow<size_t>( L )>;

//! Evaluate linear/bilinear/trilinear/... interpolation on [-1, 1]^D
template<size_t D> MLHP_EXPORT MLHP_PURE
MultilinearShapes<D> multilinearShapeFunctions( std::array<double, D> rst, 
                                                std::array<size_t, D> diff = { } );


template<size_t L, size_t G> MLHP_EXPORT MLHP_PURE
JacobianMatrix<G, L> multilinearJacobian( MultilinearCornersSpan<L, G> corners, 
                                          std::array<double, L> rst );

template<size_t D> MLHP_EXPORT MLHP_PURE
std::array<double, D + 1> simplexShapeFunctions( std::array<double, D> rst, 
                                                 std::array<size_t, D> diff = { } );

//! Compute Jacobian matrix of composed mapping outer o inner as matrix product inner * outer
template<size_t G, size_t I, size_t L>
JacobianMatrix<G, L> concatenateJacobians( const JacobianMatrix<G, I>& outer,
                                           const JacobianMatrix<I, L>& inner );

template<size_t G, size_t L = G>
double computeDeterminant( const JacobianMatrix<G, L>& matrix );

template<size_t D>
bool isDiagonal( const JacobianMatrix<D, D>& matrix );

// ========= Triangles =========

template<size_t D>
constexpr auto triangleCentroid( std::array<double, D> vertex0,
                                 std::array<double, D> vertex1,
                                 std::array<double, D> vertex2 );

template<size_t D>
auto triangleNormal( std::array<double, D> vertex0,
                     std::array<double, D> vertex1,
                     std::array<double, D> vertex2 );

OptionalCoordinates<3> triangleRayIntersection( const std::array<double, 3>& vertex0,
                                                const std::array<double, 3>& vertex1,
                                                const std::array<double, 3>& vertex2,
                                                const std::array<double, 3>& rayOrigin,
                                                const std::array<double, 3>& rayAxis,
                                                double epsilon = 1e-12 );

//! Target size must be at least 3. Returns span in target.
//! Side == false --> left side, Side == true --> right side
template<size_t D>
CoordinateSpan<D> clipTriangle( const std::array<double, D>& vertex0,
                                const std::array<double, D>& vertex1,
                                const std::array<double, D>& vertex2,
                                size_t axis, double position, bool side,
                                CoordinateSpan<D> targetPolygon );

//! TargetPolygon size must be at least 9. Returns subspan in targetPolygon.
template<size_t D>
CoordinateSpan<D> clipTriangle( const std::array<double, D>& vertex0,
                                const std::array<double, D>& vertex1,
                                const std::array<double, D>& vertex2,
                                const BoundingBox<D>& bounds,
                                CoordinateSpan<D> targetPolygon );

template<size_t D>
BoundingBox<D> triangleClippedBoundingBox( const std::array<double, D>& vertex0,
                                           const std::array<double, D>& vertex1,
                                           const std::array<double, D>& vertex2,
                                           size_t axis, double position, bool side );

template<size_t D>
BoundingBox<D> triangleClippedBoundingBox( const std::array<double, D>& vertex0,
                                           const std::array<double, D>& vertex1,
                                           const std::array<double, D>& vertex2,
                                           const spatial::BoundingBox<D>& bounds );

//! Array of simplices that subdivide an n cube (like 6 tetrahedra subdivide a cube)
template<size_t D> 
constexpr auto simplexSubdivisionIndices( );

// ========= Axis aligned bounding boxes =========

//! Initialize with numeric_limits
template<size_t D> constexpr
BoundingBox<D> makeFullBoundingBox( );

template<size_t D> constexpr
BoundingBox<D> makeEmptyBoundingBox( );

template<size_t D> constexpr
BoundingBox<D> boundingBoxOr( const BoundingBox<D>& bounds1,
                              const BoundingBox<D>& bounds2 );

template<size_t D> constexpr
BoundingBox<D> boundingBoxOr( const BoundingBox<D>& bounds,
                              std::array<double, D> xyz );

template<size_t D> constexpr
BoundingBox<D> boundingBoxAnd( const BoundingBox<D>& bounds1,
                               const BoundingBox<D>& bounds2 );

template<size_t D> constexpr
BoundingBox<D> extendBoundingBox( const BoundingBox<D>& bounds,
                                  double relative = 1e-10,
                                  double absolute = 0.0 );

template<size_t D> constexpr
BoundingBox<D> boundingBoxAt( const std::array<double, D>& xyz, 
                              double width );

template<size_t D> constexpr
BoundingBox<D> boundingBoxAt( const std::array<double, D>& xyz,
                              const std::array<double, D>& lengths );

template<size_t D> constexpr
bool insideBoundingBox( const BoundingBox<D>& bounds, 
                        std::array<double, D> xyz );

template<size_t D> constexpr MLHP_PURE
bool boundingBoxIsValid( const BoundingBox<D>& bounds, double epsilon = 0.0 );

template<size_t D> constexpr
double boundingBoxVolume( const BoundingBox<D>& bounds );

template<size_t D> MLHP_EXPORT
BoundingBox<D> boundingBox( CoordinateConstSpan<D> coordinates );

template<size_t D>
BoundingBox<D> boundingBox( const std::array<double, D>& vertex0,
                            const std::array<double, D>& vertex1,
                            const std::array<double, D>& vertex2 );

template<size_t D> constexpr
bool boundingBoxIntersectsOther( const BoundingBox<D>& bounds0, 
                                 const BoundingBox<D>& bounds1 );

template<size_t D>
bool boundingBoxIntersectsRay( const spatial::BoundingBox<D>& bounds, 
                               const std::array<double, D>& rayOrigin,
                               const std::array<double, D>& rayDirection );

// ========= Spatial function objects =========

template<size_t D, typename... Args>
auto constantFunction( double value );

template<size_t I, size_t O = 1, typename... Args>
auto constantFunction( std::array<double, I> value );

//! Binds given spatial coordinate to a given value
template<size_t D, typename ReturnType, typename... Args>
auto slice( const std::function<ReturnType( std::array<double, D>, Args...)>& function, size_t axis, double value );

//! Binds last spatial coordinate to a given value
template<size_t D, typename ReturnType, typename... Args>
auto sliceLast( const std::function<ReturnType( std::array<double, D>, Args...)>& function, double value );

//! Peels last spatial coordinate into separate double parameter
template<size_t D>
auto peelLast( const ScalarFunction<D>& function );

//! Adds N dimensions
template<size_t N, size_t D>
auto expandDimension( const ScalarFunction<D>& function );

//! Activates function only if mask( xyz ) == true
template<size_t D> MLHP_EXPORT
ScalarFunction<D> mask( const ScalarFunction<D>& function,
                        const ImplicitFunction<D>& mask );

//! Gauss bell with value at center equals scaling
template<size_t D>
auto centerNormalizedGaussBell( std::array<double, D> center,
                                double sigma,
                                double scaling = 1.0 );

//! Gauss bell with integral over [-inf, inf]^D equals scaling
template<size_t D>
auto integralNormalizedGaussBell( std::array<double, D> center,
                                  double sigma,
                                  double scaling = 1.0 );

template<size_t D>
auto revolveAroundPath( const ScalarFunction<D>& function,
                        const ParameterFunction<D>& path,
                        const RealFunction& scaling );

// ========= Coordinate generators =========

template<size_t D>
auto makeGridPointGenerator( std::array<size_t, D> npoints,
                             std::array<double, D> lengths = array::make<D>( 1.0 ),
                             std::array<double, D> origin = array::make<D>( 0.0 ) );

template<size_t D>
auto makeRstGenerator( std::array<size_t, D> npoints, 
                       double scaling = 1.0 );

template<size_t D> MLHP_EXPORT
void cartesianTickVectors( std::array<size_t, D> ncells,
                           std::array<double, D> lengths,
                           std::array<double, D> origin,
                           CoordinateGrid<D>& target );

//! Equidistant points in the local coordinates for the given cell type
template<size_t D> MLHP_EXPORT
void distributeSeedPoints( CellType type, 
                           size_t nseedpoints, 
                           CoordinateList<D>& rst );

template<size_t D> MLHP_EXPORT
CoordinateGrid<D> cartesianTickVectors( std::array<size_t, D> ncells,
                                        std::array<double, D> lengths,
                                        std::array<double, D> origin );

template<size_t D> MLHP_EXPORT
CoordinateList<D> tensorProduct( const CoordinateGrid<D>& grid );

template<size_t D> MLHP_EXPORT
void tensorProduct( const CoordinateGrid<D>& grid, 
                    CoordinateList<D>& target );

//! Evently distributes points on sphere (approximately)
MLHP_EXPORT
void fibonacciSphere( CoordinateSpan<3> target );

MLHP_EXPORT
CoordinateList<3> fibonacciSphere( size_t n );

// ========= Homogeneous transformations =========

// Provides translate, scale, rotate, invert and operator(). 
// When suitable allows method chaining. Definition can be   
// found in _impl.hpp. Created using functions below.                                 
template<size_t D> 
struct HomogeneousTransformation;

//! Create homogeneous translation
template<size_t D> MLHP_EXPORT MLHP_PURE
HomogeneousTransformation<D> translate( std::array<double, D> vector );

//! Create homogeneous scaling
template<size_t D> MLHP_EXPORT
HomogeneousTransformation<D> scale( std::array<double, D> factors );

//! Create homogeneous rotation: 2D overload
MLHP_EXPORT
HomogeneousTransformation<2> rotate( double phi );

//! Create homogeneous rotation: 3D overload
MLHP_EXPORT
HomogeneousTransformation<3> rotate( std::array<double, 3> normal, double phi );

//! Create homogeneous rotation: Generic implementation
template<size_t D> MLHP_EXPORT
HomogeneousTransformation<D> rotate( std::array<double, D> v1,
                                     std::array<double, D> v2,
                                     double phi );

template<size_t D, typename... HomogeneousTransformations>
HomogeneousTransformation<D> concatenate( const HomogeneousTransformation<D>& transformation1,
                                          const HomogeneousTransformation<D>& transformation2,
                                          HomogeneousTransformations&&... transformations );

// Determine if and what spatial function an arbitrary object can be converted to
template<typename T> struct InspectFunctionImpl { static constexpr auto type = 0; };

template<utilities::DoubleCastable Result, size_t I>
struct InspectFunctionImpl<std::function<Result( std::array<double, I> )>>
{
    static constexpr auto type = 1;
    static constexpr auto idim = I;
};

template<utilities::DoubleCastable Result, size_t O, size_t I>
struct InspectFunctionImpl<std::function<std::array<Result, O>( std::array<double, I> )>>
{
    static constexpr auto type = 2;
    static constexpr auto idim = I;
    static constexpr auto odim = O;
};

template<typename Function>
using InspectFunction = InspectFunctionImpl<decltype( std::function { std::declval<Function>( ) })>;

template<typename Function> concept ConvertibleToScalarFunction = InspectFunction<Function>::type == 1;
template<typename Function> concept ConvertibleToVectorFunction = InspectFunction<Function>::type == 2;

} // namespace mlhp::spatial

namespace mlhp::solution
{

//! Gaussian bell travelling in space
template<size_t D> MLHP_EXPORT
spatial::ScalarFunction<D + 1> amLinearHeatSource( const spatial::ParameterFunction<D>& path,
                                                   const RealFunction& intensity,
                                                   double sigma );

template<size_t D> MLHP_EXPORT
spatial::ScalarFunction<D + 1> amLinearHeatSolution( const spatial::ParameterFunction<D>& path,
                                                     const RealFunction& intensity,
                                                     double capacity, double kappa,
                                                     double sigma, double dt,
                                                     double shift = 0.0 );

//! Standard ND Fichera cube / 1D singular example
template<size_t D> MLHP_EXPORT
spatial::ScalarFunction<D> singularSolution( );

template<size_t D> MLHP_EXPORT
spatial::VectorFunction<D, D> singularSolutionDerivatives( );

template<size_t D> MLHP_EXPORT
spatial::ScalarFunction<D> singularSolutionSource( );

} // namespace mlhp::solution

namespace mlhp
{

template<size_t D> constexpr auto operator+( std::array<double, D> arr1, std::array<double, D> arr2 );
template<size_t D> constexpr auto operator-( std::array<double, D> arr1, std::array<double, D> arr2 );
template<size_t D> constexpr auto operator*( std::array<double, D> arr1, std::array<double, D> arr2 );
template<size_t D> constexpr auto operator/( std::array<double, D> arr1, std::array<double, D> arr2 );

template<size_t D> constexpr auto operator+( std::array<double, D> arr, double value );
template<size_t D> constexpr auto operator-( std::array<double, D> arr, double value );
template<size_t D> constexpr auto operator*( std::array<double, D> arr, double value );
template<size_t D> constexpr auto operator/( std::array<double, D> arr, double value );

template<size_t D> constexpr auto operator+( double value, std::array<double, D> arr );
template<size_t D> constexpr auto operator-( double value, std::array<double, D> arr );
template<size_t D> constexpr auto operator*( double value, std::array<double, D> arr );
template<size_t D> constexpr auto operator/( double value, std::array<double, D> arr );

template<size_t D> std::ostream& operator<<( std::ostream& stream, std::array<double, D> coordinates );

} // namespace mlhp

#include "mlhp/core/spatial_impl.hpp"

#endif // MLHP_CORE_SPATIAL_HPP
