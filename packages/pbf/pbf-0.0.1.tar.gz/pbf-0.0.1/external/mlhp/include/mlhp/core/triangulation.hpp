// This file is part of the mlhp project. License: See LICENSE

#ifndef MLHP_CORE_TRIANGULATION_HPP
#define MLHP_CORE_TRIANGULATION_HPP

#include "mlhp/core/coreexport.hpp"
#include "mlhp/core/alias.hpp"
#include "mlhp/core/mesh.hpp"
#include "mlhp/core/kdtree.hpp"

namespace mlhp
{

template<size_t D>
struct Triangulation
{
    auto ntriangles( ) const { return triangles.size( ); }
    auto nvertices( ) const { return vertices.size( ); }

    MLHP_EXPORT MLHP_PURE
    std::array<size_t, 3> triangleIndices( size_t itriangle ) const;
    
    MLHP_EXPORT MLHP_PURE
    spatial::Triangle<D> triangleVertices( size_t itriangle ) const;

    MLHP_EXPORT
    spatial::BoundingBox<D> boundingBox( ) const;
    
    MLHP_EXPORT
    spatial::BoundingBox<D> boundingBox( size_t itriangle ) const;

	std::vector<std::array<double, D>> vertices;
	std::vector<std::array<size_t, 3>> triangles;
};

//! Read stl into vertex list
MLHP_EXPORT
CoordinateList<3> readStl( const std::string& filename,
                           bool flipOnOppositeNormal = false );

//! Create triangulation from vertex list
template<size_t D> MLHP_EXPORT
Triangulation<D> createTriangulation( CoordinateConstSpan<D> vertices );

MLHP_EXPORT
size_t countIntersections( const KdTree<3>& tree,
                           const Triangulation<3>& triangulation,
                           const std::array<double, 3>& rayOrigin,
                           const std::array<double, 3>& rayDirection,
                           std::vector<size_t>& triangleTarget );

class TriangulationDomain
{
public:
    using TriangulationPtr = memory::vptr<Triangulation<3>>;
    using KdTreePtr = memory::vptr<KdTree<3>>;

    MLHP_EXPORT
    TriangulationDomain( const std::string& stlfile );

    MLHP_EXPORT
    TriangulationDomain( const TriangulationPtr& triangulation );

    MLHP_EXPORT
    TriangulationDomain( const TriangulationPtr& triangulation,
                         const KdTreePtr& kdTree );

    MLHP_EXPORT
    std::any initialize( ) const;

    MLHP_EXPORT
    bool inside( std::array<double, 3> xyz, std::any& cache ) const;

private:
    TriangulationPtr triangulation_;
    KdTreePtr kdtree_;
};

template<size_t D> MLHP_EXPORT
KdTree<D> buildKdTree( const Triangulation<D>& triangulation,
                       const kdtree::Parameters& parameters = { } );

template<size_t D> MLHP_EXPORT
KdTree<D> buildKdTree( const Triangulation<D>& triangulation,
                       const spatial::BoundingBox<D>& bounds,
                       const kdtree::Parameters& parameters = { } );

namespace kdtree
{

template<size_t D> MLHP_EXPORT
kdtree::ObjectProvider<D> makeTriangleProvider( const Triangulation<D>& triangulation, bool clip = true );

}

//! Standard marching cubes
MLHP_EXPORT
Triangulation<3> marchingCubes( const ImplicitFunction<3>& function,
                                std::array<size_t, 3> ncells,
                                std::array<double, 3> lengths,
                                std::array<double, 3> origin = { } );

// Concepts to replace linker errors due to missing instantiation with compiler errors.
template <typename T>
concept MarchingCubesIndex = std::is_same_v<T, size_t> ||
                             std::is_same_v<T, std::int64_t>;

// Marching cubes in local coordinates. Creates actual cube shapes for uncut cubes.
template<MarchingCubesIndex IndexType> MLHP_EXPORT
void marchingCubesBoundary( const AbsMapping<3>& mapping,
                            const ImplicitFunction<3>& function,
                            const std::vector<bool>& evaluations,
                            const CoordinateGrid<3>& rstGrid,
                            std::array<size_t, 3> resolution,
                            CoordinateList<3>& rstList,
                            std::vector<IndexType>& triangles,
                            std::any& anyCache );

template<MarchingCubesIndex IndexType> MLHP_EXPORT
void marchingCubesVolume( const AbsMapping<3>& mapping,
                          const ImplicitFunction<3>& function,
                          const std::vector<bool>& evaluations,
                          const CoordinateGrid<3>& rstGrid,
                          std::array<size_t, 3> resolution,
                          CoordinateList<3>& rstList,
                          std::vector<IndexType>& connectivity,
                          std::vector<IndexType>& offsets,
                          std::any& anyCache );

//using CellAssociatedTriangles = std::pair<std::vector<double>, std::vector<CellIndex>>;
//
////! Marching cubes on mesh cells
//MLHP_EXPORT
//CellAssociatedTriangles marchingCubes( const ImplicitFunction<3>& function,
//                                       const AbsMesh<3>& mesh, 
//                                       size_t ncellsPerDirection );

template<size_t D>
struct CellAssociatedTriangulation
{
    Triangulation<D> triangulation;

    std::vector<std::array<double, 3>> rst;
    std::vector<size_t> triangleOffsets;
    std::vector<CellIndex> cells;

    MLHP_EXPORT
    operator Triangulation<D>& ( );

    MLHP_EXPORT
    operator const Triangulation<D>& ( ) const;
};

MLHP_EXPORT
CellAssociatedTriangulation<3> marchingCubesBoundary( const AbsMesh<3>& mesh,
                                                      const ImplicitFunction<3>& function,
                                                      std::array<size_t, 3> resolution );

// Marching cubes implementational details
namespace marchingcubes
{

MLHP_EXPORT
extern std::vector<std::vector<size_t>> tetrahedra;

MLHP_EXPORT
extern std::array<std::uint8_t, 2460> triangleData;

MLHP_EXPORT
extern std::array<std::uint16_t, 257> triangleIndices;

MLHP_EXPORT
extern std::array<std::uint16_t, 256> edgeTable;

MLHP_EXPORT
extern std::array<std::array<size_t, 2>, 12> numbering;

MLHP_EXPORT
std::array<double, 3> interpolate( const ImplicitFunction<3>& function,
                                   std::array<double, 3> c1, bool v1,
                                   std::array<double, 3> c2, bool v2 );

MLHP_EXPORT
std::array<double, 3> interpolate( const ImplicitFunction<3>& function,
                                   const AbsMapping<3>& mapping,
                                   std::array<double, 3> c1, bool v1,
                                   std::array<double, 3> c2, bool v2 );

MLHP_EXPORT
void evaluateGrid( const AbsMapping<3>& mapping,
                   const ImplicitFunction<3>& function,
                   std::array<size_t, 3> resolution,
                   std::array<std::vector<double>, 3>& rstGrid,
                   std::vector<bool>& evaluations );

} // marchingcubes
} // mlhp

#endif // MLHP_CORE_TRIANGULATION_HPP
