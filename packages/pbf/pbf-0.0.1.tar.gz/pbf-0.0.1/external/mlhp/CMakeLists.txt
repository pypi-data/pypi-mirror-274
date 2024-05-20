# This file is part of the mlhp project. License: See LICENSE

cmake_minimum_required( VERSION 3.12 )

project( mlhp LANGUAGES CXX )

# Find out if mlhp is the root CMake project or not
get_directory_property( hasParent PARENT_DIRECTORY)
string( COMPARE EQUAL "${hasParent}" "" MLHP_IS_ROOT )

# ------------------- set project variables -----------------------

option( BUILD_SHARED_LIBS "Build shared library" ON )
option( MLHP_DEBUG_CHECKS "Enable debug checks with (hopefully) minor performance penalty." ON )
option( MLHP_ALL_OPTIMIZATIONS "Compile with all optimizations, including platform specific ones" ON )

option( MLHP_ENABLE_PYTHONBINDINGS "Enable pybind11 based python interface" OFF )
option( MLHP_ENABLE_TESTS "Enable unit-tests and system tests if also python bindings are ON." ${MLHP_IS_ROOT} )
option( MLHP_ENABLE_EXAMPLES "Enable example drivers." OFF )
option( MLHP_ENABLE_OMP "Compile with shared memory parallelism." ON )

set( MLHP_DIMENSIONS_TO_INSTANTIATE "1, 2, 3, 4" CACHE STRING "List of spatial dimensions to compile." )

set( MLHP_BUILD_ARCHIVE_DIR ${CMAKE_BINARY_DIR}/lib CACHE PATH "Build directory for static libs." )
set( MLHP_BUILD_LIBRARY_DIR ${CMAKE_BINARY_DIR}/lib CACHE PATH "Build directory for dynamic libs." )
set( MLHP_BUILD_BINARY_DIR ${CMAKE_BINARY_DIR}/bin CACHE PATH "Build directory for binaries." )

set( MLHP_SIMD_ALIGNMENT 32 CACHE STRING "Simd over-alignment 32 or 64, depending on cache line size of the CPU." )
set( MLHP_INDEX_SIZE_CELLS 32 CACHE STRING "Unsigned integer size used to index mesh cells." )
set( MLHP_INDEX_SIZE_DOFS 32 CACHE STRING "Unsigned integer size used to index degrees of freedom and sparse indices." )

mark_as_advanced( MLHP_BUILD_ARCHIVE_DIR MLHP_BUILD_LIBRARY_DIR MLHP_BUILD_BINARY_DIR
                  MLHP_INDEX_SIZE_CELLS MLHP_INDEX_SIZE_DOFS )

set( MLHP_OUTPUT_DIRS ARCHIVE_OUTPUT_DIRECTORY ${MLHP_BUILD_ARCHIVE_DIR}
                      LIBRARY_OUTPUT_DIRECTORY ${MLHP_BUILD_LIBRARY_DIR}
                      RUNTIME_OUTPUT_DIRECTORY ${MLHP_BUILD_BINARY_DIR} )
       
# Changes the default install path to build/install, assuming build is the project directory
if ( CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT )
    set ( CMAKE_INSTALL_PREFIX "${CMAKE_CURRENT_BINARY_DIR}/install" CACHE PATH "default install path" FORCE )
endif( )

# Set up build types with Release as default
include(tools/cmake/ConfigureBuildType.cmake)

# ---------------------------- Core -------------------------------

# Provides interface target vtu11::vtu11
add_subdirectory(external/vtu11)

# Create mlhp_public_compile_flags and mlhp_private_compile_flags interface targets
include(tools/cmake/ConfigureCompiler.cmake)

# Configure the explicit template instantiation of space dimensions
include(tools/cmake/ConfigureInstantiation.cmake)

# To automatically configure a library export header into build tree
include(GenerateExportHeader)

# Sets MLHP_CORE_SOURCES and MLHP_CORE_INCLUDES
include( src/core/files.cmake )

list( TRANSFORM MLHP_CORE_SOURCES PREPEND src/core/ )
list( TRANSFORM MLHP_CORE_INCLUDES PREPEND include/mlhp/core/ )

add_library( mlhpcore ${MLHP_CORE_SOURCES} ${MLHP_CORE_INCLUDES} include/mlhp/core.hpp )
add_library( mlhp::core ALIAS mlhpcore )

target_link_libraries( mlhpcore PRIVATE mlhp_private_compile_flags vtu11::vtu11
                                PUBLIC mlhp_public_compile_flags )

target_include_directories( mlhpcore PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include 
                                            ${CMAKE_CURRENT_BINARY_DIR}/include )   
# Not sure what this does: $<INSTALL_INTERFACE:include>

generate_export_header( mlhpcore EXPORT_MACRO_NAME MLHP_EXPORT EXPORT_FILE_NAME 
                        ${CMAKE_CURRENT_BINARY_DIR}/include/mlhp/core/coreexport.hpp )

# Set output directories
set_target_properties( mlhpcore PROPERTIES ${MLHP_OUTPUT_DIRS} )

