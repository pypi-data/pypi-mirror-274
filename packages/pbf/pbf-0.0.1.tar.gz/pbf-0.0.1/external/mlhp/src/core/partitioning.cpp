// This file is part of the mlhp project. License: See LICENSE

#include "mlhp/core/partitioning.hpp"
#include "mlhp/core/quadrature.hpp"
#include "mlhp/core/refinement.hpp"
#include "mlhp/core/polynomials.hpp"
#include "mlhp/core/arrayfunctions.hpp"
#include "mlhp/core/mesh.hpp"
#include "mlhp/core/spatial.hpp"

#include <array>

namespace mlhp
{

template<size_t D>
void mapQuadraturePointGrid( const AbsMapping<D>& mapping,
                             const CoordinateGrid<D>& rstGrid,
                             CoordinateList<D>& xyzList,
                             std::vector<double>& weights )
{
    auto orders = array::elementSizes( rstGrid );
    auto size = weights.size( );

    MLHP_CHECK( size == array::product( orders ), "Inconsistent sizes." );

    xyzList.resize( size );

    nd::executeWithIndex( orders, [&]( std::array<size_t, D> ijk, size_t i )
    {
        auto [xyz, detJ] = map::withDetJ( mapping, array::extract( rstGrid, ijk ) );

        xyzList[i] = xyz;
        weights[i] *= detJ;
    } );
}

template<size_t D>
void mapQuadraturePointLists( const AbsMapping<D>& mapping,
                              const CoordinateGrid<D>& rstLists,
                              CoordinateList<D>& xyzList,
                              std::vector<double>& weights )
{
    auto size = weights.size( );

    for( size_t axis = 0; axis < D; ++axis )
    {
        MLHP_CHECK( rstLists[axis].size( ) == size, "Inconsistent sizes" );
    }

    xyzList.resize( size );

    for( size_t i = 0; i < size; ++i )
    {
        auto rst = array::extract( rstLists, array::make<D>( i ) );
        auto [xyz, detJ] = map::withDetJ( mapping, rst );

        MLHP_CHECK( detJ > 0, "Jacobian is not positive." );

        xyzList[i] = xyz;
        weights[i] *= detJ;
    }
}

namespace
{

template<size_t D>
void internalSpaceTreeLeaves( const ImplicitFunction<D>& function, 
                              const AbsMapping<D>& mapping,
                              size_t depth, size_t nseedpoints,
                              auto&& append )
{
    auto generateRecursive = [&]( auto&& self, auto&& cell, size_t level ) -> void
    {
        auto result = int { 0 };
        auto fullMapping = [&]( ){ return ConcatenatedMapping<D>{ &mapping, &cell }; };

        if( level < depth && 0 == ( result = intersectionTest( function, fullMapping( ), nseedpoints ) ) )
        { 
            auto times = array::make<D>( size_t { 2 } );
            auto generator = makeCartesianMappingSplitter( cell, times );

            nd::execute( times, [&]( std::array<size_t, D> ijk )
            { 
                self( self, generator( ijk ), level + 1 );
            } );
        }
        else
        {
            append( cell, result, level );
        }
    };

    generateRecursive( generateRecursive, CartesianMapping<D> { }, 0 );
}

} // namespace

template<size_t D>
void generateSpaceTreeLeaves( const ImplicitFunction<D>& function,
                              const AbsMapping<D>& mapping,
                              size_t depth, size_t nseedpoints,
                              std::vector<CartesianMapping<D>>& cells )
{
    auto append = [&]( auto&& cell, auto&&, auto&& )
    {
        cells.push_back( cell );
    };

    internalSpaceTreeLeaves( function, mapping, depth, nseedpoints, append );
}

template<size_t D>
void generateSpaceTreeLeaves( const ImplicitFunction<D>& function,
                              const AbsMapping<D>& mapping,
                              size_t depth, size_t nseedpoints,
                              std::vector<CartesianMapping<D>>& cells,
                              std::vector<int>& cutState,
                              bool computeCutStateOfFinestCells )
{
    auto append = [&]( auto&& cell, auto&& cut, auto&& level )
    {
        if( computeCutStateOfFinestCells && level == depth )
        {
            auto fullMapping = ConcatenatedMapping<D>( &mapping, &cell );

            cut = intersectionTest( function, fullMapping, nseedpoints );
        }
    
        cells.push_back( cell );
        cutState.push_back( cut );
    };

    internalSpaceTreeLeaves( function, mapping, depth, nseedpoints, append );
}

template<size_t D>
struct SpaceTreeQuadrature<D>::Cache
{
    std::vector<CartesianMapping<D>> mappings;
    std::vector<int> cutState;
    const AbsMapping<D>* mapping;
    QuadraturePointCache quadrature;
};

template<size_t D>
SpaceTreeQuadrature<D>::SpaceTreeQuadrature( const ImplicitFunction<D>& function, double alpha, size_t depth ) :
    function_( function ), depth_( depth ), alphaFCM_( alpha ), numberOfSeedPoints_( 5 )
{ }

template<size_t D>
QuadratureCache<D> SpaceTreeQuadrature<D>::initialize( ) const
{
    return Cache { };
}

template<size_t D>
size_t SpaceTreeQuadrature<D>::partition( const MeshMapping<D>& mapping,
                                          QuadratureCache<D>& anyCache ) const
{
    MLHP_CHECK( mapping.type == CellType::NCube, "Space tree only works on n-cubes." );

    auto& data = anyCache.template cast<Cache>( );

    data.mapping = &mapping;
    data.mappings.resize( 0 );
    data.cutState.resize( 0 );

    generateSpaceTreeLeaves( function_, mapping, depth_, numberOfSeedPoints_, data.mappings, data.cutState );

    return data.mappings.size( );
}

template<size_t D>
bool SpaceTreeQuadrature<D>::distribute( size_t ipartition,
                                         std::array<size_t, D> orders,
                                         CoordinateGrid<D>& rst,
                                         CoordinateList<D>& xyzList,
                                         std::vector<double>& weights,
                                         QuadratureCache<D>& anyCache ) const
{
    auto& data = anyCache.template cast<Cache>( );

    tensorProductQuadrature( orders, rst, weights, data.quadrature );

    auto detJ = data.mappings[ipartition].mapGrid( rst );
    auto cut = data.cutState[ipartition];

    mapQuadraturePointGrid( *data.mapping, rst, xyzList, weights );

    for( size_t ipoint = 0; ipoint < xyzList.size( ); ++ipoint )
    {
        weights[ipoint] *= ( cut == -1 || ( cut == 0 && !function_( xyzList[ipoint] ) ) ) ? alphaFCM_ * detJ : detJ;
    }

    return true;
}

template<size_t D>
bool SpaceTreeQuadrature<D>::distributeForMomentFitting( size_t ipartition,
                                                         std::array<size_t, D> orders,
                                                         CoordinateGrid<D>& rst,
                                                         CoordinateGrid<D>& weightsGrid,
                                                         std::vector<double>& weights,
                                                         QuadratureCache<D>& anyCache ) const
{
    auto& data = anyCache.template cast<Cache>( );

    auto intersection = data.cutState[ipartition];

    tensorProductQuadrature( orders, rst, weightsGrid, data.quadrature );

    weights.resize( array::product( orders ) );

    double detJ = data.mappings[ipartition].mapGrid( rst );

    // Do intersection test on gauss points if cell was not checked
    if( intersection == 0 )
    {
        size_t count = 0;

        nd::executeWithIndex( orders, [&]( std::array<size_t, D> ijk, size_t i )
        {
            bool isInside = function_( data.mapping->map( array::extract( rst, ijk ) ) );

            count = count + static_cast<size_t>( isInside );

            weights[i] = isInside ? 1.0 : alphaFCM_;
        } );

        intersection = count == 0 ? -1 : ( count == array::product( orders ) ? 1 : 0 );
    }
    
    // Either distribute tensor product of weights or the weights in each axis
    if( intersection == 0 )
    {
        nd::executeWithIndex( orders, [&]( std::array<size_t, D> ijk, size_t i )
        {
            weights[i] *= array::product( array::extract( weightsGrid, ijk ) ) * detJ;
        } );
    }
    else
    {
        utilities::scaleVector( weightsGrid[0], detJ * ( intersection == 1 ? 1.0 : alphaFCM_ ) );
    }

    return intersection == 0;
}

template<size_t D>
void SpaceTreeQuadrature<D>::setNumberOfSeedPoints( size_t numberOfSeedPoints )
{
    numberOfSeedPoints_ = numberOfSeedPoints;
}

template<size_t D>
struct MomentFittingQuadrature<D>::Cache
{
    const AbsMapping<D>* mapping;

