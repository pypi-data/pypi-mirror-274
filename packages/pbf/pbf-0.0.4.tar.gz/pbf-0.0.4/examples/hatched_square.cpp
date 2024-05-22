// This file is part of the mlhpbf project. License: See LICENSE

#include "mlhp/pbf.hpp"

namespace mlhp
{

struct Compute : Units
{
    static void compute( )
    {
        static constexpr size_t D = 3;

        auto laserSpeed = 800.0 * mm / s;
        auto laserD4Sigma = 170.0 * um;
        auto laserPower = 180.0 * W;
        auto laserAbsorptivity = 0.32;
        auto laserDepthScaling = 45.0 * um / laserD4Sigma;

        // z = 0 is the base plate
        auto layerHeight = 32 * um; 
        
        auto buildChamber = std::array { std::array { 0.0 * mm, 0.0 * mm, -1.0 * mm },
                                         std::array { 9.0 * mm, 9.0 * mm, layerHeight } };
    
        // NIST example
        auto center = array::setEntry( array::midpoint( buildChamber[0], buildChamber[1] ), D - 1, layerHeight);
        auto laserPositions = laser::hatchedRectanglePositions( center, 3.0 * mm, 2.0 * mm, 100 * um );
        auto laserTrack = laser::hatchedRectangleTrack( laserPositions, laserPower, laserSpeed, 2.0 * ms, 2.0 * ms );

        // Discretization
        auto trefinement = size_t { 4 };
        auto mrefinement = size_t { 3 };
        auto hrefinement = size_t { trefinement + 1 };
    
        auto telementsize = 0.12 * laserD4Sigma; // 20 * um;
        auto timestep = 0.25 * laserD4Sigma / laserSpeed;
        
        // Create base mesh ticks and reduce top layer element height
        auto baseElementSize = telementsize * utilities::binaryPow<size_t>( trefinement );
        auto baseMeshTicks = createBaseMeshTicks<D>( buildChamber, baseElementSize, layerHeight, 0.64 );

        baseMeshTicks.back( ).back( ) = layerHeight;

        auto material = makeIN625( );
        auto material2 = readMaterialFile( "materials/IN625.json" );

        auto general = ProblemSetup<D>
        {
            .buildChamber = buildChamber,
            .duration = laserTrack.back( ).time + 4.0 * ms,
            .baseplate = material,
            .structure = material,
            .powder = makePowder( material ),
            .air = makeAir( material ),
            .baseGrid = std::make_shared<CartesianGrid<D>>( std::move( baseMeshTicks ) ),
        };

        auto sharedSetup = std::make_shared<ProblemSetup<D>>( std::move( general ) );
        auto beamShape = laser::gaussianBeamShape<D>( laserD4Sigma / 4.0, laserAbsorptivity );

        auto thermal = ThermalProblem<D>
        {
            .general = sharedSetup,
            .ambientTemperature = 25.0 * C,
            .refinement = makeLaserBasedRefinement<D>( laserTrack, laserD4Sigma, trefinement ),
            .degree = 1,
            .timeStep = timestep,
            .source = laser::volumeSource<D>( laserTrack, beamShape, laserDepthScaling ),
            .postprocess = makeThermalPostprocessing<D>( "outputs/hatched_square_", 8 )
        };

        auto ux = makeDisplacementBC<D>( boundary::bottom, 0 );
        auto uy = makeDisplacementBC<D>( boundary::bottom, 1 );
        auto uz = makeDisplacementBC<D>( boundary::bottom, 2 );

        auto mechanical = MechanicalProblem<D>
        {
            .general = sharedSetup,
            .refinement = makeLaserBasedRefinement<D>( laserTrack, laserD4Sigma, mrefinement ),
            .degree = 1,
            .dirichlet = { ux, uy, uz },
            .postprocess = makeMechanicalPostprocessing<D>( "outputs/hatched_square_", 8 )
        };

        auto history0 = initializeHistory<D>( sharedSetup->baseGrid, layerHeight, hrefinement );

        computeThermalProblem( thermal, std::move( history0 ) );
        //computeThermomechanicalProblem( thermal, mechanical, std::move( history0 ) );
    }
};

} // namespace mlhp

int main( int argn, char** argv )
{
    mlhp::Compute::compute( );
}
