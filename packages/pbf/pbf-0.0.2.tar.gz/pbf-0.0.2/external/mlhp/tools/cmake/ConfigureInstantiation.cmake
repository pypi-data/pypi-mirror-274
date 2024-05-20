# --------------- Prepare C++ xmacro lists of dimensions to instantiate ----------------

string( REPLACE "," " " MLHP_INSTANTIATE_STRIPPED ${MLHP_DIMENSIONS_TO_INSTANTIATE} )

string( REGEX REPLACE "([0-9]+)" "MLHP_INSTANTIATE_DIM(\\1)" MLHP_DIMENSIONS_XMACRO_LIST ${MLHP_INSTANTIATE_STRIPPED} )

message( STATUS "Dimensions: " ${MLHP_DIMENSIONS_TO_INSTANTIATE} )

# ---------- Postprocessing is only instantiated for dimensions 1, 2, and 3 ------------

# Remove all numbers with more than 1 digit
string( REGEX REPLACE "([0-9][0-9]+)" "" MLHP_INSTANTIATE_POSTPROCESSING_STRIPPED1 ${MLHP_INSTANTIATE_STRIPPED} )

# Remove all numbers between 4 and 9, as well as 0
string( REGEX REPLACE "([0,4-9])" "" MLHP_INSTANTIATE_POSTPROCESSING_STRIPPED2 ${MLHP_INSTANTIATE_POSTPROCESSING_STRIPPED1} )

# -------------------------------------- finalize --------------------------------------

# Replace numbers between 1 and 3 with MLHP_INSTANTIATE_DIM(number)
string( REGEX REPLACE "([1-3])" "MLHP_INSTANTIATE_DIM(\\1)" MLHP_POSTPROCESSING_DIMENSIONS_XMACRO_LIST ${MLHP_INSTANTIATE_POSTPROCESSING_STRIPPED2} )
