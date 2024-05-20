# This file is part of the mlhpbf project. License: See LICENSE

cmake_minimum_required( VERSION 3.12 )

project( mlhpbf LANGUAGES CXX )

# Find out if this is the root CMake project or not
get_directory_property( hasParent PARENT_DIRECTORY )
string( COMPARE EQUAL "${hasParent}" "" PBF_IS_ROOT )

# Options
option( PBF_ENABLE_TESTS "Enable verification tests." ${PBF_IS_ROOT} )
option( PBF_ENABLE_EXAMPLES "Enable example drivers." ${PBF_IS_ROOT} )
option( PBF_ENABLE_PYTHONBINDINGS "Enable python bindings." OFF )

# -------------------- External dependencies ----------------------

# Configure mlhp
set( MLHP_ENABLE_PYTHONBINDINGS ${PBF_ENABLE_PYTHONBINDINGS} CACHE BOOL "" FORCE )
set( MLHP_DIMENSIONS_TO_INSTANTIATE "1, 2, 3, 4" CACHE STRING "" )
set( MLHP_DEBUG_CHECKS OFF CACHE BOOL "" )
set( MLHP_INDEX_SIZE_DOFS "64" CACHE STRING "" )

add_subdirectory( external/mlhp )

# ------------------------- PBF library ---------------------------

set( MLHPBF_HEADERS laser.hpp materials.hpp history.hpp thermal.hpp mechanical.hpp )
list( TRANSFORM MLHPBF_HEADERS PREPEND ${CMAKE_CURRENT_SOURCE_DIR}/include/mlhp/pbf/ )

add_library( mlhpbf INTERFACE )

target_sources( mlhpbf INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}/include/mlhp/pbf.hpp ${MLHPBF_HEADERS} )
target_include_directories( mlhpbf INTERFACE include external )
target_link_libraries( mlhpbf INTERFACE mlhp::core )

add_library( mlhp::pbf ALIAS mlhpbf )

file( COPY materials DESTINATION ${CMAKE_BINARY_DIR} )

# ---------------------- Verification tests -----------------------

if( ${PBF_ENABLE_TESTS} )
	include( tests/files.cmake )
	list( TRANSFORM PBF_TEST_SOURCES PREPEND tests/ )

	add_executable( mlhpbf_tests ${PBF_TEST_SOURCES} )
	target_link_libraries( mlhpbf_tests PRIVATE mlhp::pbf )
	set_target_properties( mlhpbf_tests PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin )
	target_include_directories( mlhpbf_tests PRIVATE mlhp/external/catch2 )

endif( ${PBF_ENABLE_TESTS} )

# ----------------------- Python bindings -------------------------

if( ${PBF_ENABLE_PYTHONBINDINGS} )

    include( src/python/files.cmake )
 
    list( TRANSFORM PBF_PYTHON_BINDING_SOURCES PREPEND src/python/ )
 
    pybind11_add_module( pymlhpbf ${PBF_PYTHON_BINDING_SOURCES} )
 
    target_link_libraries( pymlhpbf PRIVATE mlhp::pbf mlhp_private_compile_flags )
    
    target_include_directories( pymlhpbf PRIVATE . )
      
    # Set output directories
    set_target_properties( pymlhpbf PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${MLHP_BUILD_BINARY_DIR} )

    # Whenever we build pymlhpbf we want to build pymlhpcore too
    add_dependencies( pymlhpbf pymlhpcore )

    # Copy python sources
    file( COPY src/python/pbf.py DESTINATION ${MLHP_BUILD_BINARY_DIR} )
	
    install( TARGETS pymlhpbf LIBRARY DESTINATION . )
    install( FILES src/python/pbf.py DESTINATION . )

endif( ${PBF_ENABLE_PYTHONBINDINGS} )

# ----------------------- Example drivers -------------------------

function( createCppExample name description )
    string( TOUPPER ${name} nameUpperCase )
    set( exampleOption PBF_ENABLE_EXAMPLE_${nameUpperCase} )
    
    if( ${PBF_ENABLE_EXAMPLES} )
        option( ${exampleOption} ${description} OFF )
        
        if( "${${exampleOption}}" )
            add_executable( ${name} examples/${name}.cpp  )
            target_link_libraries( ${name} PRIVATE mlhp::pbf )
            set_target_properties( ${name} PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin )
            
        endif( "${${exampleOption}}" )
           
    else( ${PBF_ENABLE_EXAMPLES} )
        unset( ${exampleOption} CACHE )
    endif( ${PBF_ENABLE_EXAMPLES} )
endfunction( )

function( createPythonExample name description )
    if( ${PBF_ENABLE_PYTHONBINDINGS} )
        configure_file( examples/${name}.py ${MLHP_BUILD_BINARY_DIR}/${name}.py COPYONLY )
    endif( ${PBF_ENABLE_PYTHONBINDINGS} )
endfunction( )

createCppExample( hatched_square "NIST hatched square on a bare plate." )
createCppExample( single_track "Single track on bare plate." )

createPythonExample( singletrack "Single track thermal computation." )
createPythonExample( steadystate "Steady state thermal computation  ." )
