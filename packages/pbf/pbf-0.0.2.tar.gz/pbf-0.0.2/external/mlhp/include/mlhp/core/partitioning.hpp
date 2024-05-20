// This file is part of the mlhp project. License: See LICENSE

#ifndef MLHP_CORE_PARTITIONING_HPP
#define MLHP_CORE_PARTITIONING_HPP

#include "mlhp/core/alias.hpp"
#include "mlhp/core/mapping.hpp"
#include "mlhp/core/sparse.hpp"

#include <any>

namespace mlhp
{
        
//! Simple depth-first quadtree refined towards the implicitly defined boundary 
template<size_t D> MLHP_EXPORT
void generateSpaceTreeLeaves( const ImplicitFunction<D>& function,
                              const AbsMapping<D>& mapping,
                              size_t depth, 
                              size_t nseedpoints,
                              std::vector<CartesianMapping<D>>& cells );

//! Also store whether cells were outside (-1), cut (0), or inside (1). Cells at full depth are 
//! not refined, making an intersection test unnecessary. When computeCutStateOfFinestCells is 
//! active, this test is done regardless, otherwise full depth cells are always considered cut.
template<size_t D> MLHP_EXPORT
void generateSpaceTreeLeaves( const ImplicitFunction<D>& function,
                              const AbsMapping<D>& mapping,
                              size_t depth, 
                              size_t nseedpoints,
                              std::vector<CartesianMapping<D>>& cells,
                              std::vector<int>& cutState,
                              bool computeCutStateOfFinestCells = false );

template<size_t D> MLHP_EXPORT
void mapQuadraturePointGrid( const AbsMapping<D>& mapping,
                             const CoordinateGrid<D>& rstGrid,
                             CoordinateList<D>& xyzList,
                             std::vector<double>& weights );

template<size_t D> MLHP_EXPORT
void mapQuadraturePointLists( const AbsMapping<D>& mapping,
                              const CoordinateGrid<D>& rstLists,
                              CoordinateList<D>& xyzList,
                              std::vector<double>& weights );

template<size_t D>
using QuadratureCache = utilities::UniqueTypeErasedCache<AbsQuadrature<D>>;

template<size_t D>
class AbsQuadrature : utilities::DefaultVirtualDestructor
{
public:

    // Initialize thread-local data
    virtual QuadratureCache<D> initialize( ) const = 0;
    
    // Generate partition and store data in cache
    virtual size_t partition( const MeshMapping<D>& mapping,
                              QuadratureCache<D>& anyCache ) const = 0;

    // Distribute integration points for given partition. Returns true if points form
    // a grid. If so, rst contains the grid coordinate ticks, so that an integration point
    // in 3D at grid indices i, j, k is accessed as (rst[0][i], rst[1][j], rst[2][k]). 
    // If no grid, the coordinates at index i are (rst[0][i], rst[1][i], rst[2][i]).
    // The global coordinates in xyz are never considered grids.
    virtual bool distribute( size_t ipartition,
                             std::array<size_t, D> orders,
                             CoordinateGrid<D>& rst,
                             CoordinateList<D>& xyzList,
                             std::vector<double>& weights,
                             QuadratureCache<D>& anyCache ) const = 0;
};

template<size_t D>
class StandardQuadrature final : public AbsQuadrature<D>
{
public:
    MLHP_EXPORT 
    QuadratureCache<D> initialize( ) const override;

    MLHP_EXPORT 
    size_t partition( const MeshMapping<D>& mapping,
                      QuadratureCache<D>& anyCache ) const override;
        
    MLHP_EXPORT 
    bool distribute( size_t ipartition,
                     std::array<size_t, D> orders,
                     CoordinateGrid<D>& rst,
                     CoordinateList<D>& xyzList,
                     std::vector<double>& weights,
                     QuadratureCache<D>& anyCache ) const override;

private:
    struct Cache;
};

template<size_t D>
class SpaceTreeQuadrature final : public AbsQuadrature<D>
{
public:
    MLHP_EXPORT 
    SpaceTreeQuadrature( const ImplicitFunction<D>& function, 
                         double alpha, 
                         size_t depth );

    MLHP_EXPORT 
    QuadratureCache<D> initialize( ) const override;

    MLHP_EXPORT 
    size_t partition( const MeshMapping<D>& mapping,
                      QuadratureCache<D>& anyCache ) const override;

    MLHP_EXPORT 
    bool distribute( size_t ipartition,
                     std::array<size_t, D> orders,
                     CoordinateGrid<D>& rst,
                     CoordinateList<D>& xyzList,
                     std::vector<double>& weights,
                     QuadratureCache<D>& anyCache ) const override;