    size_t numberOfPartitions;

    CoordinateGrid<D> lagrangeEvaluation;
    CoordinateGrid<D> coordinateGrid;
    CoordinateGrid<D> weightsGrid;
    CoordinateList<D> coordinateList;
    std::vector<double> rhsWeights;
    QuadraturePointCache quadrature;

    QuadratureCache<D> spaceTreeCache;
};

template<size_t D>
MomentFittingQuadrature<D>::MomentFittingQuadrature( const ImplicitFunction<D>& function, 
                                                     double alpha, 
                                                     size_t depth,
                                                     bool adaptOrders ) :
    function_( function ), rhsPartitioner_( function, alpha, depth ), adaptOrders_( adaptOrders )
{ }

template<size_t D>
QuadratureCache<D> MomentFittingQuadrature<D>::initialize( ) const
{
    Cache cache;

    cache.spaceTreeCache = rhsPartitioner_.initialize( );

    return cache;
}

template<size_t D>
size_t MomentFittingQuadrature<D>::partition( const MeshMapping<D>& mapping,
                                              QuadratureCache<D>& anyCache ) const
{
    MLHP_CHECK( mapping.type == CellType::NCube, "Moment fitting only works on n-cubes." );

    auto& data = anyCache.template cast<Cache>( );

    data.mapping = &mapping;
    data.numberOfPartitions = rhsPartitioner_.partition( mapping, data.spaceTreeCache );

    return 1;
}

template<size_t D>
bool MomentFittingQuadrature<D>::distribute( size_t,
                                             std::array<size_t, D> orders,
                                             CoordinateGrid<D>& rstGrid,
                                             CoordinateList<D>& xyzList,
                                             std::vector<double>& weights,
                                             QuadratureCache<D>& anyCache ) const
{
    auto& data = anyCache.template cast<Cache>( );
    
    if( data.numberOfPartitions == 1 )
    {
        rhsPartitioner_.distribute( 0, orders, rstGrid, xyzList, weights, data.spaceTreeCache );
    }
    else
    {
        if( adaptOrders_ )
        {
            orders = array::multiply<size_t>( orders, 2 );
        }

        weights.resize( array::product( orders ) );
        xyzList.resize( array::product( orders ) );

        tensorProductQuadrature( orders, rstGrid, data.quadrature );

        std::fill( weights.begin( ), weights.end( ), 0.0 );
        
        for( size_t iPartition = 0; iPartition < data.numberOfPartitions; ++iPartition )
        {
            auto& subRst = data.coordinateGrid;
            auto& lagrange = data.lagrangeEvaluation;

            // Distribute tensor product of weights if cut, otherwise only distribute weights in each axis
            bool cut = rhsPartitioner_.distributeForMomentFitting( iPartition, orders, subRst, data.weightsGrid,
                                                                   data.rhsWeights, data.spaceTreeCache );

            // Pre-evaluate all lagrange polynomials in each coordinate axis for each integration point
            for( size_t axis = 0; axis < D; ++axis )
            {
                lagrange[axis].resize( orders[axis] * orders[axis] );

                polynomial::lagrange( orders[axis] - 1, orders[axis], rstGrid[axis].data( ), subRst[axis].data( ), lagrange[axis].data( ) );
            }

            // Loop over moment fitting points (on root cell) and add integral of associated Lagrange function
            nd::executeWithIndex( orders, [&]( std::array<size_t, D> ijk1, size_t index1 )
            {
                auto offsets = array::multiply( ijk1, orders );

                // Integrate current Lagrage function by summing tensor product of leaf quadrature points
                if( cut )
                {
                    // Remove the innermost loop (that we add manually for performance)
                    auto slicedOrders = array::sliceIfNotOne( orders, D - 1 );

                    nd::executeWithIndex( slicedOrders, [&]( decltype( slicedOrders ) ijk2, size_t index2 )
                    {
                        double shapes = 1.0;

                        // Pre compute N1 * N2 * ... Nd - 1
                        for( size_t axis = 0; axis < ijk2.size( ); ++axis )
                        {   
                            shapes *= lagrange[axis][offsets[axis] + ijk2[axis]];
                        }
                     
                        // Multiply with evaluations of Nd and the integration point weight
                        for( size_t iPoint = 0; iPoint < orders[D - 1]; ++iPoint )
                        {
                            double value = shapes * lagrange[D - 1][offsets[D - 1] + iPoint];

                            weights[index1] += value * data.rhsWeights[index2 * orders[D - 1] + iPoint];
                        }
                    } );
                }
                // If cell is not cut we can simplify this N-D integral to a product of 1-D integrals
                else
                {
                    double integralND = 1.0;

                    for( size_t axis = 0; axis < D; ++axis )
                    {
                        double integral1D = 0.0;

                        for( size_t iPoint = 0; iPoint < orders[axis]; ++iPoint )
                        {
                            integral1D += lagrange[axis][offsets[axis] + iPoint] * data.weightsGrid[axis][iPoint];
                        }

                        integralND *= integral1D;
                    }

                    weights[index1] += integralND;
                }
            } );

        } // for iPartition

        nd::executeWithIndex( orders, [&]( std::array<size_t, D> ijk, size_t i )
        {
            auto [xyz, detJ] = map::withDetJ( *data.mapping, array::extract( rstGrid, ijk ) );

            xyzList[i] = xyz;
            weights[i] *= detJ;
        } );
    }

    return true;
}

template<size_t D>
void MomentFittingQuadrature<D>::setNumberOfSeedPoints( size_t numberOfSeedPoints )
{
    rhsPartitioner_.setNumberOfSeedPoints( numberOfSeedPoints );
}

template<size_t D>
struct StandardQuadrature<D>::Cache
{
    QuadraturePointCache quadrature;
    const AbsMapping<D>* mapping;
};

template<size_t D>
QuadratureCache<D> StandardQuadrature<D>::initialize( ) const
{
    return Cache { };
}

template<size_t D>
size_t StandardQuadrature<D>::partition( const MeshMapping<D>& mapping,
                                         QuadratureCache<D>& anyCache ) const
{
    anyCache.template cast<Cache>( ).mapping = &mapping;

    return 1;
}

template<size_t D>
bool StandardQuadrature<D>::distribute( size_t,
                                        std::array<size_t, D> orders,
                                        CoordinateGrid<D>& rst,
                                        CoordinateList<D>& xyz,
                                        std::vector<double>& weights,
                                        QuadratureCache<D>& anyCache ) const
{

    auto& data = anyCache.template cast<Cache>( );

    if( data.mapping->type == CellType::NCube )
    {
        tensorProductQuadrature( orders, rst, weights, data.quadrature );
        mapQuadraturePointGrid( *data.mapping, rst, xyz, weights );

        return true;
    }
    else
    {
        MLHP_CHECK( data.mapping->type == CellType::Simplex, "Unknown cell type" );
        
        simplexQuadrature<D>( orders, rst, weights, data.quadrature );
        mapQuadraturePointLists<D>( *data.mapping, rst, xyz, weights );

        return false;
    }
}

template<size_t D>
struct CachedQuadrature<D>::CellCache
{ 
    size_t npartitions = 0;