install( TARGETS mlhpcore
         EXPORT mlhpcore-targets
         ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
         LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
         RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
         INCLUDES DESTINATION ${LIBLEGACY_INCLUDE_DIRS} )

# install( DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/include/mlhp
#          DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/ )
#         
# install( DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/include/mlhp
#          DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/ )

# ----------------------- Core testrunner -------------------------

if( ${MLHP_ENABLE_TESTS} )

    # Creates MLHP_CORE_TEST_SOURCES variable
    include( tests/core/files.cmake )
    include( tests/system/files.cmake )

    list( TRANSFORM MLHP_CORE_TEST_SOURCES PREPEND tests/core/ )
    list( TRANSFORM MLHP_SYSTEM_TEST_SOURCES PREPEND tests/system/ )

    add_executable( mlhpcore_testrunner ${MLHP_CORE_TEST_SOURCES} )

    target_link_libraries( mlhpcore_testrunner PRIVATE mlhp::core mlhp_private_compile_flags )

    target_include_directories( mlhpcore_testrunner PRIVATE . )   

    file( GLOB MLHP_CORE_TESTFILES tests/core/testfiles/* )
    file( COPY ${MLHP_CORE_TESTFILES} DESTINATION testfiles/core )

    # Set output directories
    set_target_properties( mlhpcore_testrunner PROPERTIES ${MLHP_OUTPUT_DIRS} )
  
    # Setup system tests
    add_executable( system_testrunner ${MLHP_SYSTEM_TEST_SOURCES} )
                    
    target_link_libraries( system_testrunner PRIVATE mlhp::core mlhp_private_compile_flags )
    
    target_include_directories( system_testrunner PRIVATE . )   
    
    set_target_properties( system_testrunner PROPERTIES ${MLHP_OUTPUT_DIRS} )
  
endif( ${MLHP_ENABLE_TESTS} )

# --------------------------- Examples ----------------------------

include( tools/cmake/CreateExampleDriver.cmake )

CreateExampleCppDriver( fichera_corner "Poisson equation fichera corner benchmark." )
CreateExampleCppDriver( travelling_heat_source "Linear heat equation with moving point-like source." )
CreateExampleCppDriver( wing_elastic_fcm "FCM example with linear elasticity." )

CreateExamplePythonDriver( example_fcm "Placeholder fcm example." )
CreateExamplePythonDriver( example_gmsh "Compute with unstructured grid from gmsh file." )

# ----------------------- Python bindings -------------------------

if( ${MLHP_ENABLE_PYTHONBINDINGS} )

    add_subdirectory( external/pybind11 )

    # Creates MLHP_PYTHON_BINDING_SOURCES variable
    include( src/python/files.cmake )

    list( TRANSFORM MLHP_PYTHON_BINDING_SOURCES PREPEND src/python/ )

    pybind11_add_module( pymlhpcore ${MLHP_PYTHON_BINDING_SOURCES} )

    target_link_libraries( pymlhpcore PRIVATE mlhpcore mlhp_private_compile_flags )
    
    target_include_directories( pymlhpcore PRIVATE . )

    # Set output directories
    set_target_properties( pymlhpcore PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${MLHP_BUILD_BINARY_DIR} )

    # After building pymlhpcore write file bin/mlhpPath.py containing directory of python module
    add_custom_command( TARGET pymlhpcore POST_BUILD COMMAND ${CMAKE_COMMAND} -E echo 
      "$<TARGET_FILE_DIR:pymlhpcore>" > ${MLHP_BUILD_BINARY_DIR}/mlhpPythonPath )

    # Copy python sources
    file( COPY src/python/mlhp.py DESTINATION ${MLHP_BUILD_BINARY_DIR} )

    #install( TARGETS pymlhpcore
    #         EXPORT pymlhpcore-targets
    #         ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    #         LIBRARY DESTINATION ${CMAKE_INSTALL_BINDIR}
    #         RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR} )

	# This install works for building with scikit-build-core
	install( TARGETS pymlhpcore LIBRARY DESTINATION . )
	install( FILES src/python/mlhp.py DESTINATION . )
 
endif( ${MLHP_ENABLE_PYTHONBINDINGS} )

if( ${MLHP_ENABLE_PYTHONBINDINGS} AND ${MLHP_ENABLE_TESTS} )

    # Creates MLHP_PYTHON_TESTS variable
    include( tests/system/files.cmake )

    list( TRANSFORM MLHP_PYTHON_TESTS PREPEND tests/system/ )
            
    file( COPY ${MLHP_PYTHON_TESTS} DESTINATION ${MLHP_BUILD_BINARY_DIR}/systemtests )
    file( COPY tests/system/run_systemtests.py DESTINATION ${MLHP_BUILD_BINARY_DIR} )
        
endif( ${MLHP_ENABLE_PYTHONBINDINGS} AND ${MLHP_ENABLE_TESTS} )

# Configure configuration header to build tree
configure_file( src/core/config.hpp.in include/mlhp/core/config.hpp )
