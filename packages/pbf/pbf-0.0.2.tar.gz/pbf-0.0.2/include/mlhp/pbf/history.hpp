// This file is part of the mlhpbf project. License: See LICENSE

#ifndef MLHPBF_HISTORY_HPP
#define MLHPBF_HISTORY_HPP

#include "mlhp/core.hpp"

namespace mlhp
{

template<size_t D, typename T>
struct HistoryContainer
{
    using Initialize = std::function<T( std::array<double, D> xyz )>;

    HistoryContainer( ) :
        grid { makeRefinedGrid<D>( array::makeSizes<D>( 1 ), array::make<D>( 1.0 ) ) },
        data ( 1, T { } ), maxdepth { 0 }
    { }

    HistoryContainer( const HierarchicalGridSharedPtr<D>& grid_,
                      const Initialize& initialize,
                      RefinementLevel maxdepth_ ) :
        grid { grid_ }, data( grid_->ncells( ) ), maxdepth { maxdepth_ }, 
        createBackwardMapping { grid_->createBackwardMappingFactory( ) }
    { 
        auto ncells = static_cast<std::int64_t>( grid->ncells( ) );

        #pragma omp parallel
        {
            auto mapping = grid->createMapping( );

            #pragma omp for
            for( std::int64_t ii = 0; ii < ncells; ++ii )
            {
                auto icell = static_cast<CellIndex>( ii );

                grid->prepareMapping( icell, mapping );

                data[icell] = initialize( mapping( { } ) );
            }
        }
    }

    HistoryContainer( const HierarchicalGridSharedPtr<D>& grid_, 
                      RefinementLevel maxdepth_,
                      std::vector<T>&& data_ ) :
        grid { grid_ }, data( std::move( data_ ) ), maxdepth { maxdepth_ },
        createBackwardMapping { grid_->createBackwardMappingFactory( ) }
    { 
        MLHP_CHECK( grid->ncells( ) == data.size( ), "Inconsistent history array size." );
    }

    T* operator() ( std::array<double, D> xyz )
    {
        thread_local std::unique_ptr<AbsBackwardMapping<D>> mapping;

        if( !mapping || &mapping->mesh( ) != grid.get( ) )
        {
            mapping = createBackwardMapping( );
        }

        if( auto result = mapping->map( xyz ); result )
        {
            return &data[result->first];
        }
        else
        {
            return nullptr;
        }
    }

    const T* operator() ( std::array<double, D> xyz ) const
    {
        return const_cast<HistoryContainer*>( this )->operator() ( xyz );
    }