    std::vector<double> data = { };
    std::vector<size_t> offsets = { 0 };

    void addPartition( const CoordinateGrid<D>& rstGrid,
                       const CoordinateList<D>& xyzList,
                       const std::vector<double>& weights );

    void getPartition( size_t ipartition,
                       CoordinateGrid<D>& rstGrid,
                       CoordinateList<D>& xyzList,
                       std::vector<double>& weights );
};

template<size_t D>
void CachedQuadrature<D>::CellCache::addPartition( const CoordinateGrid<D>& rstGrid,
                                                   const CoordinateList<D>& xyzList,
                                                   const std::vector<double>& weights )
{
    offsets.resize( offsets.size( ) + D + 2 );

    auto rstOffsets = offsets.data( ) + offsets.size( ) - D - 3;
    auto& xyzOffset = offsets[offsets.size( ) - 3];
    auto& weightsOffset = offsets[offsets.size( ) - 2];

    for( size_t axis = 0; axis + 1 < D; ++axis )
    {
        rstOffsets[axis + 1] = rstOffsets[axis] + rstGrid[axis].size( );
    }
    
    xyzOffset = rstOffsets[D - 1] + rstGrid.back( ).size( );
    weightsOffset = xyzOffset + xyzList.size( ) * D;
    offsets.back( ) = weightsOffset + weights.size( );

    data.resize( offsets.back( ) );
    
    for( size_t axis = 0; axis < D; ++axis )
    {
        std::copy( rstGrid[axis].begin( ), rstGrid[axis].end( ), data.begin( ) + 
            static_cast<std::ptrdiff_t>( rstOffsets[axis] ) );
    }
    
    for( size_t ipoint = 0; ipoint < xyzList.size( ); ++ipoint )
    {
        for( size_t axis = 0; axis < D; ++axis )
        {
            data[xyzOffset + D * ipoint + axis] = xyzList[ipoint][axis];
        }
    }
    
    std::copy( weights.begin( ), weights.end( ), data.begin( ) + 
        static_cast<std::ptrdiff_t>( weightsOffset ) );
}

template<size_t D>
void CachedQuadrature<D>::CellCache::getPartition( size_t ipartition,
                                                   CoordinateGrid<D>& rstGrid,
                                                   CoordinateList<D>& xyzList,
                                                   std::vector<double>& weights )
{
    auto begin = ipartition * ( D + 2 );
    auto rstOffsets = offsets.data( ) + begin;
    auto xyzOffset = offsets[begin + D];
    auto weightsOffset = offsets[begin + D + 1];
        
    for( size_t axis = 0; axis < D; ++axis )
    {
        rstGrid[axis].resize( rstOffsets[axis + 1] - rstOffsets[axis] );

        std::copy( data.begin( ) + static_cast<std::ptrdiff_t>( rstOffsets[axis] ),
                   data.begin( ) + static_cast<std::ptrdiff_t>( rstOffsets[axis + 1] ),
                   rstGrid[axis].begin( ) );
    }

    xyzList.resize( ( weightsOffset - xyzOffset ) / D );
    weights.resize( xyzList.size( ) );

    for( size_t ipoint = 0; ipoint < xyzList.size( ); ++ipoint )
    {
        for( size_t axis = 0; axis < D; ++axis )
        {
            xyzList[ipoint][axis] = data[xyzOffset + D * ipoint + axis];
        }
    }

    std::copy( data.begin( ) + static_cast<std::ptrdiff_t>( weightsOffset ), 
               data.begin( ) + static_cast<std::ptrdiff_t>( weightsOffset + xyzList.size( ) ),
               weights.begin( ) );
}

template<size_t D>
CachedQuadrature<D>::CachedQuadrature( const AbsMesh<D>& mesh, 
                                       const std::vector<std::array<size_t, D>>& degrees,
                                       const AbsQuadrature<D>& partitioner ) :
    points_ { std::make_shared<std::vector<CellCache>>( mesh.ncells( ) ) },
    data_( 0 ), offsets_( 0 ), partitions_( mesh.ncells( ) + 1, 0 )
{
    auto ncells = mesh.ncells( );

    MLHP_CHECK( degrees.size( ) == ncells, "Inconsistent sizes." );
    
    #pragma omp parallel
    {
        auto partitionerCache = partitioner.initialize( );
        auto mapping = mesh.createMapping( );
        auto rstGrid = CoordinateGrid<D> { };
        auto xyzList = CoordinateList<D> { };
        auto weights = std::vector<double>{ };
        auto data = std::vector<double> { };
        auto sizes = std::vector<size_t> { };
        auto cells = std::vector<CellIndex>{ };

        #pragma omp for
        for( std::int64_t ii = 0; ii < static_cast<std::int64_t>( ncells ); ++ii )
        {
            auto icell = static_cast<CellIndex>( ii );
        
            cells.push_back( icell );

            mesh.prepareMapping( icell, mapping );

            partitions_[icell + 1] = partitioner.partition( mapping, partitionerCache );

            for( size_t ipartition = 0; ipartition < partitions_[icell + 1]; ++ipartition )
            {
                auto isGrid = partitioner.distribute( ipartition, degrees[icell], 
                    rstGrid, xyzList, weights, partitionerCache );

                MLHP_CHECK( isGrid, "Does cached integration partitioner work for non-grids?" );

                size_t id = sizes.size( );

                sizes.resize( id + D + 2 );

                for( size_t axis = 0; axis < D; ++axis )
                {
                    sizes[id + axis] = rstGrid[axis].size( );
                }

                sizes[id + D + 0] = xyzList.size( ) * D;
                sizes[id + D + 1] = weights.size( );

                auto offsets = std::array<size_t, D + 3> { 0 };

                std::partial_sum( sizes.data( ) + id, sizes.data( ) + id + D + 2, offsets.data( ) + 1 );

                offsets = array::add( offsets, data.size( ) );

                data.resize( offsets.back( ) );
                    
                for( size_t axis = 0; axis < D; ++axis )
                {
                    std::copy( rstGrid[axis].begin( ), rstGrid[axis].end( ), data.data( ) + offsets[axis] );
                }
                    
                for( size_t ipoint = 0; ipoint < xyzList.size( ); ++ipoint )
                {
                    for( size_t axis = 0; axis < D; ++axis )
                    {
                        data[offsets[D] + D * ipoint + axis] = xyzList[ipoint][axis];
                    }
                }
                
                std::copy( weights.begin( ), weights.end( ), data.data( ) + offsets[D + 1] );
            }

        } // for ii
        
        #pragma omp barrier
        { }

        #pragma omp single
        {
            std::partial_sum( partitions_.begin( ), partitions_.end( ), partitions_.begin( ) );

            offsets_.resize( partitions_.back( ) * ( D + 2 ) + 1 );
        }

        size_t offset = 0;

        for( auto icell : cells )
        {
            for( auto ipartition = partitions_[icell]; ipartition < partitions_[icell + 1]; ++ipartition )
            {
                for( size_t i = 0; i < D + 2; ++i )
                {
                    offsets_[ipartition * ( D + 2 ) + i + 1] = sizes[offset++];
                }
            }
        }
        
        #pragma omp barrier
        { }

        #pragma omp single
        {
            std::partial_sum( offsets_.begin( ), offsets_.end( ), offsets_.begin( ) );

            data_.resize( offsets_.back( ) );
        }

        offset = 0;

        for( auto icell : cells )
        {
            for( auto ipartition = partitions_[icell]; ipartition < partitions_[icell + 1]; ++ipartition )
            {
                auto offset0 = offsets_[( D + 2 ) * ipartition];
                auto offset1 = offsets_[( D + 2 ) * ( ipartition + 1 )];
                auto size = offset1 - offset0;

                std::copy( data.data( ) + offset, data.data( ) + offset + size, data_.data( ) + offset0 );
               
                offset += size;
            }
        }
    } // omp parallel 
}

template<size_t D>
QuadratureCache<D> CachedQuadrature<D>::initialize( ) const
{
    return CellIndex { 0 };
}

template<size_t D>
size_t CachedQuadrature<D>::partition( const MeshMapping<D>& mapping,
                                       QuadratureCache<D>& anyCache ) const 
{
    MLHP_CHECK( mapping.type == CellType::NCube, "Does cached integration partitioner work for non-grids?" );

    auto& icell = anyCache.template cast<CellIndex>( );

    icell = mapping.icell;

    return partitions_[icell + 1] - partitions_[icell];
}

template<size_t D>
bool CachedQuadrature<D>::distribute( size_t ipartition,
                                      std::array<size_t, D>,
                                      CoordinateGrid<D>& rstGrid,
                                      CoordinateList<D>& xyzList,
                                      std::vector<double>& weights,
                                      QuadratureCache<D>& anyCache ) const 
{
    auto cellOffset = partitions_[anyCache.template cast<CellIndex>( )] + ipartition;
    auto offsets = offsets_.data( ) + ( cellOffset + ipartition ) * ( D + 2 );

    for( size_t axis = 0; axis < D; ++axis )
    {
        rstGrid[axis].resize( offsets[axis + 1] - offsets[axis] );

        std::copy( data_.data( ) + offsets[axis], data_.data( ) + 
            offsets[axis + 1], rstGrid[axis].begin( ) );
    }

    xyzList.resize( ( offsets[D + 1] - offsets[D] ) / D );
    weights.resize( xyzList.size( ) );
    
    for( size_t ipoint = 0; ipoint < xyzList.size( ); ++ipoint )
    {
        for( size_t axis = 0; axis < D; ++axis )
        {
            xyzList[ipoint][axis] = data_[offsets[D] + D * ipoint + axis];
        }
    }
    
    std::copy( data_.data( ) + offsets[D + 1], data_.data( ) + 
        offsets[D + 2], weights.begin( ) );

    return true;
}

template<size_t D>
MeshProjectionQuadrature<D>::MeshProjectionQuadrature( const AbsHierarchicalGrid<D>& otherMesh,
                                                       const AbsQuadrature<D>& partitioner ) :
    otherMesh_( &otherMesh ),
    partitioner_( &partitioner )
{ }

template<size_t D>
QuadratureCache<D> MeshProjectionQuadrature<D>::initialize( ) const
{
    return Cache { };
}

template<size_t D>
struct MeshProjectionQuadrature<D>::Cache
{
    using PartitionData = std::tuple<MeshMapping<D>, ConcatenatedMapping<D>, QuadratureCache<D>, size_t>;

