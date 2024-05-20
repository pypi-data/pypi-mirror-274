// This file is part of the mlhp project. License: See LICENSE

#ifndef MLHP_CORE_DENSE_HPP
#define MLHP_CORE_DENSE_HPP

#include "mlhp/core/memory.hpp"
#include "mlhp/core/coreexport.hpp"

#include <cstddef>
#include <span>

namespace mlhp::linalg
{

//! In-place row-major LU decomposition with partial pivoting
MLHP_EXPORT void lu( double* M, size_t* p, size_t size );

//! Forward and backward substitution using lu factorization
MLHP_EXPORT void luSubstitute( const double* LU, const size_t* p, size_t size, const double* b, double* u );

//! Inverse computation using lu factorization
MLHP_EXPORT void luInvert( double* LU, size_t* p, size_t size, double* I );

//! Compute determinant based on LU factorization (product of diagonal entries)
MLHP_EXPORT MLHP_PURE double luDeterminant( const double* LU, size_t size );

//! Inverts row major dense (size, size) matrix
MLHP_EXPORT void invert( const double* source, double* target, size_t size );

//! Matrix multiplication for square row-major matrices
void mmproduct( const double* left, const double* right, double* target, size_t size );

//! Matrix multiplication for non-square row-major matrices
void mmproduct( const double* left, const double* right, double* target, size_t leftM, size_t leftN, size_t rightN );

//! Matrix vector products
void mvproduct( const double* M, const double* v, double* target, size_t size1, size_t size2 );
void mvproduct( const double* M, const double* v, double* target, size_t size );

template<size_t D1, size_t D2>
std::array<double, D1> mvproduct( const double* M, std::array<double, D2> v );

template<size_t D>
std::array<double, D> mvproduct( const double* M, std::array<double, D> v );

template<size_t D1, size_t D2>
std::array<double, D1> mvproduct( const std::array<double, D1 * D2>& M, std::array<double, D2> v );

// Assumptions: Aligned, padded, no aliasing
struct SymmetricDenseMatrix { };
struct UnsymmetricDenseMatrix { };

template<bool Symmetric>
struct DenseMatrixTypeHelper { using type = SymmetricDenseMatrix; };

template<>
struct DenseMatrixTypeHelper<false> { using type = UnsymmetricDenseMatrix; };

template<bool Symmetric>
using DenseMatrixType = typename DenseMatrixTypeHelper<Symmetric>::type;

template<typename MatrixType>
inline constexpr bool isSymmetricDense = std::is_same_v<MatrixType, SymmetricDenseMatrix>;

template<typename MatrixType>
inline constexpr bool isUnsymmetricDense = std::is_same_v<MatrixType, UnsymmetricDenseMatrix>;

template<typename DenseMatrixType>
constexpr size_t denseRowIncrement( size_t iRow, size_t paddedLength );

template<typename T = double>
auto symmetricNumberOfBlocks( size_t iRow );

template<typename T = double>
auto symmetricDenseOffset( size_t rowI, size_t columnJ );

template<typename MatrixType, typename T>
auto indexDenseMatrix( T* matrix, size_t i, size_t j, size_t paddedSize );

template<typename MatrixType, typename T = double>
auto denseMatrixStorageSize( size_t size );

template<typename TargetMatrixType, typename MatrixExpr>
void elementLhs( double* target, size_t size, size_t nblocks, MatrixExpr&& expression );

// Write block into dense matrix
template<typename TargetMatrixType, typename MatrixExpr> inline
void elementLhs( double* target, size_t allsize1, 
                 size_t offset0, size_t size0, 
                 size_t offset1, size_t size1, 
                 MatrixExpr&& expression );

template<typename MatrixExpr>
void unsymmetricElementLhs( double* target, size_t size, size_t nblocks, MatrixExpr&& function );

// Same as above but assuming upper storage
template<typename MatrixExpr>
void symmetricElementLhs( double* target, size_t size, size_t nblocks, MatrixExpr&& function );

// In-place addition of a vector with a given expression, assuming no aliasing.
template<typename VectorExpr = void>
void elementRhs( double* target, size_t size, size_t nblocks, VectorExpr&& function );

template<typename T>
auto adapter( T&& span, size_t size1 );

} // namespace mlhp::linalg

#include "mlhp/core/dense_impl.hpp"

#endif // MLHP_CORE_DENSE_HPP
