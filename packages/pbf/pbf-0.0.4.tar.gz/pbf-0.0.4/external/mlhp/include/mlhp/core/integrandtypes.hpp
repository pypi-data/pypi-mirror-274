// This file is part of the mlhp project. License: See LICENSE

#ifndef MLHP_CORE_INTEGRANDTYPES_HPP
#define MLHP_CORE_INTEGRANDTYPES_HPP

#include "mlhp/core/alias.hpp"
#include "mlhp/core/memory.hpp"
#include "mlhp/core/utilities.hpp"

namespace mlhp
{

template<size_t D>
class DomainIntegrand
{
public:

    using Cache = utilities::UniqueTypeErasedCache<DomainIntegrand>;

    // Construct using simple evaluation function.
    using Evaluate1 = std::function<void( const BasisFunctionEvaluation<D>& shapes, 
                                          AlignedDoubleVectors& targets, double weightDetJ )>;
    
    DomainIntegrand( AssemblyTypeVector types,
                     DiffOrders maxDiffOrder,
                     const Evaluate1& evaluate ) :
        types_( types ), diffOrder_( maxDiffOrder )
    { 
        create_ = []( ){ return std::any { }; };
        prepare_ = []( auto&&... ) noexcept { };

        evaluate_ = [=]( Cache&, const BasisFunctionEvaluation<D>& shapes,
                         AlignedDoubleVectors& targets, double weightDetJ )
        { 
            evaluate( shapes, targets, weightDetJ );
        };
    }

    // Construct evaluator with also location map, element index and temporary storage. 
    using Evaluate2 = std::function<void( const BasisFunctionEvaluation<D>& shapes,
                                          const LocationMap& locationMap, 
                                          AlignedDoubleVectors& targets, 
                                          AlignedDoubleVector& tmp,
                                          double weightDetJ )>;

    struct Cache2
    { 
        const LocationMap* locationMap; 
        memory::AlignedVector<double> tmp;
    };

    DomainIntegrand( DiffOrders maxDiffOrder, AssemblyTypeVector types, const Evaluate2& evaluate ) :
        types_( types ), diffOrder_( maxDiffOrder )
    { 
        create_ = []( ) { return Cache2 { .locationMap = nullptr, .tmp = { } }; };

        prepare_ = []( Cache& anyCache, size_t, const LocationMap& locationMap )
        {
            auto& cache = anyCache.template cast<Cache2>( );
            cache.locationMap = &locationMap;
        };

        evaluate_ = [=]( Cache& anyCache, const BasisFunctionEvaluation<D>& shapes,
                         AlignedDoubleVectors& targets, double weightDetJ )
        { 
            auto& cache = anyCache.template cast<Cache2>( );

            evaluate( shapes, *cache.locationMap, targets, cache.tmp, weightDetJ );
        };
    }

    // Generic constructor
    using Create = std::function<Cache( )>;

    using Prepare = std::function<void( Cache& cache, size_t elementIndex,
                                        const LocationMap& locationMap )>;
    
    using Evaluate = std::function<void( Cache& cache, const BasisFunctionEvaluation<D>& shapes,
                                         AlignedDoubleVectors& targets, double weightDetJ )>;

    DomainIntegrand( AssemblyTypeVector types, DiffOrders maxDiffOrder,
                     const Create& create, const Prepare& prepare, const Evaluate& evaluate ) :
        types_( types ), diffOrder_( maxDiffOrder ), 
        create_( create ), prepare_( prepare ), evaluate_( evaluate )
    { }

    // Evaluation functions
    Cache createCache( ) const { return create_( ); }

    void prepare( Cache& cache, size_t ielement, const LocationMap& locationMap ) const
    { 
        return prepare_( cache, ielement, locationMap );
    }

    void evaluate( Cache& cache, const BasisFunctionEvaluation<D>& shapes,
                   AlignedDoubleVectors& targets, double weightDetJ ) const
    {
        evaluate_( cache, shapes, targets, weightDetJ );
    }

    AssemblyTypeVector types( ) const { return types_; }
    DiffOrders diffOrder( ) const { return diffOrder_; }

private:
    AssemblyTypeVector types_;
    DiffOrders diffOrder_;
    Create create_;
    Prepare prepare_;
    Evaluate evaluate_;
};

template<size_t D>
class BasisProjectionIntegrand
{
public:
    using Evaluate = std::function<void( const LocationMap& locationMap0,
                                         const LocationMap& locationMap1,
                                         const BasisFunctionEvaluation<D>& shapes0,
                                         const BasisFunctionEvaluation<D>& shapes1,
                                         AlignedDoubleVectors& targets,
                                         double weightDetJ )>;

    BasisProjectionIntegrand( AssemblyTypeVector types,
                              DiffOrders diffOrder,
                              const Evaluate& evaluate ) :
        types_( types ), diffOrder_( diffOrder ), evaluate_( evaluate )
    { }

    void evaluate( const LocationMap& locationMap0,
                   const LocationMap& locationMap1,
                   const BasisFunctionEvaluation<D>& shapes0,
                   const BasisFunctionEvaluation<D>& shapes1,
                   AlignedDoubleVectors& targets,
                   double weightDetJ ) const
    {
        return evaluate_( locationMap0, locationMap1, 
            shapes0, shapes1, targets, weightDetJ );
    }

    DiffOrders diffOrder( ) const { return diffOrder_; }
    AssemblyTypeVector types( ) const { return types_; }

private:
    AssemblyTypeVector types_;
    DiffOrders diffOrder_;
    Evaluate evaluate_;
};

template<size_t D>
class SurfaceIntegrand
{
public:
    using Evaluate = std::function<void( const BasisFunctionEvaluation<D>& shapes,
                                         const LocationMap& locationMap,
                                         std::array<double, D> normal,
                                         AlignedDoubleVectors& targets,
                                         double weightDetJ )>;

    SurfaceIntegrand( const AssemblyTypeVector& types, 
                      DiffOrders diffOrder, 
                      const Evaluate& evaluate ) :
        types_( types ), difforder_( diffOrder ), evaluate_( evaluate )
    { }

    void evaluate( const BasisFunctionEvaluation<D>& shapes, 
                   const LocationMap& locationMap,
                   std::array<double, D> normal,
                   AlignedDoubleVectors& targets,
                   double weightDetJ ) const
    {
        evaluate_( shapes, locationMap, normal, targets, weightDetJ );
    }

    AssemblyTypeVector types( ) const { return types_; }
    DiffOrders diffOrder( ) const { return difforder_; }

private:
    AssemblyTypeVector types_;
    DiffOrders difforder_;
    Evaluate evaluate_;
};

} // mlhp

#endif // MLHP_CORE_INTEGRANDTYPES_HPP