    std::vector<mesh::SharedSupport<D>> cells;
    std::vector<PartitionData> data;
    std::vector<size_t> mapToSubcell;
};

template<size_t D>
size_t MeshProjectionQuadrature<D>::partition( const MeshMapping<D>& mapping,
                                               QuadratureCache<D>& anyCache ) const
{
     auto mesh = dynamic_cast<const AbsHierarchicalGrid<D>*>( mapping.mesh );
     
     MLHP_CHECK( mapping.type == CellType::NCube, "Mesh intersection only works on grids." );
     MLHP_CHECK( mesh != nullptr && mesh->baseGrid( ).ncells( ) == otherMesh_->baseGrid( ).ncells( ),
                 "Mesh intersection requires identical base meshes." );

     auto& cache = anyCache.template cast<Cache>( );
     auto& data = cache.data;

     cache.cells.resize( 0 );
     cache.mapToSubcell.resize( 0 );

     // Generate partitions 
     mesh::findInOtherGrid( *mesh, *otherMesh_, cache.cells, mesh->fullIndex( mapping.icell ) );
     
     // Resize and initialize cache
     auto nsubcells = cache.cells.size( );
     auto previousSize = data.size( );

     data.resize( std::max( nsubcells, previousSize ) );

     for( size_t isubcell = previousSize; isubcell < nsubcells; ++isubcell )
     {
        std::get<2>( data[isubcell] ) = partitioner_->initialize( );
     }

     auto offset = size_t { 0 };

     // For each subcell: prepare mapping, partition subcell, append to backward index map
     for( size_t isubcell = 0; isubcell < cache.cells.size( ); ++isubcell )
     {
         auto& [subMeshMapping, subMapping, stdany, npartitions] = data[isubcell];

         subMapping.globalMapping = &mapping;
         subMapping.localMapping = &cache.cells[isubcell].thisCell;
         subMeshMapping.reset( *mapping.mesh, subMapping, mapping.icell );

         npartitions = partitioner_->partition( subMeshMapping, stdany );

         cache.mapToSubcell.resize( cache.mapToSubcell.size( ) + npartitions, isubcell );

         std::swap( npartitions, offset );
         offset += npartitions;
     }

     return offset;
}

template<size_t D>
CellIndex MeshProjectionQuadrature<D>::distribute( size_t ipartition,
                                                   std::array<size_t, D> orders,
                                                   CoordinateGrid<D>& thisRstGrid,
                                                   CoordinateGrid<D>& otherRstGrid,
                                                   CoordinateList<D>& xyzList,
                                                   std::vector<double>& weights,
                                                   QuadratureCache<D>& anyCache ) const
{
    auto& cache = anyCache.template cast<Cache>( );
    auto& isubcell = cache.mapToSubcell[ipartition];
    auto& [meshMapping, mapping, stdany, offset] = cache.data[isubcell];

    partitioner_->distribute( ipartition - offset, orders, 
        thisRstGrid, xyzList, weights, stdany );

    std::copy( thisRstGrid.begin( ), thisRstGrid.end( ), otherRstGrid.begin( ) );

    cache.cells[isubcell].thisCell.mapGrid( thisRstGrid );
    cache.cells[isubcell].otherCell.mapGrid( otherRstGrid );

    return cache.cells[isubcell].otherIndex;
}

template<size_t D>
bool MeshProjectionQuadrature<D>::distribute( size_t ipartition,
                                              std::array<size_t, D> orders,
                                              CoordinateGrid<D>& rstGrid,
                                              CoordinateList<D>& xyzList,
                                              std::vector<double>& weights,
                                              QuadratureCache<D>& anyCache ) const
{
    auto& cache = anyCache.template cast<Cache>( );
    auto& isubcell = cache.mapToSubcell[ipartition];
    auto& [meshMapping, mapping, stdany, offset] = cache.data[isubcell];

    partitioner_->distribute( ipartition - offset, orders, 
        rstGrid, xyzList, weights, stdany );
    
    cache.cells[isubcell].thisCell.mapGrid( rstGrid );

    return true;
}

#define MLHP_INSTANTIATE_DIM( D )                                             \
                                                                              \
    template class SpaceTreeQuadrature<D>;                                    \
    template class MomentFittingQuadrature<D>;                                \
    template class StandardQuadrature<D>;                                     \
    template class CachedQuadrature<D>;                                       \
    template class MeshProjectionQuadrature<D>;                               \
                                                                              \
    template MLHP_EXPORT                                                      \
    void mapQuadraturePointGrid( const AbsMapping<D>& mapping,                \
                                 const CoordinateGrid<D>& rstGrid,            \
                                 CoordinateList<D>& xyzList,                  \
                                 std::vector<double>& weights );              \
                                                                              \
    template MLHP_EXPORT                                                      \
    void mapQuadraturePointLists( const AbsMapping<D>& mapping,               \
                                    const CoordinateGrid<D>& rst,             \
                                    CoordinateList<D>& xyzList,               \
                                    std::vector<double>& weights );           \
                                                                              \
    template MLHP_EXPORT                                                      \
    void generateSpaceTreeLeaves( const ImplicitFunction<D>& function,        \
                                  const AbsMapping<D>& mapping,               \
                                  size_t depth,                               \
                                  size_t nseedpoints,                         \
                                  std::vector<CartesianMapping<D>>& cells,    \
                                  std::vector<int>& cutState,                 \
                                  bool computeCutStateOfFinestCells );        \
                                                                              \
    template MLHP_EXPORT                                                      \
    void generateSpaceTreeLeaves( const ImplicitFunction<D>& function,        \
                                  const AbsMapping<D>& mapping,               \
                                  size_t depth,                               \
                                  size_t nseedpoints,                         \
                                  std::vector<CartesianMapping<D>>& cells );

    MLHP_DIMENSIONS_XMACRO_LIST
#undef MLHP_INSTANTIATE_DIM

} // mlhp
