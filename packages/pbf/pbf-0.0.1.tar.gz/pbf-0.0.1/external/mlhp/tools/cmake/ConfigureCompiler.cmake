add_library( mlhp_public_compile_flags INTERFACE )
add_library( mlhp_private_compile_flags INTERFACE )

target_compile_features( mlhp_public_compile_flags INTERFACE cxx_std_20 )

add_library( mlhp_optimization_flags INTERFACE )
 
if( CMAKE_CXX_COMPILER_ID STREQUAL "GNU" )

    # Hidden visibility
    target_compile_options( mlhp_private_compile_flags INTERFACE -fvisibility=hidden )

    # Compiler warnings
    target_compile_options( mlhp_private_compile_flags INTERFACE -fPIC -pedantic -Wall -Wextra -Wcast-align
        -Wsuggest-attribute=pure -Wimport -Wsuggest-final-methods -Wsuggest-attribute=format 
        -Wsuggest-attribute=malloc -Wformat-y2k -Wpacked  
        -Wswitch-enum -Wwrite-strings -Wformat-nonliteral -Wformat-security -Wcast-qual -Wsuggest-override 
        -Wsuggest-final-types -Wdisabled-optimization -Wformat=2 -Winit-self -Wlogical-op -Wmissing-include-dirs 
        -Wnoexcept -Wold-style-cast -Woverloaded-virtual -Wredundant-decls -Wshadow -Wsign-conversion -Wsign-promo 
        -Wstrict-null-sentinel -Wundef )
   
    target_compile_options( mlhp_private_compile_flags INTERFACE -Wno-attributes -Wno-restrict -Wno-unknown-pragmas )
 
    # Mostly from: https://stackoverflow.com/questions/5088460/flags-to-enable-thorough-and-verbose-g-warnings
    # Removed: -Wsuggest-attribute=noreturn -Wpadded  -Wsuggest-attribute=cold -Wswitch-default 

    target_compile_options( mlhp_optimization_flags INTERFACE -Ofast -march=native -mprefer-vector-width=512 )

elseif( CMAKE_CXX_COMPILER_ID STREQUAL "Intel" )

elseif( CMAKE_CXX_COMPILER_ID STREQUAL "Clang" )

    # Hidden visibility
    target_compile_options( mlhp_private_compile_flags INTERFACE -fvisibility=hidden -fPIC )
    
    # Warnings / errors (enable later: -Wconversion -Wfloat-equal)
    target_compile_options( mlhp_private_compile_flags INTERFACE -Wall -Wextra -Wpedantic -Wshadow -Wunreachable-code 
        -Wuninitialized -Wold-style-cast -Wno-missing-braces -Wno-instantiation-after-specialization )

    # Same optimization flags as gcc
    target_compile_options( mlhp_optimization_flags INTERFACE -Ofast -march=native -mprefer-vector-width=512 )

elseif( CMAKE_CXX_COMPILER_ID STREQUAL "MSVC" )

    # Remove inconsistent dll interface warning
    target_compile_options( mlhp_public_compile_flags INTERFACE /wd4251 )

    # Warning levels
    target_compile_options( mlhp_private_compile_flags INTERFACE /W3 )

    # Optimizations
    target_compile_options( mlhp_optimization_flags INTERFACE /arch:AVX2 /fp:fast /fp:except- )

    ## For when clang is used with msvc
    #target_compile_options( mlhp_private_compile_flags INTERFACE -Wno-missing-braces -Wno-instantiation-after-specialization )

endif( CMAKE_CXX_COMPILER_ID STREQUAL "GNU" )

if( ${MLHP_ALL_OPTIMIZATIONS} )

    message( STATUS "Enabling optimizations for native architecture." )
    
    target_link_libraries( mlhp_public_compile_flags INTERFACE mlhp_optimization_flags )
    
endif( ${MLHP_ALL_OPTIMIZATIONS} )

# Enable omp if option is ON
if( ${MLHP_ENABLE_OMP} )
    find_package(OpenMP REQUIRED COMPONENTS CXX)
    target_link_libraries( mlhp_public_compile_flags INTERFACE OpenMP::OpenMP_CXX )
endif( ${MLHP_ENABLE_OMP} )

