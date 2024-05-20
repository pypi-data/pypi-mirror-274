// This file is part of the mlhp project. License: See LICENSE

#include "pybind11/pybind11.h"
#include "pybind11/functional.h"
#include "pybind11/stl.h"

#include "mlhp/core.hpp"

#include "src/python/helper.hpp"

#include <sstream>
#include <iomanip>

namespace mlhp::bindings
{

template<size_t D>
void defineSpatialFunctions( pybind11::module& m )
{
    m.def( add<D>( "makeConstantFunction" ).c_str( ), []( double value )
    {
        return ScalarFunctionWrapper<D>( spatial::constantFunction<D>( value ) );
    } );
        
    m.def( add<D>( "makeConstantFunction" ).c_str( ), []( std::array<double, D> value )
    {
        return VectorFunctionWrapper<D>( spatial::constantFunction<D, D>( value ) );
    } );
       
    m.def( "sliceLast", []( const ScalarFunctionWrapper<D + 1>& function, double value )
    {
        return ScalarFunctionWrapper<D>{ spatial::sliceLast( 
            static_cast<spatial::ScalarFunction<D + 1>>( function ), value ) };
    } );

    m.def( add<D>( "makeSingularSolution" ).c_str( ), []( )
    { 
        return ScalarFunctionWrapper<D>{ solution::singularSolution<D>( ) };
    } );

    m.def( add<D>( "makeSingularSolutionSource" ).c_str( ), []( )
    { 
        return ScalarFunctionWrapper<D>{ solution::singularSolutionSource<D>( ) };
    } );

    m.def( add<D>( "makeSingularSolutionDerivatives" ).c_str( ), []( )
    { 
        return VectorFunctionWrapper<D> { solution::singularSolutionDerivatives<D>( ) };
    } );
        
    m.def( add<D>( "makeAmLinearHeatSource" ).c_str( ), []( const SpatialParameterFunctionWrapper<D>& path,
                                                            const RealFunctionWrapper& intensity,
                                                            double sigma )
    { 
        return ScalarFunctionWrapper<D + 1>{ solution::amLinearHeatSource<D>( path, intensity, sigma )};
    } );
        
    m.def( add<D>( "makeAmLinearHeatSolution" ).c_str( ), []( const SpatialParameterFunctionWrapper<D>& path,
                                                              const RealFunctionWrapper& intensity,
                                                              double capacity, double kappa,
                                                              double sigma, double dt, double shift )
    { 
        return ScalarFunctionWrapper<D + 1>{ solution::amLinearHeatSolution<D>( 
            path, intensity, capacity, kappa, sigma, dt, shift ) };
    } );
        
    // Remove these once we found a way of parsing functions in python
    if constexpr( D <= 3 )
        m.def( "makeAmLinearHeatPath", []( std::array<double, D> lengths ) { 
            return SpatialParameterFunctionWrapper<D>( [=]( double t ) noexcept {
                if constexpr( D == 1 ) return std::array { 0.6 * t + 0.2 };
                if constexpr( D == 2 ) return std::array { 0.6 * t + 0.2, lengths[1] / 2.0 };
                if constexpr( D == 3 ) return std::array { 0.6 * t + 0.2, lengths[1] / 2.0, lengths[2] }; 
            } ); } );
    if constexpr( D == 3 )
        m.def( "makeAmLinearHeatIntensity", []( ) { return RealFunctionWrapper( 
            [=]( double t ) noexcept { return std::min( t / 0.05, 1.0 ); } ); } );
}

template<size_t D>
void defineGrid( pybind11::module& m )
{
    auto registerMeshStr = []<typename Type, typename...Args>( pybind11::class_<Type, Args...>& pybindclass, std::string type )
    {
        auto str = [=]( const Type& mesh )
        {
            std::ostringstream os;

            os << type << "<" << D << "> (adress: " << &mesh << ")\n";
            os << "    ncells       : " << mesh.ncells( ) << std::endl;
            os << "    memory usage : " << utilities::memoryUsageString( mesh.memoryUsage( ) ) << std::endl;

            return os.str( );
        };

        pybindclass.def( "__str__", str );
    };

    auto __str__ = []( const HierarchicalGridSharedPtr<D>& grid )
    { 
        std::ostringstream os;

        print( *grid, os );

        return os.str( );
    };

    auto refine = []( AbsHierarchicalGrid<D>& self,
                      const RefinementFunctionWrapper<D>& refinement )
    { 
        self.refine( refinement );
    };

    auto neighbours = []( const AbsMesh<D>& mesh, CellIndex icell, size_t iface )
    {
        auto target = std::vector<MeshCellFace> { };

        mesh.neighbours( icell, iface, target );

        return target;
    };
    
    auto absMesh = pybind11::class_<AbsMesh<D>, MeshSharedPtr<D>> 
        ( m, add<D>( "AbsMesh" ).c_str( ) );

    absMesh.def( "ncells", &AbsMesh<D>::ncells );
    absMesh.def( "nfaces", &AbsMesh<D>::nfaces );
    absMesh.def( "ndim", []( const AbsMesh<D>& ) { return D; } );
    absMesh.def( "cellType", &AbsMesh<D>::cellType );
    absMesh.def( "memoryUsage", &AbsMesh<D>::memoryUsage );
    absMesh.def( "neighbours", neighbours );

    auto absGrid = pybind11::class_<AbsGrid<D>, AbsMesh<D>, GridSharedPtr<D>>
        ( m, add<D>( "AbsGrid" ).c_str( ) );
    
    registerMeshStr( absGrid, "AbsGrid" );
    
    auto cartesianGrid = pybind11::class_<CartesianGrid<D>, AbsGrid<D>, CartesianGridSharedPtr<D>>
        ( m, add<D>( "CartesianGrid" ).c_str( ) );
    
    cartesianGrid.def( "boundingBox", []( const CartesianGrid<D>& grid ) { return grid.boundingBox( ); } );
    
    registerMeshStr( cartesianGrid, "CartesianGrid" );
    
    m.def( "makeGrid", &makeCartesianGrid<D>,
           pybind11::arg( "nelements" ),
           pybind11::arg( "lengths" ) = array::make<D>( 1.0 ),
           pybind11::arg( "origin" ) = array::make<D>( 0.0 ) );
    
    pybind11::class_<AbsHierarchicalGrid<D>, AbsMesh<D>, HierarchicalGridSharedPtr<D>>
        ( m, add<D>( "AbsHierarchicalGrid" ).c_str( ) )
        .def( "nleaves", &AbsHierarchicalGrid<D>::nleaves )
        .def( "refine", refine )
        .def( "__str__", __str__ );

    auto refinedGrid = pybind11::class_<RefinedGrid<D>, AbsHierarchicalGrid<D>, std::shared_ptr<RefinedGrid<D>>>
        ( m, add<D>( "RefinedGrid" ).c_str( ) );
    
    using FactoryType = HierarchicalGridSharedPtr<D>( std::array<size_t, D>,
                                                      std::array<double, D>, 
                                                      std::array<double, D> );

    m.def( "makeRefinedGrid", static_cast<FactoryType*>( makeRefinedGrid<D> ),
           pybind11::arg( "nelements" ),
           pybind11::arg( "lengths" ) = array::make<D>( 1.0 ),
           pybind11::arg( "origin" ) = array::make<D>( 0.0 ) );
    
    m.def( "makeRefinedGrid", []( GridSharedPtr<D> grid ) { return makeRefinedGrid<D>( grid ); },
        pybind11::arg( "grid" ) );
    
    pybind11::class_<ImplicitFunctionWrapper<D>>( m, add<D>( "ImplicitFunction" ).c_str( ) )
        .def( "__call__", &ImplicitFunctionWrapper<D>::call );

    pybind11::class_<RefinementFunctionWrapper<D>>( m, add<D>( "RefinementFunction" ).c_str( ) )
        .def( "__call__", &RefinementFunctionWrapper<D>::call );

    m.def( "makeImplicitSphere", []( std::array<double, D> center, double radius )
        { return ImplicitFunctionWrapper<D>{ implicit::sphere( center, radius ) }; },
        pybind11::arg( "center" ), pybind11::arg( "radius" ) );

    m.def( "makeImplicitCube", []( std::array<double, D> x1, std::array<double, D> x2 )
        { return ImplicitFunctionWrapper<D>{ implicit::cube( x1, x2 ) }; },
        pybind11::arg( "corner1" ), pybind11::arg( "corner2" ) );
    
    m.def( "makeImplicitEllipsoid", []( std::array<double, D> origin, std::array<double, D> radii )
        { return ImplicitFunctionWrapper<D>{ implicit::ellipsoid( origin, radii ) }; },
        pybind11::arg( "origin" ), pybind11::arg( "radii" ) );
    
    m.def( "makeImplicitThreshold", []( const ScalarFunctionWrapper<D>& function, 
                                       double threshold, double sign ) -> ImplicitFunctionWrapper<D>
        { return implicit::threshold( function.get( ), threshold, sign ); },
        pybind11::arg( "function" ), pybind11::arg( "threshold" ) = 0.0, pybind11::arg( "sign" ) = true );

    m.def( "invert", []( const ImplicitFunctionWrapper<D>& function )
        { return ImplicitFunctionWrapper<D>{ implicit::invert<D>( function ) }; },
        pybind11::arg( "function" ) );
          
    m.def( "extrude", []( const ImplicitFunctionWrapper<D>& function, double minValue, double maxValue, size_t axis )
        { return ImplicitFunctionWrapper<D + 1>{ implicit::extrude<D>( function, minValue, maxValue, axis ) }; },
        pybind11::arg( "function" ), pybind11::arg( "minValue" ), pybind11::arg( "maxValue" ), pybind11::arg( "axis" ) = D );

    m.def( "refineTowardsBoundary", []( const ImplicitFunctionWrapper<D>& function,
                                        size_t maxDepth,
                                        size_t numberOfSeedPoints )
    {
        return RefinementFunctionWrapper<D>{ refineTowardsDomainBoundary<D>( 
            function, maxDepth, numberOfSeedPoints ) };
    }, pybind11::arg( "function" ), pybind11::arg( "maxDepth" ), 
       pybind11::arg( "numberOfSeedPoints" ) = 7 );

    m.def( "refineInsideDomain", []( const ImplicitFunctionWrapper<D>& function,
                                     size_t maxDepth,
                                     size_t numberOfSeedPoints )
    {
        return RefinementFunctionWrapper<D>{ refineInsideDomain<D>(
            function, maxDepth, numberOfSeedPoints ) };
    }, pybind11::arg( "function" ), pybind11::arg( "maxDepth" ), 
       pybind11::arg( "numberOfSeedPoints" ) = 7 );

    m.def( "refinementOr", []( const RefinementFunctionWrapper<D>& function1,
                               const RefinementFunctionWrapper<D>& function2 )
    {
        return RefinementFunctionWrapper<D>{ refinementOr<D>( function1, 
            static_cast<RefinementFunction<D>>( function2 ) ) };
    } );
}

template<size_t D>
void defineMesh( pybind11::module& m )
{
    auto printMesh = []( const UnstructuredMesh<D>& mesh )
    { 
        std::ostringstream os;

        print( mesh, os );

        return os.str( );
    };

    pybind11::class_<UnstructuredMesh<D>, AbsMesh<D>, std::shared_ptr<UnstructuredMesh<D>>>
        ( m, add<D>( "UnstructuredMesh" ).c_str( ) ) 
        .def( "__str__", printMesh );

    m.def( "makeUnstructuredMesh", []( CoordinateList<D>&& rst,
                                       std::vector<size_t>&& connectivity,
                                       std::vector<size_t>&& offsets )
        { return std::make_shared<UnstructuredMesh<D>>( std::move( rst ), 
            std::move( connectivity ), std::move( offsets ) ); },
        pybind11::arg( "nelements" ),
        pybind11::arg( "lengths" ) = array::make<D>( 1.0 ),
        pybind11::arg( "origin" ) = array::make<D>( 0.0 ) );
    
}

void defineBasisSingle( pybind11::module& m )
{
    pybind11::class_<AnsatzTemplateVector>( m, "AnsatzTemplateVector" );

    pybind11::class_<PolynomialDegreeTuple>( m, "PolynomialDegreeTuple" )
        .def( pybind11::init<size_t>( ) )
        .def( pybind11::init<const std::vector<size_t>&>( ) );

    pybind11::class_<UniformGrading>( m, "UniformGrading", 
        "Same polynomial degrees everywhere." )
        .def( pybind11::init<PolynomialDegreeTuple>( ),
              pybind11::arg( "uniformDegrees" ) );

    pybind11::class_<LinearGrading>( m, "LinearGrading",
        "Set degrees on finest elements. Increment degrees by one per level coarser." )
        .def( pybind11::init<PolynomialDegreeTuple>( ),
              pybind11::arg( "fineDegrees" ) );

    pybind11::class_<InterpolatedGrading>( m, "InterpolatedGrading",
        "Interpolate between degrees on root elements and finest elements." )
        .def( pybind11::init<PolynomialDegreeTuple, 
                             PolynomialDegreeTuple>( ),
              pybind11::arg( "rootDegrees" ), pybind11::arg( "fineDegrees" ) );
}

template<size_t D, GradingConcept Grading>
void defineBasisFactoryWithGrading( pybind11::module& m )
{
    using FactoryType = MultilevelHpBasisSharedPtr<D>( 
        const HierarchicalGridSharedPtr<D>&, const Grading&, size_t );
    
    m.def( "makeHpTensorSpace", static_cast<FactoryType*>( makeHpBasis<TensorSpace> ),
           "Create tensor space multi-level hp basis with custom polynomial grading.",
           pybind11::arg( "grid" ), pybind11::arg( "grading" ), pybind11::arg( "nfields" ) = 1 );

    m.def( "makeHpTrunkSpace", static_cast<FactoryType*>( makeHpBasis<TrunkSpace> ),
           "Create trunk space multi-level hp basis with custom polynomial grading.",
           pybind11::arg( "grid" ), pybind11::arg( "grading" ), pybind11::arg( "nfields" ) = 1 );

    auto ptr1 = &makeHpBasisFactory<TensorSpace, D, Grading>;
    auto ptr2 = &makeHpBasisFactory<TrunkSpace, D, Grading>;

    m.def( add<D>( "makeHpTensorSpaceFactory" ).c_str( ), ptr1, "Create factory that creates tensor "
           "space hp bases with custom polynomial degree distribution.", pybind11::arg( "degrees" ) );

    m.def( add<D>( "makeHpTrunkSpaceFactory" ).c_str( ), ptr2, "Create factory that creates trunk "
           "space hp bases with custom polynomial degree distribution.", pybind11::arg( "degrees" ) );
}

template<size_t D>
void defineBasis( pybind11::module& m )
{
    using AbsBasisBinding = pybind11::class_<AbsBasis<D>, std::shared_ptr<AbsBasis<D>>>;

    AbsBasisBinding( m, add<D>( "AbsBasis" ).c_str( ) )
        .def( "nelements", &AbsBasis<D>::nelements )
        .def( "ndof", &AbsBasis<D>::ndof )
        .def( "ndim", []( const AbsBasis<D>& ){ return D; } )
        .def( "nfields", &AbsBasis<D>::nfields );

    using MlhpBasis = MultilevelHpBasis<D>;
    using MlhpBasisBinding = pybind11::class_<MlhpBasis, AbsBasis<D>, std::shared_ptr<MlhpBasis>>;

    auto __str__ = []( const MultilevelHpBasis<D>& basis )
    { 
        std::ostringstream os;

        print( basis, os );

        return os.str( );
    };

    MlhpBasisBinding( m, add<D>( "MultilevelHpBasis" ).c_str( ) )
        .def( "__str__", __str__ )
        .def("memoryUsage", &MlhpBasis::memoryUsage);

    pybind11::implicitly_convertible<size_t, PolynomialDegreeTuple>( );
    pybind11::implicitly_convertible<std::vector<size_t>, PolynomialDegreeTuple>( );

    using FactoryType1 = MultilevelHpBasisSharedPtr<D>( const HierarchicalGridSharedPtr<D>&,
                                                        const PolynomialDegreeTuple&, size_t );
    
    m.def( "makeHpTensorSpace", static_cast<FactoryType1*>( makeHpBasis<TensorSpace> ),
           "Create tensor space multi-level hp basis with uniform polynomial degree distribution.",
           pybind11::arg( "grid" ),  pybind11::arg( "degrees" ), pybind11::arg( "nfields" ) = 1 );

    m.def( "makeHpTrunkSpace", static_cast<FactoryType1*>( makeHpBasis<TrunkSpace> ),
           "Create trunk space multi-level hp basis with uniform polynomial degree distribution.",
           pybind11::arg( "grid" ),  pybind11::arg( "degrees" ), pybind11::arg( "nfields" ) = 1 );

    m.def( "makeHpTensorSpaceFactory", []( std::array<size_t, D> degrees )
           { return makeHpBasisFactory<TensorSpace, D>( degrees ); },
           "Create factory that creates tensor space hp bases with uniform polynomial degree distribution.",
           pybind11::arg( "degrees" ) );

    m.def( "makeHpTrunkSpaceFactory", []( std::array<size_t, D> degrees )
           { return makeHpBasisFactory<TrunkSpace, D>( degrees ); },
           "Create factory that creates trunk space hp bases with uniform polynomial degree distribution.",
           pybind11::arg( "degrees" ) );

    using FactoryType2 = MultilevelHpBasisFactory<D>( const PolynomialDegreeTuple& );

    auto ptr1 = static_cast<FactoryType2*>( makeHpBasisFactory<TensorSpace, D> );
    auto ptr2 = static_cast<FactoryType2*>( makeHpBasisFactory<TrunkSpace, D> );

    m.def( add<D>( "makeHpTensorSpaceFactory" ).c_str( ), ptr1, "Create factory that creates tensor "
           "space hp bases with custom polynomial degree distribution.", pybind11::arg( "degrees" ) );

    m.def( add<D>( "makeHpTrunkSpaceFactory" ).c_str( ), ptr2, "Create factory that creates trunk "
           "space hp bases with custom polynomial degree distribution.", pybind11::arg( "degrees" ) );

    defineBasisFactoryWithGrading<D, UniformGrading>( m );
    defineBasisFactoryWithGrading<D, LinearGrading>( m );
    defineBasisFactoryWithGrading<D, InterpolatedGrading>( m );

    auto count = []( std::array<size_t, D> degrees )
    {
        BooleanMask<D> mask;

        TrunkSpace::initialMaskProvider<D>( )( mask, degrees );

        return std::accumulate( mask.begin( ), mask.end( ), std::uint64_t { 0 } );
    };

    m.def( "countTrunkSpaceDofs", count, "Number element dofs using trunk space.", pybind11::arg( "degrees" ) );

    m.def( "makeAdditiveSchwarzPreconditioner", []( const linalg::UnsymmetricSparseMatrix& matrix,
                                                    const AbsBasis<D>& basis,
                                                    const DofIndexVector& dirichletDofs )
           { return makeAdditiveSchwarzPreconditioner( matrix, basis, dirichletDofs ); },
           pybind11::arg( "matrix" ), pybind11::arg( "basis" ), 
           pybind11::arg( "dirichletDofs" ) = DofIndexVector { } );

    auto printUnstructured = []( const UnstructuredBasis<D>& basis )
    {
        std::ostringstream os;

        print( basis, os );

        return os.str( );
    };

    pybind11::class_<UnstructuredBasis<D>, AbsBasis<D>, std::shared_ptr<UnstructuredBasis<D>>>
        ( m, add<D>( "UnstructuredBasis" ).c_str( ) )
       .def( "__str__", printUnstructured )
       .def( "memoryUsage", &UnstructuredBasis<D>::memoryUsage );

    m.def( "makeUnstructuredBasis", []( const std::shared_ptr<UnstructuredMesh<D>>& mesh,
                                        size_t nfields )
        { return std::make_shared<UnstructuredBasis<D>>( mesh, nfields ); },
        pybind11::arg( "mesh" ), pybind11::arg( "nfields" ) = 1 );
}

template<size_t D>
void definePartitioners( pybind11::module& m )
{
    pybind11::class_<AbsQuadrature<D>>( m, 
        add<D>( "AbsQuadrature" ).c_str( ) );

    pybind11::class_<StandardQuadrature<D>, AbsQuadrature<D>>
        ( m, add<D>( "StandardQuadrature" ).c_str( ) );

    pybind11::class_<SpaceTreeQuadrature<D>, AbsQuadrature<D>>
        ( m, add<D>( "SpaceTreeQuadrature" ).c_str( ) );

    pybind11::class_<MomentFittingQuadrature<D>, AbsQuadrature<D>>
        ( m, add<D>( "MomentFittingQuadrature" ).c_str( ) );

    pybind11::class_<MeshProjectionQuadrature<D>, AbsQuadrature<D>>
        ( m, add<D>( "MeshProjectionQuadrature" ).c_str( ) );

    m.def( add<D>( "makeStandardQuadrature" ).c_str( ), []( ){ return StandardQuadrature<D>{ }; } );

    m.def( "makeSpaceTreeQuadrature", []( const ImplicitFunctionWrapper<D>& function, size_t depth, double epsilon )
           { return SpaceTreeQuadrature<D>{ function, epsilon, depth }; },
           pybind11::arg( "function" ), pybind11::arg( "depth" ), pybind11::arg( "epsilon" ) = 1.0 );
    
    m.def( "makeMomentFittingQuadrature", []( const ImplicitFunctionWrapper<D>& function, 
                                               size_t depth, double epsilon, bool adaptOrders )
           { return MomentFittingQuadrature<D>{ function, epsilon, depth, adaptOrders }; },
           pybind11::arg( "function" ), pybind11::arg( "depth" ), pybind11::arg( "epsilon" ) = 1.0,
           pybind11::arg( "adaptOrders" ) = true );

    m.def( "makeMeshProjectionQuadrature", []( const AbsHierarchicalGrid<D>& grid,
                                               const AbsQuadrature<D>& quadrature )
           { return MeshProjectionQuadrature<D> { grid, quadrature }; },
           pybind11::arg( "grid" ), pybind11::arg( "quadrature" ) = StandardQuadrature<D> { } );
}

template<typename T>
void defineFunctionWrapper( pybind11::module& m, const std::string& name )
{
    pybind11::class_<FunctionWrapper<T>>( m, name.c_str( ) )
        .def( pybind11::init<T>( ) )
        .def( "__call__", &FunctionWrapper<T>::call );
}

constexpr bool notInstantiated( size_t D )
{
    auto dimensions = std::array { MLHP_DIMENSIONS_LIST };

    return std::find( dimensions.begin( ), dimensions.end( ), D ) == dimensions.end( );
}

void defineFunctionWrappersSingle( pybind11::module& m )
{
    defineFunctionWrapper<RealFunction>( m, "RealFunction" );
    defineFunctionWrapper<linalg::LinearOperator>( m, "LinearOperator" );
}

template<size_t D>
void defineFunctionWrappers( pybind11::module& m )
{
    defineFunctionWrapper<spatial::ScalarFunction<D>>( m, add<D>( "ScalarFunction" ) );
    defineFunctionWrapper<spatial::VectorFunction<D>>( m, add<D>( "VectorFunction" ) );
    defineFunctionWrapper<spatial::ParameterFunction<D>>( m, add<D>( "SpatialPath" ) );
    defineFunctionWrapper<QuadratureOrderDeterminor<D>>( m, add<D>( "QuadratureOrderDeterminor" ) );

    if constexpr( notInstantiated( D + 1 ) )
    {
        defineFunctionWrapper<spatial::ScalarFunction<D + 1>>( m, add<D + 1>( "ScalarFunction" ) );
        defineFunctionWrapper<spatial::VectorFunction<D + 1>>( m, add<D + 1>( "VectorFunction" ) );
    }
}

template<size_t D>
void defineIntegrands( pybind11::module& m )
{
    pybind11::class_<DomainIntegrand<D>>( m, add<D>( "DomainIntegrand" ).c_str( ) );
    pybind11::class_<Kinematics<D>>( m, add<D>( "Kinematics" ).c_str( ) );
    pybind11::class_<Constitutive<D>>( m, add<D>( "Constitutive" ).c_str( ) );

    m.def( "makePoissonIntegrand", []( const ScalarFunctionWrapper<D>& kappa,
                                       const ScalarFunctionWrapper<D>& source )
        { return makePoissonIntegrand<D>( kappa, source ); } );

    m.def( "makeL2ErrorIntegrand", []( const DoubleVector& dofs,
                                       const ScalarFunctionWrapper<D>& solution )
        { return makeL2ErrorIntegrand<D>( dofs.get( ), solution ); } );

    m.def( "makeEnergyErrorIntegrand", []( const DoubleVector& dofs,
                                           const VectorFunctionWrapper<D, D>& derivatives )
        { return makeEnergyErrorIntegrand<D>( dofs.get( ), derivatives ); } );

    m.def( add<D>( "makeSmallStrainKinematics" ).c_str( ), makeSmallStrainKinematics<D> );
    m.def( "makeIntegrand", []( const Kinematics<D>& kinematics,
                                const Constitutive<D>& constitutive,
                                const VectorFunctionWrapper<D, D>& rhs )
        { return makeIntegrand<D>( kinematics, constitutive, rhs ); },
        pybind11::arg( "kinematics" ), pybind11::arg( "constitutive" ),
        pybind11::arg( "source") = spatial::constantFunction<D>( array::make<D>( 0.0 ) ) );

    if constexpr( D == 3 )
    {
        m.def( "makeIsotropicElasticMaterial", []( const ScalarFunctionWrapper<3>& E,
                                                   const ScalarFunctionWrapper<3>& nu )
            { return makeIsotropicElasticMaterial( E, nu ); } );
    }
    if constexpr( D == 2 )
    {
        m.def( "makePlaneStressMaterial", []( const ScalarFunctionWrapper<D>& E,
                                              const ScalarFunctionWrapper<D>& nu )
            { return makePlaneStressMaterial( E, nu ); } );

        m.def( "makePlaneStrainMaterial", []( const ScalarFunctionWrapper<D>& E,
                                              const ScalarFunctionWrapper<D>& nu )
            { return makePlaneStrainMaterial( E, nu ); } );
    }

    pybind11::class_<BasisProjectionIntegrand<D>>( m, add<D>( "BasisProjectionIntegrand" ).c_str( ) );

    m.def( "makeTransientPoissonIntegrand", []( const ScalarFunctionWrapper<D + 1>& capacity,
                                                const ScalarFunctionWrapper<D + 1>& diffusivity,
                                                const ScalarFunctionWrapper<D + 1>& source,
                                                const DoubleVector& dofs,
                                                std::array<double, 2> timeStep,
                                                double theta )
           { return makeTransientPoissonIntegrand<D>( capacity, diffusivity, source, dofs.get( ), timeStep, theta ); } ); 

    m.def( add<D>( "makeL2BasisProjectionIntegrand" ).c_str( ), []( const DoubleVector& dofs )
           { return makeL2BasisProjectionIntegrand<D>( dofs.get( ) ); } );
}

void bindLinalg( pybind11::module& m )
{
    pybind11::class_<linalg::AbsSparseMatrix,
        std::shared_ptr<linalg::AbsSparseMatrix>>
        absSparseMatrix( m, "AbsSparseMatrix" );

    absSparseMatrix.def( "memoryUsage", &linalg::AbsSparseMatrix::memoryUsage );

    [[maybe_unused]]
    pybind11::class_<linalg::SymmetricSparseMatrix,
        std::shared_ptr<linalg::SymmetricSparseMatrix>>
        symmetricSparse( m, "SymmetricSparseMatrix", absSparseMatrix );

    [[maybe_unused]]
    pybind11::class_<linalg::UnsymmetricSparseMatrix,
        std::shared_ptr<linalg::UnsymmetricSparseMatrix>>
        unsymmetricSparse( m, "UnsymmetricSparseMatrix", absSparseMatrix );
    
    auto print = []( const auto& matrix )
    { 
        std::stringstream sstream;

        linalg::print( matrix, sstream );

        return sstream.str( );
    };

    symmetricSparse.def( "__str__", [=]( const linalg::SymmetricSparseMatrix& matrix ) { return print( matrix ); } );
    unsymmetricSparse.def( "__str__", [=]( const linalg::UnsymmetricSparseMatrix & matrix ){ return print( matrix ); } );

    [[maybe_unused]]
    pybind11::class_<DoubleVector> doubleVector( m, "DoubleVector" );

    doubleVector.def( pybind11::init<std::size_t>( ) );
    doubleVector.def( pybind11::init<std::size_t, double>( ) );
    doubleVector.def( pybind11::init<std::vector<double>>( ) );
    doubleVector.def( "__len__", []( const DoubleVector& self ){ return self.get( ).size( ); } );
    doubleVector.def( "get", static_cast<const std::vector<double>& (DoubleVector::*)( ) const>( &DoubleVector::get ) );
      
    [[maybe_unused]]
    pybind11::class_<ScalarDouble> scalarDouble( m, "ScalarDouble" );
    
    scalarDouble.def( pybind11::init<>( ) );
    scalarDouble.def( pybind11::init<double>( ) );
    scalarDouble.def( "get", []( const ScalarDouble& value ) { return value.get( ); } );
    
    m.def( "makeCGSolver", []( double tolerance )
    { 
        auto solver = linalg::makeCGSolver( tolerance );

        return std::function { [=]( const linalg::AbsSparseMatrix& matrix,
                                    DoubleVector& rhs )
        {
            return DoubleVector { solver( matrix, rhs.get( ) ) };
        } };
    }, pybind11::arg( "tolerance" ) = 1e-8 );
    
    m.def( "makeMultiply", []( const linalg::AbsSparseMatrix& matrix )
           { return LinearOperatorWrapper { linalg::makeDefaultMultiply( matrix ) }; },
           "Create default linear operator for sparse matrix-vector product.",
           pybind11::arg( "matrix" ) );

    auto internalCGF = []( const LinearOperatorWrapper& multiply,
                           const DoubleVector& b,
                           const LinearOperatorWrapper& preconditioner,
                           size_t maxit, double tolerance )
    {
        std::vector<double> solution;

        auto residuals = linalg::cg( multiply, b.get( ), solution, preconditioner, maxit, tolerance );

        return std::make_pair( DoubleVector { std::move( solution ) }, residuals );
    };
    
    auto internalBiCGStabF = []( const LinearOperatorWrapper& multiply,
                                 const DoubleVector& b,
                                 const LinearOperatorWrapper& preconditioner,
                                 size_t maxit, double tolerance )
    {
        std::vector<double> solution;

        auto residuals = linalg::bicgstab( multiply, b.get( ), solution, preconditioner, maxit, tolerance );

        return std::make_pair( DoubleVector { std::move( solution ) }, residuals );
    };

    m.def( "internalCG", internalCGF );
    m.def( "internalBiCGStab", internalBiCGStabF );

    m.def( "makeNoPreconditioner", []( size_t size ){ return 
           LinearOperatorWrapper { linalg::makeNoPreconditioner( size ) }; },
           pybind11::arg( "size" ) );

    m.def( "makeDiagonalPreconditioner", []( const linalg::AbsSparseMatrix& matrix )
           { return LinearOperatorWrapper { linalg::makeDiagonalPreconditioner( matrix ) }; },
           pybind11::arg( "matrix" ) );

    m.def( "fill", []( linalg::AbsSparseMatrix& matrix, double value )
           { std::fill( matrix.data( ), matrix.data( ) + matrix.nnz( ), value ); },
           pybind11::arg( "matrix" ), pybind11::arg( "value" ) = 0.0 );

    m.def( "fill", []( DoubleVector& vector, double value )
           { std::fill( vector.get( ).begin( ), vector.get( ).end( ), value ); },
           pybind11::arg( "matrix" ), pybind11::arg( "value" ) = 0.0 );
    
    m.def( "copy", []( const DoubleVector& vector ) -> DoubleVector
           { return vector.get( ); }, pybind11::arg( "vector" ) );

    m.def( "norm", []( const DoubleVector& vector )
           { return std::sqrt( std::inner_product( vector.get( ).begin( ), 
                vector.get( ).end( ), vector.get( ).begin( ), 0.0 ) );; },
           pybind11::arg( "vector" ) );

    m.def( "add", []( const DoubleVector& vector1, 
                      const DoubleVector& vector2, 
                      double factor ) -> DoubleVector
           { 
               MLHP_CHECK( vector1.get( ).size( ) == vector2.get( ).size( ),
                           "Inconsistent vector sizes in addition." );

               auto result = std::vector<double>( vector1.get( ).size( ) );

               std::transform( vector1.get( ).begin( ), vector1.get( ).end( ), 
                    vector2.get( ).begin( ), result.begin( ), 
                    [=]( double v1, double v2 ) { return v1 + factor * v2; } );

               return result;
           },
           pybind11::arg( "vector1" ), pybind11::arg( "vector2" ),
           pybind11::arg( "factor" ) = 1.0 );
}

template<size_t D>
void defineBoundaryCondition( pybind11::module& m )
{
    auto convertFunctions = []( const std::vector<ScalarFunctionWrapper<D>>& functions )
    { 
        std::vector<spatial::ScalarFunction<D>> convertedFunctions;

        for( const auto& function : functions )
        {
            convertedFunctions.push_back( function );
        }

        return convertedFunctions;
    };

    IntegrationOrderDeterminorWrapper<D> defaultDeterminor { makeIntegrationOrderDeterminor<D>( 1 ) };
    
    m.def( "integrateDirichletDofs", [=]( const std::vector<ScalarFunctionWrapper<D>>& functions,
                                          const AbsBasis<D>& basis, std::vector<size_t> faces,
                                          const IntegrationOrderDeterminorWrapper<D>& orderDeterminor )
        { return boundary::boundaryDofs<D>( convertFunctions( functions ), basis, faces, orderDeterminor ); }, 
        pybind11::arg( "boundaryFunctions" ), pybind11::arg( "basis" ), pybind11::arg( "faces" ), 
        pybind11::arg( "orderDeterminor" ) = defaultDeterminor );

    m.def( "integrateDirichletDofs", [=]( const ScalarFunctionWrapper<D>& function,
                                          const AbsBasis<D>& basis, std::vector<size_t> faces,
                                          const IntegrationOrderDeterminorWrapper<D>& orderDeterminor,
                                          size_t fieldComponent )
        { return boundary::boundaryDofs<D>( function, basis, faces, orderDeterminor, fieldComponent ); }, 
        pybind11::arg( "boundaryFunctions" ), pybind11::arg( "basis" ), pybind11::arg( "faces" ),
        pybind11::arg( "orderDeterminor" ) = defaultDeterminor, pybind11::arg( "fieldComponent" ) = 0 );
}

void definePostprocessingSingle( pybind11::module& m )
{
    pybind11::enum_<PostprocessTopologies>( m, "PostprocessTopologies" )
        .value( "Nothing", PostprocessTopologies::None )
        .value( "Corners", PostprocessTopologies::Corners )
        .value( "Edges", PostprocessTopologies::Edges )
        .value( "Faces", PostprocessTopologies::Faces )
        .value( "Volumes", PostprocessTopologies::Volumes )
        .def( "__or__", []( PostprocessTopologies a,
                            PostprocessTopologies b )
                            { return a | b; } );

    pybind11::class_<OutputMeshPartition, std::shared_ptr<OutputMeshPartition>>( m, "OutputMeshPartition" )
        .def( pybind11::init<>( ) )
        .def( "index", []( const OutputMeshPartition& o ){ return o.index; } )
        .def( "points", []( const OutputMeshPartition& o ){ return o.points; } )
        .def( "connectivity", []( const OutputMeshPartition& o ){ return o.connectivity; } )
        .def( "offsets", []( const OutputMeshPartition& o ){ return o.offsets; } )
        .def( "types", []( const OutputMeshPartition& o ){ return o.types; } );

    pybind11::class_<VtuOutput>( m, "VtuOutput" )
        .def( pybind11::init( []( std::string filename, std::string writemode )
            { return VtuOutput { .filename = filename, .mode = writemode }; } ), 
            pybind11::arg( "filename" ) = "output.vtu",
            pybind11::arg( "writemode" ) = "RawBinaryCompressed" );

    pybind11::class_<PVtuOutput>( m, "PVtuOutput" )
        .def( pybind11::init( []( std::string filename, std::string writemode, size_t maxpartitions )
            { return PVtuOutput { .filename = filename, .mode = writemode, .maxpartitions = maxpartitions }; } ),
            pybind11::arg( "filename" ) = "output.vtu",
            pybind11::arg( "writemode" ) = "RawBinaryCompressed",
            pybind11::arg( "maxpartitions" ) = 2 * parallel::getMaxNumberOfThreads( ) );
    
    pybind11::class_<DataAccumulator, std::shared_ptr<DataAccumulator>>( m, "DataAccumulator" )
        .def( pybind11::init<>( ) )
        .def( "mesh", []( const DataAccumulator& d ){ return *d.mesh; } )
        .def( "data", []( const DataAccumulator& d ){ return *d.data; } );
}

template<size_t D>
void definePostprocessingDimensions( pybind11::module& m )
{
    pybind11::class_<ElementProcessor<D>, std::shared_ptr<ElementProcessor<D>>>
        ( m, add<D>( "ElementProcessor" ).c_str( ) );

    pybind11::class_<CellProcessor<D>, std::shared_ptr<CellProcessor<D>>>
        ( m, add<D>( "CellProcessor" ).c_str( ) );

    m.def( add<D>( "makeSolutionProcessor" ).c_str( ), []( const DoubleVector& dofs,
                                                           const std::string& name )
        { 
            return std::make_shared<ElementProcessor<D>>( 
                makeSolutionProcessor<D>( dofs.get( ), name ) );
        }, 
        pybind11::arg( "dofs" ), 
        pybind11::arg( "solutionName" ) = "Solution" );

    m.def( "makeFunctionProcessor", []( const ScalarFunctionWrapper<D>& function,
                                        const std::string& name )
           { return std::make_shared<CellProcessor<D>>(
                   makeFunctionProcessor<D>( function.get( ), name ) ); },
           pybind11::arg( "function" ), pybind11::arg( "name" ) );

    m.def( "makeFunctionProcessor", []( const ImplicitFunctionWrapper<D>& function,
                                        const std::string& name )
           { return std::make_shared<CellProcessor<D>>(
                   makeFunctionProcessor<D>( function.get( ), name ) ); },
           pybind11::arg( "function" ), pybind11::arg( "name" ) = "Domain" );

    m.def( "makeVonMisesProcessor", []( const DoubleVector& dofs,
                                        const Kinematics<D>& kinematics,
                                        const Constitutive<D>& constitutive,
                                        const std::string& name )
        { 
            return std::make_shared<ElementProcessor<D>>( 
                makeVonMisesProcessor<D>( dofs.get( ), kinematics, constitutive, name ) );
        }, 
        pybind11::arg( "dofs" ), pybind11::arg( "kinematics" ), pybind11::arg( "contitutive" ),
        pybind11::arg( "name" ) = "VonMisesStress" );

    if constexpr( D <= 3 )
    {
        defineFunctionWrapper<PostprocessingMeshCreator<D>>( m, add<D>( "PostprocessingMeshCreator" ).c_str( ) );

        auto define1 = [&]<typename WriterType>( )
        {
            auto defaultMesh = wrapFunction( createGridOnCells<D>( array::makeSizes<D>( 1 ) ) );

            m.def( "internalWriteBasisOutput", []( const AbsBasis<D>& basis,
                                                   const PostprocessingMeshCreatorWrapper<D>& postmesh,
                                                   WriterType& writer,
                                                   std::vector<ElementProcessor<D>>&& processors )
            {
                writeOutput( basis, postmesh.get( ), mergeProcessors( std::move( processors ) ), writer );
            },
            pybind11::arg( "basis" ), pybind11::arg( "postmesh" ) = defaultMesh,
            pybind11::arg( "writer" ), pybind11::arg( "processors" ) = std::vector<ElementProcessor<D>>{ } );

            m.def( "internalWriteMeshOutput", []( const AbsMesh<D>& mesh,
                                                  const PostprocessingMeshCreatorWrapper<D>& postmesh,
                                                  WriterType& writer,
                                                  std::vector<CellProcessor<D>>&& processors )
            {
                writeOutput( mesh, postmesh.get( ), mergeProcessors( std::move( processors ) ), writer );
            },
            pybind11::arg( "mesh" ), pybind11::arg( "postmesh" ) = defaultMesh,
            pybind11::arg( "writer" ), pybind11::arg( "processors" ) = std::vector<CellProcessor<D>>{ } );
        };
        
        define1.template operator()<DataAccumulator>( );
        define1.template operator()<VtuOutput>( );
        define1.template operator()<PVtuOutput>( );

        m.def( "convertToElementProcessor", []( CellProcessor<D> processor ) { return
            convertToElementProcessor<D>( std::move( processor ) ); }, pybind11::arg( "elementProcessor" ) );

        auto createGridOnCellsF = []( std::array<size_t, D> resolution,
                                      PostprocessTopologies topologies )
        {
            return PostprocessingMeshCreatorWrapper<D> { createGridOnCells( resolution, topologies ) };
        };

        m.def( "createGridOnCells", createGridOnCellsF, pybind11::arg( "resolution" ), 
               pybind11::arg( "topologies" ) = defaultOutputTopologies[D] );
    }
}

void defineDimensionIndendent( pybind11::module& m )
{    
    pybind11::enum_<CellType>( m, "CellType" )
        .value( "NCube", CellType::NCube )
        .value( "Simplex", CellType::Simplex );
    
    m.def( "inflateDofs", []( const DoubleVector& interiorDofs,
                              const DofIndicesValuesPair& dirichletDofs ) -> DoubleVector
        { return DoubleVector { boundary::inflate( interiorDofs.get( ), dirichletDofs ) }; }, 
        pybind11::arg( "interiorDofs" ), 
        pybind11::arg( "dirichletDofs" ) );

    m.def( "combineDirichletDofs", &boundary::combine, pybind11::arg( "boundaryDofs" ) );

    
    auto instantiateMarchingCubes = [&]<typename Resolution>( )
    {
        auto createMarchingCubesBoundaryF = []( const ImplicitFunctionWrapper<3>& function,
                                                Resolution resolution,
                                                bool recoverMeshBoundaries )
        {
            return PostprocessingMeshCreatorWrapper<3> { createMarchingCubesBoundary( 
                function, resolution, recoverMeshBoundaries ) };
        };
        
        auto createMarchingCubesVolumeF = []( const ImplicitFunction<3>& function,
                                              Resolution resolution )
        {
            return PostprocessingMeshCreatorWrapper<3> { 
                createMarchingCubesVolume( function, resolution ) };
        };

        m.def( "createMarchingCubesBoundary", createMarchingCubesBoundaryF, pybind11::arg( "function" ),
                pybind11::arg( "resolution" ), pybind11::arg( "recoverMeshBoundaries" ) = true );
        m.def( "createMarchingCubesVolume", createMarchingCubesVolumeF, 
                pybind11::arg( "function" ), pybind11::arg( "resolution" ) );
    };

    instantiateMarchingCubes.operator()<std::array<size_t, 3>>( );
    instantiateMarchingCubes.operator()<const ResolutionDeterminor<3>&>( );

    defineFunctionWrappersSingle( m );
    defineBasisSingle( m );
    definePostprocessingSingle( m );
}

template<size_t D>
void defineDimension( pybind11::module& m )
{
    //defineDimensionTag<D>( m );
    defineFunctionWrappers<D>( m );
    defineSpatialFunctions<D>( m );
    defineGrid<D>( m );
    defineMesh<D>( m );
    defineBasis<D>( m );
    definePartitioners<D>( m );
    defineIntegrands<D>( m );
    defineBoundaryCondition<D>( m );
    definePostprocessingDimensions<D>( m );
}

template<size_t... D>
void defineDimensions( pybind11::module& m )
{
    [[maybe_unused]] std::initializer_list<int> tmp { ( defineDimension<D>( m ), 0 )... };
}


void bindDiscretization( pybind11::module& m )
{
    bindLinalg( m );

    defineDimensionIndendent( m );
    defineDimensions<MLHP_DIMENSIONS_LIST>( m );
}

} // mlhp::bindings