    HierarchicalGridSharedPtr<D> grid;
    std::vector<T> data;
    RefinementLevel maxdepth;
    BackwardMappingFactory<D> createBackwardMapping;
};

enum class MaterialType : size_t 
{ 
    BasePlate = 0, 
    Structure = 1, 
    Powder    = 2, 
    Air       = 3 
};

struct HistoryData
{
    MaterialType materialType;
};

template<size_t D>
using ThermoplasticHistory = HistoryContainer<D, HistoryData>;

template<size_t D> inline
ThermoplasticHistory<D> initializeHistory( const GridSharedPtr<D>& baseGrid,
                                           const ImplicitFunction<D>& part,
                                           double powderHeight,
                                           size_t nseedpoints, 
                                           size_t maxdepth ) 
{
    auto materialInitializer = [=]( std::array<double, D> xyz )
    {
        if( xyz[2] < 0.0 )
        {
            return MaterialType::BasePlate;
        }
        else if( xyz[2] > powderHeight )
        {
            return MaterialType::Air;
        }
        else
        {
            return part( xyz ) ? MaterialType::Structure : MaterialType::Powder;
        }
    };

    // Refine to material interface and top level
    auto refinement = [&]( const MeshMapping<D>& mapping, 
                           RefinementLevel level )
    {
        auto refine = false;

        if( level < maxdepth )
        {
            auto pointsPerDirection = array::make<D>( nseedpoints );
            auto rstGenerator = spatial::makeRstGenerator( pointsPerDirection, 0.99 );
            auto ijk0 = array::makeSizes<D>( 0 );
            auto initialType = materialInitializer( mapping.map( rstGenerator( ijk0 ) ) );

            nd::execute( pointsPerDirection, [&]( std::array<size_t, D> ijk )
            {
                if( refine == false && ijk != ijk0 )
                {
                    auto xyz = mapping.map( rstGenerator( ijk ) );

                    refine = materialInitializer( xyz ) != initialType;
                }
            } );
        }

        return refine;
    };

    auto grid = makeRefinedGrid<D>( baseGrid );

    grid->refine( refinement );

    auto initialize = [&]( std::array<double, D> xyz )
    {
        return HistoryData { .materialType = materialInitializer( xyz ) };
    };

    return ThermoplasticHistory<D>( grid, initialize, static_cast<RefinementLevel>( maxdepth ) );
}

template<size_t D> inline
ThermoplasticHistory<D> initializeHistory( const GridSharedPtr<D>& baseGrid,
                                           double powderHeight,
                                           size_t maxdepth ) 
{
    return initializeHistory<D>( baseGrid, utilities::returnValue( false ), powderHeight, 4, maxdepth );
}

struct PowderMaterial
{
    static constexpr auto Tm = 1320.0;// * Units::C;
};

namespace detail
{

template<size_t D> inline
void evaluateTemperature( const MultilevelHpBasis<D>& tbasis, 
                          const std::vector<double>& tdofs, 
                          const ThermoplasticHistory<D>& history, 
                          auto&& levelFunction )
{
    auto ntelements = tbasis.nelements( );

    // Determine cells inside melt pool
    #pragma omp parallel
    {
        auto subcells = std::vector<mesh::SharedSupport<D>> { };
        auto shapes = BasisFunctionEvaluation<D> { };
        auto cache = tbasis.createEvaluationCache( );
        auto locationMap = LocationMap { };
        auto seedgrid = CoordinateGrid<D> { };
        auto seedbounds = std::array { array::make<D>( 2.0 ), array::make<D>( -1.0 ) };

        #pragma omp for
        for( std::int64_t ii = 0; ii < static_cast<std::int64_t>( ntelements ); ++ii )
        {
            auto icell = static_cast<CellIndex>( ii );

            utilities::resize0( subcells, locationMap );

            mesh::findInOtherGrid( tbasis.hierarchicalGrid( ), *history.grid,
                subcells, tbasis.hierarchicalGrid( ).fullIndex( icell ) );

            tbasis.prepareEvaluation( icell, 0, shapes, cache );
            tbasis.locationMap( icell, locationMap );

            for( CellIndex isubcell = 0; isubcell < subcells.size( ); ++isubcell )
            {
                auto hindex = subcells[isubcell].otherIndex;

                if( history.data[hindex].materialType == MaterialType::Powder || 
                    history.data[hindex].materialType == MaterialType::BasePlate )
                {
                    auto evaluate = [&]( size_t nseedpoints )
                    {
                        spatial::cartesianTickVectors( array::makeSizes<D>( nseedpoints - 1 ), 
                            seedbounds[0], seedbounds[1], seedgrid );

                        subcells[isubcell].thisCell.mapGrid( seedgrid );

                        tbasis.prepareGridEvaluation( seedgrid, cache );

                        auto melted = false;
                        auto Tmax = std::numeric_limits<double>::min( );
                        auto limits = array::makeSizes<D>( nseedpoints );

                        nd::execute( limits, [&]( std::array<size_t, D> ijk )
                        {
                            if( !melted ) 
                            {
                                tbasis.evaluateGridPoint( ijk, shapes, cache );
                                    
                                auto T = evaluateSolution( shapes, locationMap, tdofs );
                                
                                Tmax = std::max( Tmax, T );

                                if( T >= PowderMaterial::Tm )
                                {
                                    melted = true;

                                    levelFunction( hindex );
                                }
                            }
                        } );

                        return std::pair { Tmax, melted };
                    };

                    if( auto [Tmax, melted] = evaluate( 3 ); !melted && Tmax > 0.5 * PowderMaterial::Tm )
                    {
                        evaluate( 6 );
                    }
                }
            }
        }
    } // omp parallel
}

template<size_t D> inline
ThermoplasticHistory<D> createNewHistoryAndInterpolate( const ThermoplasticHistory<D>& oldHistory,
                                                        const std::vector<int>& indicator )
{
    auto newGrid = makeRefinedGrid( *oldHistory.grid, indicator );
    auto ncells = newGrid->ncells( );
    auto newData = std::vector<HistoryData>( ncells );

    #pragma omp parallel
    {
        auto subcells = std::vector<mesh::SharedSupport<D>> { };

        #pragma omp for
        for( std::int64_t ii = 0; ii < static_cast<std::int64_t>( ncells ); ++ii )
        {
            auto icell = static_cast<CellIndex>( ii );

            utilities::resize0( subcells );

            mesh::findInOtherGrid( *newGrid, *oldHistory.grid,
                subcells, newGrid->fullIndex( icell ) );

            newData[icell] = oldHistory.data[subcells[0].otherIndex];
        }
    } // pragma omp parallel

    return ThermoplasticHistory<D>( newGrid, oldHistory.maxdepth, std::move( newData ) );
}

template<size_t D> inline
ThermoplasticHistory<D> refineHistory( const ThermoplasticHistory<D>& history,
                                       const MultilevelHpBasis<D>& tbasis,
                                       const std::vector<double>& tdofs )
{
    auto refine = std::vector<int>( history.grid->ncells( ), 0 );

    auto updateIndicator = [&]( auto hindex )
    {
        auto level = history.grid->refinementLevel( history.grid->fullIndex( hindex ) );

        refine[hindex] = static_cast<int>( history.maxdepth ) - static_cast<int>( level );
    };

    detail::evaluateTemperature( tbasis, tdofs, history, updateIndicator );

    return createNewHistoryAndInterpolate( history, refine );
}

template<size_t D> inline
void updateMaterial( ThermoplasticHistory<D>& history,
                     const MultilevelHpBasis<D>& tbasis, 
                     const std::vector<double>& tdofs )
{
    // Then update the material state (for the newly created cells)
    auto updatePowder = [&]( auto hindex )
    {
        history.data[hindex].materialType = MaterialType::Structure;
    };

    detail::evaluateTemperature( tbasis, tdofs, history, updatePowder );
}
        
template<size_t D> inline
ThermoplasticHistory<D> coarsenHistory( const ThermoplasticHistory<D>& fineHistory )
{
    auto adapt = std::vector<int>( fineHistory.grid->ncells( ), 0 );
    auto nroots = fineHistory.grid->baseGrid( ).ncells();

    auto recursive = [&]( auto&& self, CellIndex ifull ) -> std::pair<HistoryData, bool>
    {
        if( auto child = fineHistory.grid->child( ifull, { } ); child != NoCell )
        {
            auto [value, coarsen] = self( self, child );
            auto limits = array::make<D>( LocalPosition { 2 } );
                    
            // Determine material values of children are equal
            nd::execute( limits, [&]( auto ijk )
            {
                if( ijk != std::array<LocalPosition, D> { } )
                {
                    auto [valueI, coarsenI] = self( self, fineHistory.grid->child( ifull, ijk ) );

                    coarsen = coarsen && coarsenI && ( valueI.materialType == value.materialType );
                }
            } );

            if( coarsen )
            {
                nd::execute( limits, [&]( auto ijk )
                {
                    if( auto child2 = fineHistory.grid->child( ifull, ijk ); fineHistory.grid->isLeaf( child2 ) )
                    {
                        adapt[fineHistory.grid->leafIndex( child2 )] = std::numeric_limits<int>::min( );
                    }
                } );
            }

            return { value, coarsen };
        }
        else
        {
            return { fineHistory.data[fineHistory.grid->leafIndex( ifull )], true };
        }
    };

    for( CellIndex iroot = 0; iroot < nroots; ++iroot )
    {
        recursive( recursive, iroot );
    }

    return createNewHistoryAndInterpolate( fineHistory, adapt );
}
                    
} // detail

template<size_t D> inline
auto updateHistory( const ThermoplasticHistory<D>& history,
                    const MultilevelHpBasis<D>& tbasis, 
                    const std::vector<double>& tdofs )
{
    // Refine powder cells above the melting temperature to max depth
    auto fineHistory = detail::refineHistory( history, tbasis, tdofs );

    // Update newly created finer powder cells 
    detail::updateMaterial( fineHistory, tbasis, tdofs );

    // Coarsen history cells with equal material 
    return detail::coarsenHistory( fineHistory );
}

} // namespace mlhp

#endif // MLHPBF_HISTORY_HPP
