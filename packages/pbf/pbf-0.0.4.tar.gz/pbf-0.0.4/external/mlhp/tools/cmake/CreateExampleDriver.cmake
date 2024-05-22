function( CreateExampleCppDriver name description )

    string( TOUPPER ${name} nameUpperCase )
    
    set( exampleOption MLHP_ENABLE_CPP_EXAMPLE_${nameUpperCase} )
    
    if( ${MLHP_ENABLE_EXAMPLES} )
    
        option( ${exampleOption} ${description} OFF )
        
        if( "${${exampleOption}}" )
        
            add_executable( ${name} examples/${name}.cpp  )
            
            target_link_libraries( ${name} PRIVATE mlhpcore )
                        
            set_target_properties( ${name} PROPERTIES ${MLHP_OUTPUT_DIRS} )
            
        endif( "${${exampleOption}}" )
           
    else( ${MLHP_ENABLE_EXAMPLES} )
  
        unset( ${exampleOption} CACHE )
        
    endif( ${MLHP_ENABLE_EXAMPLES} )
    
endfunction()

function( CreateExamplePythonDriver name description )

    if( ${MLHP_ENABLE_EXAMPLES} AND ${MLHP_ENABLE_PYTHONBINDINGS} )
    
        configure_file( examples/${name}.py ${MLHP_BUILD_BINARY_DIR}/${name}.py COPYONLY )
    
    endif( ${MLHP_ENABLE_EXAMPLES} AND ${MLHP_ENABLE_PYTHONBINDINGS} )

endfunction()