    MLHP_EXPORT 
    void setNumberOfSeedPoints( size_t numberOfSeedPoints );

    //! For moment fitting
    MLHP_EXPORT 
    bool distributeForMomentFitting( size_t ipartition,
                                     std::array<size_t, D> orders,
                                     CoordinateGrid<D>& rst,
                                     CoordinateGrid<D>& weightsGrid,
                                     std::vector<double>& weights,
                                     QuadratureCache<D>& anyCache ) const;

private:
    ImplicitFunction<D> function_;
    size_t depth_;
    double alphaFCM_;
    size_t numberOfSeedPoints_;

    struct Cache;
};

template<size_t D>
class MomentFittingQuadrature final : public AbsQuadrature<D>
{
public:
    MLHP_EXPORT 
    MomentFittingQuadrature( const ImplicitFunction<D>& function, 
                             double alpha, 
                             size_t depth,
                             bool adaptOrders = true );

    MLHP_EXPORT 
    QuadratureCache<D> initialize( ) const override;

    MLHP_EXPORT 
    size_t partition( const MeshMapping<D>& mapping,
                      QuadratureCache<D>& anyCache ) const override;

    MLHP_EXPORT 
    bool distribute( size_t ipartition,
                     std::array<size_t, D> orders,
                     CoordinateGrid<D>& rst,
                     CoordinateList<D>& xyzList,
                     std::vector<double>& weights,
                     QuadratureCache<D>& anyCache ) const override;

    MLHP_EXPORT 
    void setNumberOfSeedPoints( size_t numberOfSeedPoints );

private:
    ImplicitFunction<D> function_;
    SpaceTreeQuadrature<D> rhsPartitioner_;
    
    bool adaptOrders_;

    struct Cache;
};

template<size_t D>
class CachedQuadrature final : public AbsQuadrature<D>
{
public:
    using IntegrationOrders = std::function<std::array<size_t, D>( CellIndex ielement )>;

    MLHP_EXPORT 
    CachedQuadrature( const AbsMesh<D>& mesh, 
                      const std::vector<std::array<size_t, D>>& degrees,
                      const AbsQuadrature<D>& partitioner );

    MLHP_EXPORT 
    QuadratureCache<D> initialize( ) const override;

    MLHP_EXPORT 
    size_t partition( const MeshMapping<D>& mapping,
                      QuadratureCache<D>& anyCache ) const override;
        
    MLHP_EXPORT 
    bool distribute( size_t ipartition,
                     std::array<size_t, D> orders,
                     CoordinateGrid<D>& rst,
                     CoordinateList<D>& xyzList,
                     std::vector<double>& weights,
                     QuadratureCache<D>& anyCache ) const override;

private:
    struct CellCache;
    std::shared_ptr<std::vector<CellCache>> points_;

    std::vector<double> data_;
    std::vector<size_t> offsets_;
    std::vector<size_t> partitions_;
};

//! Partitions conforming with another mesh (from e.g. a previous time step).
template<size_t D>
class MeshProjectionQuadrature final : public AbsQuadrature<D>
{
public:
    MLHP_EXPORT 
    MeshProjectionQuadrature( const AbsHierarchicalGrid<D>& otherMesh,
                              const AbsQuadrature<D>& partitioner );

    MLHP_EXPORT 
    QuadratureCache<D> initialize( ) const override;

    MLHP_EXPORT 
    size_t partition( const MeshMapping<D>& mapping,
                      QuadratureCache<D>& anyCache) const override;
             
    MLHP_EXPORT 
    bool distribute( size_t ipartition,
                     std::array<size_t, D> orders,
                     CoordinateGrid<D>& rst,
                     CoordinateList<D>& xyzList,
                     std::vector<double>& weights,
                     QuadratureCache<D>& anyCache ) const override;

    MLHP_EXPORT 
    CellIndex distribute( size_t ipartition,
                          std::array<size_t, D> orders,
                          CoordinateGrid<D>& thisRstGrid,
                          CoordinateGrid<D>& otherRstGrid,
                          CoordinateList<D>& xyzList,
                          std::vector<double>& weights,
                          QuadratureCache<D>& anyCache) const;

public:
    const AbsHierarchicalGrid<D>* otherMesh_;
    const AbsQuadrature<D>* partitioner_;

    struct Cache;
};

} // mlhp

#endif // MLHP_CORE_PARTITIONING_HPP
