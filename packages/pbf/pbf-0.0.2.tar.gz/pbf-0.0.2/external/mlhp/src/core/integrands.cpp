// This file is part of the mlhp project. License: See LICENSE

#include "mlhp/core/integrands.hpp"
#include "mlhp/core/basisevaluation.hpp"
#include "mlhp/core/dense.hpp"
#include "mlhp/core/spatial.hpp"

#include <array>

namespace mlhp
{

template<size_t D>
DomainIntegrand<D> makeL2ProjectionIntegrand( const spatial::ScalarFunction<D>& weight,
                                              const spatial::ScalarFunction<D>& source )
{

    // For multiple fields copy from the two basis implementation
    auto evaluate = [=]( const BasisFunctionEvaluation<D>& shapes,
                         AlignedDoubleVectors& targets,
                         double weightDetJ )
    {
        double factor1 = weight( shapes.xyz( ) ) * weightDetJ;
        double factor2 = source( shapes.xyz( ) ) * weightDetJ;

        auto tmp = shapes.sizes( );
        auto ndof = std::get<0>( tmp );
        auto nblocks = std::get<1>( tmp );

        auto N = shapes.noalias( 0, 0 );

        linalg::symmetricElementLhs( targets[0].data( ), ndof, nblocks, [=]( size_t i, size_t j )
        { 
            return N[i] * N[j] * factor1;
        } );

        linalg::elementRhs( targets[1].data( ), ndof, nblocks, [&]( size_t i )
        { 
            return N[i] * factor2;
        } );
    };

    auto types = std::vector { AssemblyType::SymmetricMatrix, AssemblyType::Vector };

    return DomainIntegrand<D>( types, DiffOrders::Shapes, evaluate );
}

template<size_t D>
DomainIntegrand<D> makeL2ProjectionIntegrand( const spatial::ScalarFunction<D>& source )
{
    auto weight = spatial::constantFunction<D>( 1.0 );

    return makeL2ProjectionIntegrand<D>( weight, source );
}

template<size_t D>
DomainIntegrand<D> makePoissonIntegrand( const spatial::ScalarFunction<D>& conductivity,
                                         const spatial::ScalarFunction<D>& source )
{
    auto evaluate = [=]( const BasisFunctionEvaluation<D>& shapes,
                         AlignedDoubleVectors& targets,
                         double weightDetJ )
    {
        double factor1 = conductivity( shapes.xyz( ) ) * weightDetJ;
        double factor2 = source( shapes.xyz( ) ) * weightDetJ;

        auto tmp = shapes.sizes( );
        auto ndof = std::get<0>( tmp );
        auto nblocks = std::get<1>( tmp );
        auto ndofpadded = std::get<2>( tmp );

        auto N = shapes.noalias( 0, 0 );
        auto dN = shapes.noalias( 0, 1 );

        linalg::symmetricElementLhs( targets[0].data( ), ndof, nblocks, [=]( size_t i, size_t j )
        { 
            double value = 0.0;

            for( size_t axis = 0; axis < D; ++axis )
            {
                value += dN[axis * ndofpadded + i] * dN[axis * ndofpadded + j] * factor1;
            }

            return value;
        } );

        linalg::elementRhs( targets[1].data( ), ndof, nblocks, [&]( size_t i )
        { 
            return N[i] * factor2;
        } );
    };

    auto types = std::vector { AssemblyType::SymmetricMatrix, AssemblyType::Vector };

    return DomainIntegrand<D>( types, DiffOrders::FirstDerivatives, evaluate );
}

template<size_t D>
DomainIntegrand<D> makeAdvectionDiffusionIntegrand( const spatial::VectorFunction<D>& velocity,
                                                    const spatial::ScalarFunction<D>& diffusivity,
                                                    const spatial::ScalarFunction<D>& source )
{
    auto evaluate = [=]( const BasisFunctionEvaluation<D>& shapes,
                         AlignedDoubleVectors& targets, double weight )
    {
        auto ndof = shapes.ndof( );
        auto nblocks = shapes.nblocks( );
        auto ndofpadded = shapes.ndofpadded( );
        
        auto N = shapes.noalias( 0, 0 );
        auto dN = shapes.noalias( 0, 1 );

        auto a = velocity( shapes.xyz( ) );
        auto k = diffusivity( shapes.xyz( ) );
        auto f = source( shapes.xyz( ) );
        
        linalg::unsymmetricElementLhs( targets[0].data( ), ndof, nblocks, 
                                       [&]( size_t i, size_t j )
        {
            double value = 0.0;
            
            for( size_t axis = 0; axis < D; ++axis )
            {
                value += N[i] * a[axis] * dN[axis * ndofpadded + j];

            } // axis
                    
            for( size_t axis = 0; axis < D; ++axis )
            {
                value += dN[axis * ndofpadded + i] * k * dN[axis * ndofpadded + j];
        
            } // component
        
            return value * weight;
        } );
        
        linalg::elementRhs( targets[1].data( ), ndof, nblocks, [&]( size_t i )
        {
            return N[i] * f * weight;
        } );
    };

    auto types = std::vector { AssemblyType::UnsymmetricMatrix, AssemblyType::Vector };

    return DomainIntegrand<D>( types, DiffOrders::FirstDerivatives, evaluate );
}


template<size_t D>
DomainIntegrand<D> makeL2ErrorIntegrand( const std::vector<double>& solutionDofs,
                                         const spatial::ScalarFunction<D>& solutionFunction )
{
    auto evaluate = [=, &solutionDofs]( const BasisFunctionEvaluation<D>& shapes,
                                        const LocationMap& locationMap,
                                        AlignedDoubleVectors& targets,
                                        AlignedDoubleVector&,
                                        double weightDetJ )
    {
        double analytical = solutionFunction( shapes.xyz( ) );
        double numerical = evaluateSolution( shapes, locationMap, solutionDofs );

        targets[0][0] += numerical * numerical * weightDetJ;
        targets[1][0] += analytical * analytical * weightDetJ;
        targets[2][0] += utilities::integerPow( numerical - analytical, 2 ) * weightDetJ;
    };

    return DomainIntegrand<D>( DiffOrders::Shapes, std::vector( 3, AssemblyType::Scalar ), evaluate );
}


template<size_t D>
DomainIntegrand<D> makeEnergyErrorIntegrand( const std::vector<double>& solutionDofs,
                                             const spatial::VectorFunction<D, D>& analyticalDerivatives )
{
    auto evaluate = [=, &solutionDofs]( const BasisFunctionEvaluation<D>& shapes,
                                        const LocationMap& locationMap,
                                        AlignedDoubleVectors& targets,
                                        AlignedDoubleVector&, 
                                        double weightDetJ )
    {
        auto du = evaluateGradient( shapes, locationMap, solutionDofs );
        auto analytical = analyticalDerivatives( shapes.xyz( ) );

        for( size_t axis = 0; axis < D; ++axis )
        {
            targets[0][0] += 0.5 * weightDetJ * utilities::integerPow( du[axis], 2 );
            targets[1][0] += 0.5 * weightDetJ * utilities::integerPow( analytical[axis], 2 );
            targets[2][0] += 0.5 * weightDetJ * utilities::integerPow( du[axis] - analytical[axis], 2 );
        }
    };

    return DomainIntegrand<D>( DiffOrders::FirstDerivatives, 
        std::vector( 3, AssemblyType::Scalar ), evaluate );
}

template<size_t D> MLHP_EXPORT
DomainIntegrand<D> makeInternalEnergyIntegrand( const std::vector<double>& solutionDofs,
                                                const Kinematics<D>& kinematics,
                                                const Constitutive<D>& constitutive,
                                                size_t ncomponents )
{
    auto evaluate = [=, &solutionDofs]( const BasisFunctionEvaluation<D>& shapes,
                                        const LocationMap& locationMap,
                                        AlignedDoubleVectors& targets,
                                        AlignedDoubleVector& tmp, 
                                        double weightDetJ )
    {
        tmp.resize( D * D + 2 * ncomponents );

        std::fill( tmp.begin( ), tmp.end( ), 0.0 );

        auto gradient = std::span( tmp.data( ), D * D );
        auto strain = std::span( gradient.data( ) + gradient.size( ), ncomponents );
        auto stress = std::span( strain.data( ) + strain.size( ), ncomponents);

        evaluateSolutions( shapes, locationMap, solutionDofs, gradient, 1 );

        kinematics.evaluate( shapes, gradient, strain, std::span<double> { } );
        constitutive.evaluate( shapes, strain, stress, 1 );
        
        targets[0][0] += 0.5 * spatial::dot( strain, stress ) * weightDetJ;
    };

    auto diffOrder = DiffOrders::FirstDerivatives;
    auto types = std::vector { AssemblyType::Scalar };

    return DomainIntegrand<D>( diffOrder, types, evaluate );
}

template<size_t D>
Kinematics<D> makeSmallStrainKinematics( )
{
    auto evaluate = []( const BasisFunctionEvaluation<D>& shapes, 
                        std::span<const double> du,
                        std::span<double> strainEvaluation,
                        std::span<double> strainOperator )
    { 
        static constexpr size_t ncomponents = ( D * ( D + 1 ) ) / 2;

        // Prepare 
        auto B = memory::assumeAlignedNoalias( strainOperator.data( ) );
        auto offsets = fieldOffsets<D, D>( shapes );
        auto ndofpadded = shapes.ndofpadded( );

        MLHP_CHECK( D <= 3, "Small strain kinematics only implemented up to D = 3." );

        MLHP_CHECK( strainOperator.empty( ) || strainOperator.size( ) == ncomponents * ndofpadded,
                    "Invalid strain operator size in small strain kinematrics" );
        
        MLHP_CHECK( strainEvaluation.empty( ) || strainEvaluation.size( ) == ncomponents,
                    "Invalid strain evaluation size in infinitesimal strain kinematrics" );
        
        // Now copy derivative components into the right spot
        auto evaluateComponent = [&]( size_t index, size_t iN, size_t iD )
        {
            if( !strainOperator.empty( ) )
            {
                auto dN = shapes.get( iN, 1 ) + iD * shapes.ndofpadded( iN );
                auto offset = index * ndofpadded + offsets[iN];

                std::copy_n( dN, shapes.ndof( iN ), B + offset );
            }

            if( !strainEvaluation.empty( ) )
            {
                strainEvaluation[index] += du[iN * D + iD];
            }
        };

        // ND normal strain
        for( size_t i = 0; i < D; ++i )
        {
            // e_ii
            evaluateComponent( i, i, i ); // N_i,dxi
        }

        // 2D engineering shear strain
        if constexpr( D == 2 )
        {
            // g_01 = 2 * e_01
            evaluateComponent( D, 0, 1 ); // N_0,y +       
            evaluateComponent( D, 1, 0 ); //       + N_1,x 
        }

        // 3D engineering shear strain
        if constexpr( D == 3 )                    
        {
            // g_12 = 2 * e_12
            evaluateComponent( D, 1, 2 ); // N_1,z +       
            evaluateComponent( D, 2, 1 ); //       + N_2,y 

            // g_02 = 2 * e_02
            evaluateComponent( 4, 0, 2 ); //         N_0,z +
            evaluateComponent( 4, 2, 0 ); //               + N_2,x

            // g_01 = 2 * e_01
            evaluateComponent( 5, 0, 1 ); // N_0,y +         
            evaluateComponent( 5, 1, 0 ); //               + N_1,x
        }   
    };

    return
    {
        .evaluate = evaluate
    };
}

namespace
{

template<size_t D, size_t N>
auto makeConstitutive( auto&& material )
{
    return Constitutive<D>
    { 
        .evaluate = [=]( const BasisFunctionEvaluation<D>& shapes,
                         std::span<const double> B,
                         std::span<double> target,
                         size_t size1 )
        { 
            auto C = std::array<double, N * N> { };

            material( shapes.xyz( ), C );

            linalg::mmproduct( C.data( ), B.data( ), target.data( ), N, N, size1 );
        }
    };
}

}

Constitutive<3> makeIsotropicElasticMaterial( const spatial::ScalarFunction<3>& youngsModulus,
                                              const spatial::ScalarFunction<3>& poissonRatio )
{
    auto material = [=]( std::array<double, 3> xyz, std::span<double> target )
    {
        MLHP_CHECK( target.size( ) == 6 * 6, "Invalid matrix size in isotropic elastic material." );

        // Compute Lame parameters
        auto nu = poissonRatio( xyz );
        auto tmp1 = ( 1.0 - 2.0 * nu );
        auto tmp2 = youngsModulus( xyz ) / ( ( 1.0 + nu ) * tmp1 );

        auto lambda = nu * tmp2;
        auto mu = 0.5 * tmp1 * tmp2;

        auto diagonal = lambda + 2.0 * mu;
        auto C = linalg::adapter( target, 6 );

        // Upper left block
        C( 0, 0 ) = diagonal; C( 0, 1 ) = lambda;   C( 0, 2 ) = lambda;
        C( 1, 0 ) = lambda;   C( 1, 1 ) = diagonal; C( 1, 2 ) = lambda;
        C( 2, 0 ) = lambda;   C( 2, 1 ) = lambda;   C( 2, 2 ) = diagonal;
        
        // Lower right diagonal: engineering strain -> mu instead of 2 * mu
        C( 3, 3 ) = mu; C( 4, 4 ) = mu; C( 5, 5 ) = mu;
    };
    
    return makeConstitutive<3, 6>( std::move( material ) );
}

Constitutive<2> makePlaneStressMaterial( const spatial::ScalarFunction<2>& youngsModulus,
                                         const spatial::ScalarFunction<2>& poissonRatio )
{
    auto material = [=]( std::array<double, 2> xyz, std::span<double> target )
    {
        auto nu = poissonRatio( xyz );
        auto E = youngsModulus( xyz );
        auto tmp = E / ( 1.0 - nu * nu );
        auto C = linalg::adapter( target, 3 );

        C( 0, 0 ) = tmp;
        C( 1, 1 ) = tmp;
        C( 2, 2 ) = 0.5 * tmp * ( 1.0 - nu );
        C( 0, 1 ) = tmp * nu;
        C( 1, 0 ) = tmp * nu;
    };

    return makeConstitutive<2, 3>( std::move( material ) );
}

Constitutive<2> makePlaneStrainMaterial( const spatial::ScalarFunction<2>& youngsModulus,
                                         const spatial::ScalarFunction<2>& poissonRatio )
{
    auto material = [=]( std::array<double, 2> xyz, std::span<double> target )
    {
        auto nu = poissonRatio( xyz );
        auto E = youngsModulus( xyz );
        auto tmp = E / ( ( 1.0 + nu ) * ( 1.0 - 2.0 * nu ) );
        auto C = linalg::adapter( target, 3 );

        C( 0, 0 ) = tmp * ( 1.0 - nu );
        C( 1, 1 ) = tmp * ( 1.0 - nu );
        C( 2, 2 ) = 0.5 * tmp * ( 1.0 - 2.0 * nu );
        C( 0, 1 ) = tmp * nu;
        C( 1, 0 ) = tmp * nu;

    };

    return makeConstitutive<2, 3>( std::move( material ) );
}

template<size_t D>
DomainIntegrand<D> makeIntegrand( const Kinematics<D>& kinematics,
                                  const Constitutive<D>& constitutive,
                                  const spatial::VectorFunction<D, D>& force )
{
    auto evaluate = [=]( const BasisFunctionEvaluation<D>& shapes,
                         const LocationMap&,
                         AlignedDoubleVectors& targets,
                         AlignedDoubleVector& tmp,
                         double weightDetJ )
    {
        MLHP_CHECK( shapes.nfields( ) == D, "Invalid number of fields in elasticity integrand." );

        auto ndofpadded = shapes.ndofpadded( );
        constexpr auto ncomponents = ( D * ( D + 1 ) ) / 2;

        // Two matrices with (6, padded(N)) for stresses and strains
        tmp.resize( 2 * ncomponents * ndofpadded + D * D );        

        std::fill( tmp.begin( ), tmp.end( ), 0.0 );

        auto B = memory::assumeAlignedNoalias( tmp.data( ) );
        auto S = memory::assumeAlignedNoalias( B + ncomponents * ndofpadded );

        auto strainOperator = std::span( B, ncomponents * ndofpadded );
        auto stressOperator = std::span( S, ncomponents * ndofpadded );
        auto deformationGradient = std::span( S + ncomponents * ndofpadded, D * D );
        auto strain = std::span<double> { };

        // Compute B matrix from shape function evaluation
        kinematics.evaluate( shapes, deformationGradient, strain, strainOperator );

        // Compute S = B * C
        constitutive.evaluate( shapes, strainOperator, stressOperator, ndofpadded );

        // Compute B^T * S
        linalg::symmetricElementLhs( targets[0].data( ), shapes.ndof( ), shapes.nblocks( ), 
                                     [=]( size_t i, size_t j )
        {
            double value = 0.0;

            for( size_t axis = 0; axis < ( D * ( D + 1 ) ) / 2; ++axis )
            {
                value += B[axis * ndofpadded + i] * S[axis * ndofpadded + j];

            } // component

            return value * weightDetJ;
        } );

        auto rhs = targets[1].data( );
        auto forceValues = force( shapes.xyz( ) ) * weightDetJ;

        // Compute right hand side for each field
        for( size_t ifield = 0; ifield < D; ++ifield )
        {
            auto N = shapes.noalias( ifield, 0 );
            auto size = shapes.ndof( ifield );

            linalg::elementRhs( rhs, size, shapes.nblocks( ifield ), [=]( size_t i )
            { 
                return N[i] * forceValues[ifield];
            } );

            rhs += size;
        }
    };

    auto types = std::vector { AssemblyType::SymmetricMatrix, AssemblyType::Vector };

    return DomainIntegrand<D>( DiffOrders::FirstDerivatives, types, evaluate );
}

namespace
{

template<size_t D>
auto internalMakeNeumannIntegrand( auto&& function )
{
    auto evaluate = [function = std::forward<decltype( function )>( function )]
                    ( const BasisFunctionEvaluation<D>& shapes,
                      const LocationMap& /* locationMap */,
                      std::array<double, D> /* normal */,
                      AlignedDoubleVectors& targets,
                      double weightDetJ )
    { 
        auto value = function( shapes.xyz( ) ) * weightDetJ;
        auto target = memory::assumeAlignedNoalias( targets[0].data( ) );

        static constexpr auto nfields = value.size( );

        MLHP_CHECK( shapes.nfields( ) == nfields, "Invalid number of fields." );
        MLHP_CHECK( shapes.ndofpadded( ) == targets[0].size( ), "Invalid target size." );

        for( size_t ifield = 0; ifield < nfields; ++ifield )
        {
            auto N = shapes.noalias( ifield, 0 );
            auto ndof = shapes.ndof( ifield );
            auto nblocks = shapes.nblocks( ifield );

            linalg::elementRhs( target, ndof, nblocks, [&]( size_t iDof )
            { 
                return N[iDof] * value[ifield];
            } );

            target += ndof;
        }
    };

    return SurfaceIntegrand<D>( { AssemblyType::Vector }, DiffOrders::Shapes, evaluate );
}

} // namespace

template<size_t D> MLHP_EXPORT
SurfaceIntegrand<D> makeNeumannIntegrand( const spatial::ScalarFunction<D>& function )
{
    auto vectorize = [=]( auto xyz ) { return std::array { function( xyz ) }; };

    return internalMakeNeumannIntegrand<D>( std::move( vectorize ) );
}

template<size_t D> MLHP_EXPORT
SurfaceIntegrand<D> makeNeumannIntegrand( const spatial::VectorFunction<D, D>& function )
{
    return internalMakeNeumannIntegrand<D>( function );
}


template<size_t D>
SurfaceIntegrand<D> makeRobinIntegrand( const spatial::ScalarFunction<D>& neumann,
                                        const spatial::ScalarFunction<D>& dirichlet )
{
    auto evaluate = [=]( const BasisFunctionEvaluation<D>& shapes,
                         const LocationMap& /* locationMap */,
                         std::array<double, D> /* normal */,
                         AlignedDoubleVectors& targets,
                         double weightDetJ )
    {
        auto dirichletValue = dirichlet( shapes.xyz( ) ) * weightDetJ;
        auto neumannValue = neumann( shapes.xyz( ) ) * weightDetJ;

        auto N = shapes.noalias( 0, 0 );
        auto ndof = shapes.ndof( );
        auto nblocks = shapes.nblocks( );

        linalg::symmetricElementLhs( targets[0].data( ), ndof, nblocks, 
                                     [&]( size_t idof, size_t jdof )
        { 
            return N[idof] * N[jdof] * dirichletValue;
        } );

        linalg::elementRhs( targets[0].data( ), ndof, nblocks, [&]( size_t idof )
        { 
            return N[idof] * neumannValue;
        } );
    };

    auto types = std::vector { AssemblyType::SymmetricMatrix, AssemblyType::Vector };

    return SurfaceIntegrand<D>( types, DiffOrders::Shapes, evaluate );
}

template<size_t D>
BasisProjectionIntegrand<D> makeL2BasisProjectionIntegrand( const std::vector<double>& oldDofs )
{
    auto evaluate = [&oldDofs]( const LocationMap& locationMap0,
                                const LocationMap&,
                                const BasisFunctionEvaluation<D>& shapes0,
                                const BasisFunctionEvaluation<D>& shapes1,
                                AlignedDoubleVectors& targets,
                                double weightDetJ )
    { 
        auto nfields = shapes1.nfields( );
        auto size = shapes1.ndof( );
        auto offset = size_t { 0 };

        MLHP_CHECK( shapes0.nfields( ) == nfields, "Inconsistent number of fields." );

        for( size_t kfield = 0; kfield < nfields; ++kfield )
        {
            auto ndof = shapes1.ndof( kfield );
            auto nblocks = shapes1.nblocks( kfield );

            auto Nk = shapes1.noalias( kfield, 0 );
            auto uk = evaluateSolution( shapes0, locationMap0, oldDofs, kfield );

            linalg::elementLhs<linalg::UnsymmetricDenseMatrix>( targets[0].data( ), 
                size, offset, ndof, offset, ndof, [&]( size_t i, size_t j )
            {
                return Nk[i] * Nk[j] * weightDetJ;
            } );

            linalg::elementRhs( targets[1].data( ) + offset, ndof, nblocks, [&]( size_t i )
            {
                return Nk[i] * uk * weightDetJ;

            } );

            offset += ndof;
        }
    };

    std::vector types = { AssemblyType::UnsymmetricMatrix, AssemblyType::Vector };

    return BasisProjectionIntegrand<D>( types, DiffOrders::Shapes, evaluate );
}

template<size_t D> MLHP_EXPORT
BasisProjectionIntegrand<D> makeTransientPoissonIntegrand( const spatial::ScalarFunction<D + 1>& capacity,
                                                           const spatial::ScalarFunction<D + 1>& diffusivity,
                                                           const spatial::ScalarFunction<D + 1>& source,
                                                           const std::vector<double>& dofs0,
                                                           std::array<double, 2> timeStep,
                                                           double theta )
{
    auto evaluate = [=, &dofs0]( const LocationMap& locationMap0,
                                 const LocationMap&,
                                 const BasisFunctionEvaluation<D>& shapes0,
                                 const BasisFunctionEvaluation<D>& shapes1,
                                 AlignedDoubleVectors& targets,
                                 double weightDetJ )
    { 
        auto tmp1 = shapes1.sizes( );

        auto ndof = std::get<0>( tmp1 );
        auto nblocks = std::get<1>( tmp1 );
        auto ndofpadded = std::get<2>( tmp1 );

        auto N = shapes1.noalias( 0, 0 );
        auto dN = shapes1.noalias( 0, 1 );

        auto u = evaluateSolution( shapes0, locationMap0, dofs0 );
        auto du = evaluateGradient( shapes0, locationMap0, dofs0 );

        auto xyz = shapes1.xyz( );

        auto xyzt0 = array::append( xyz, timeStep[0] );
        auto xyzt1 = array::append( xyz, timeStep[1] );

        double c = capacity( xyzt1 ) * weightDetJ / ( timeStep[1] - timeStep[0] );
        double k = diffusivity( xyzt1 ) * weightDetJ;

        double source0 = theta == 1.0 ? 0.0 : source( xyzt0 ) * weightDetJ;
        double source1 = theta == 0.0 ? 0.0 : source( xyzt1 ) * weightDetJ;

        linalg::symmetricElementLhs( targets[0].data( ), ndof, nblocks, [&]( size_t i, size_t j )
        {
            double value = N[i] * N[j] * c;

            for( size_t axis = 0; axis < D; ++axis )
            {
                value += dN[axis * ndofpadded + i] * dN[axis * ndofpadded + j] * theta * k;

            } // component

            return value;
        } );

        linalg::elementRhs( targets[1].data( ), ndof, nblocks, [&]( size_t i )
        {
            double value = N[i] * ( c * u + ( 1.0 - theta ) * source0 + theta * source1 );

            for( size_t axis = 0; axis < D; ++axis )
            {
                value -= dN[axis * ndofpadded + i] * ( 1.0 - theta ) * k * du[axis];
            }

            return value;
        } );
    };

    std::vector types = { AssemblyType::SymmetricMatrix, AssemblyType::Vector };

    return BasisProjectionIntegrand<D>( types, DiffOrders::FirstDerivatives, evaluate );
}

#define MLHP_INSTANTIATE_DIM( D )                                                                                 \
                                                                                                                  \
    template MLHP_EXPORT                                                                                          \
    DomainIntegrand<D> makePoissonIntegrand( const spatial::ScalarFunction<D>& kappa,                             \
                                             const spatial::ScalarFunction<D>& source );                          \
    template MLHP_EXPORT                                                                                          \
    DomainIntegrand<D> makeAdvectionDiffusionIntegrand( const spatial::VectorFunction<D>& velocity,               \
                                                        const spatial::ScalarFunction<D>& diffusivity,            \
                                                        const spatial::ScalarFunction<D>& source );               \
                                                                                                                  \
    template MLHP_EXPORT                                                                                          \
    Kinematics<D> makeSmallStrainKinematics( );                                                                   \
                                                                                                                  \
    template MLHP_EXPORT                                                                                          \
    DomainIntegrand<D> makeIntegrand( const Kinematics<D>& kinematics,                                            \
                                      const Constitutive<D>& constitutive,                                        \
                                      const spatial::VectorFunction<D, D>& force );                               \
                                                                                                                  \
    template MLHP_EXPORT                                                                                          \
    DomainIntegrand<D> makeL2ProjectionIntegrand( const spatial::ScalarFunction<D>& source );                     \
                                                                                                                  \
    template MLHP_EXPORT                                                                                          \
    DomainIntegrand<D> makeL2ProjectionIntegrand( const spatial::ScalarFunction<D>& weight,                       \
                                                  const spatial::ScalarFunction<D>& source );                     \
                                                                                                                  \
    template MLHP_EXPORT                                                                                          \
    DomainIntegrand<D> makeL2ErrorIntegrand( const std::vector<double>& solutionDofs,                             \
                                             const spatial::ScalarFunction<D>& solutionFunction );                \
                                                                                                                  \
    template MLHP_EXPORT                                                                                          \
    DomainIntegrand<D> makeEnergyErrorIntegrand( const std::vector<double>& solutionDofs,                         \
                                                 const spatial::VectorFunction<D, D>&                             \
                                                     analyticalDerivatives );                                     \
                                                                                                                  \
    template MLHP_EXPORT                                                                                          \
    DomainIntegrand<D> makeInternalEnergyIntegrand( const std::vector<double>& solutionDofs,                      \
                                                    const Kinematics<D>& kinematics,                              \
                                                    const Constitutive<D>& constitutive,                          \
                                                    size_t ncomponents );                                         \
                                                                                                                  \
    template MLHP_EXPORT                                                                                          \
    BasisProjectionIntegrand<D> makeL2BasisProjectionIntegrand( const std::vector<double>& oldDofs );             \
                                                                                                                  \
    template MLHP_EXPORT                                                                                          \
    BasisProjectionIntegrand<D> makeTransientPoissonIntegrand( const spatial::ScalarFunction<D + 1>& capacity,    \
                                                               const spatial::ScalarFunction<D + 1>& diffusivity, \
                                                               const spatial::ScalarFunction<D + 1>& source,      \
                                                               const std::vector<double>& dofs0,                  \
                                                               std::array<double, 2> timeStep,                    \
                                                               double theta );                                    \
                                                                                                                  \
    template class SurfaceIntegrand<D>;                                                                           \
                                                                                                                  \
    template MLHP_EXPORT                                                                                          \
    SurfaceIntegrand<D> makeNeumannIntegrand( const spatial::ScalarFunction<D>& function );                       \
                                                                                                                  \
    template MLHP_EXPORT                                                                                          \
    SurfaceIntegrand<D> makeNeumannIntegrand( const spatial::VectorFunction<D, D>& function );                    \
                                                                                                                  \
    template MLHP_EXPORT                                                                                          \
    SurfaceIntegrand<D> makeRobinIntegrand( const spatial::ScalarFunction<D>& neumann,                            \
                                            const spatial::ScalarFunction<D>& dirichlet );

    MLHP_DIMENSIONS_XMACRO_LIST
#undef MLHP_INSTANTIATE_DIM

} // mlhp
