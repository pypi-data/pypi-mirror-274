//// This file is part of the mlhp project. License: See LICENSE
//
//#include "pybind11/pybind11.h"
//#include "pybind11/stl.h"
//
//#include "core/bindings/inc/helper.hpp"
//#include "core/fekernel/inc/sparse.hpp"
//
//namespace mlhp::bindings
//{
//
//void bindLinalg( pybind11::module& m )
//{
//    pybind11::class_<linalg::AbsSparseMatrix, 
//                     std::shared_ptr<linalg::AbsSparseMatrix>> 
//        absSparseMatrix( m, "AbsSparseMatrix" );
//
//    absSparseMatrix.def( "memoryUsage", &linalg::AbsSparseMatrix::memoryUsage );
//
//    [[maybe_unused]]
//    pybind11::class_<linalg::SymmetricSparseMatrix, 
//                     std::shared_ptr<linalg::SymmetricSparseMatrix>> 
//        symmetricSparse( m, "SymmetricSparseMatrix", absSparseMatrix );
//
//    [[maybe_unused]]
//    pybind11::class_<linalg::UnsymmetricSparseMatrix, 
//                     std::shared_ptr<linalg::UnsymmetricSparseMatrix>> 
//        unsymmetricSparse( m, "UnsymmetricSparseMatrix", absSparseMatrix );
//
//    [[maybe_unused]]
//    pybind11::class_<DoubleVector> doubleVector( m, "DoubleVector" );
//
//    doubleVector.def( pybind11::init<std::size_t>( ) );
//    doubleVector.def( pybind11::init<std::size_t, double>( ) );
//    doubleVector.def( "get", &DoubleVector::get );
//}
//
//} // mlhp::bindings
//
