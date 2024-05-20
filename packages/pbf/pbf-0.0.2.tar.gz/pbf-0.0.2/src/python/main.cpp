// This file is part of the mlhpbf project. License: See LICENSE

#include "pybind11/pybind11.h"
#include "pybind11/functional.h"
#include "pybind11/stl.h"

#include "mlhp/pbf.hpp"
#include "external/mlhp/src/python/helper.hpp"

namespace mlhp::bindings
{

PYBIND11_MODULE( pymlhpbf, m )
{
    m.doc( ) = "Powder bed fusion application.";

    // Base grid
    auto createMeshF = []( std::array<double, 3> min, 
                           std::array<double, 3> max, 
                           double rootElementSize, 
                           double layerHeight, 
                           double zfactor )
    {
        return std::make_shared<CartesianGrid<3>>( createBaseMeshTicks<3>( 
            { min, max }, rootElementSize, layerHeight, zfactor ) );
    };

    m.def( "createMesh", createMeshF, pybind11::arg( "min" ), pybind11::arg( "max" ), 
        pybind11::arg( "rootElementSize" ), pybind11::arg( "layerHeight" ), 
        pybind11::arg( "elementSizeZFactor" ) = 0.64 );

    // Materials
    auto material = pybind11::class_<Material, std::shared_ptr<Material>>( m, "Material" );

    material.def( pybind11::init<>( ) );
    material.def( "__str__", []( const Material& self ){ return "Material (name: " + self.name + ")"; } );
    material.def_readwrite( "initialized", &Material::initialized );
    material.def_readwrite( "name", &Material::name );
    material.def_readwrite( "plasticModelSelector", &Material::plasticModelSelector );
    material.def_readwrite( "solidTemperature", &Material::solidTemperature );
    material.def_readwrite( "liquidTemperature", &Material::liquidTemperature );
    material.def_readwrite( "latentHeatOfFusion", &Material::latentHeatOfFusion );
    material.def_readwrite( "regularization", &Material::regularization );

    m.def( "readMaterialFile", []( std::string path ) { return readMaterialFile( path ); }, 
        pybind11::arg( "Path to material json file." ) );

    m.def( "readMaterialString", readMaterialString, 
        pybind11::arg( "Json string with material data." ) );

    auto makeMaterialF = []( std::string name ) -> Material
    {
        if( name == "IN625" ) return makeIN625( );

        MLHP_THROW( "Unknown material " + name + ". Available are [IN625]." );
    };

    m.def( "makeMaterial", makeMaterialF, pybind11::arg( "name" ) );

    // Laser
    auto laserPosition = pybind11::class_<laser::Point<3>>( m, "LaserPosition" );

    auto laserPositionStr = []( const laser::Point<3>& position )
    {
        auto sstream = std::ostringstream { };

        sstream << "LaserPosition: xyz = " << position.xyz << 
            ", time = " << position.time << ", power = " << position.power << "";

        return sstream.str( );
    };

    laserPosition.def( pybind11::init<std::array<double, 3>, double, double>( ),
                       pybind11::arg( "xyz" ), pybind11::arg( "time" ), pybind11::arg( "power" ) );
    laserPosition.def( "__str__", laserPositionStr );
    laserPosition.def_readwrite( "xyz", &laser::Point<3>::xyz );
    laserPosition.def_readwrite( "time", &laser::Point<3>::time );
    laserPosition.def_readwrite( "power", &laser::Point<3>::power );

    auto gaussianBeamF = []( double sigma, double absorptivity ) -> ScalarFunctionWrapper<2>
    {
        return std::function { spatial::integralNormalizedGaussBell<2>( { }, sigma, absorptivity ) };
    };
    
    m.def( "gaussianBeam", gaussianBeamF, pybind11::arg( "sigma" ), pybind11::arg( "absorptivity" ) = 1.0 );
    
    auto volumeSourceF = []( const laser::LaserTrack<3>& track,
                             const ScalarFunctionWrapper<2>& beamShape,
                             double depthSigma )
    {
        return ScalarFunctionWrapper<4> { laser::volumeSource<3>( track, beamShape, depthSigma ) };
    };

    m.def( "volumeSource", volumeSourceF, pybind11::arg( "laserTrack" ), 
        pybind11::arg( "beamShape" ), pybind11::arg( "depthSigma" ) = 1.0 );

    auto laserBasedRefinementF = []( const laser::LaserTrack<3>& track,
                                     double sigma, size_t depth )
    { 
        return makeLaserBasedRefinement<3>( track, sigma * 4, depth );
    };

    m.def( "laserBasedRefinement", laserBasedRefinementF, pybind11::arg( "laserTrack" ), 
        pybind11::arg( "sigma" ), pybind11::arg( "maxdepth" ) );

    // Thermal history
    auto thermalHistory = pybind11::class_<ThermoplasticHistory<3>, 
        std::shared_ptr<ThermoplasticHistory<3>>>( m, "ThermalHistory" );

    auto thermalHistoryString = []( const ThermoplasticHistory<3>& self )
    {
        auto sstream = std::stringstream { };
        auto memory = self.grid->memoryUsage( ) + utilities::vectorInternalMemory( self.data );

        sstream << "ThermalHistory (address: " << &self << ")\n";
        sstream << "    nleaves / ncells         : " << self.grid->nleaves( ) << " / " << self.grid->ncells( ) << "\n";
        sstream << "    maximum refinement level : " << static_cast<int>( self.maxdepth ) << "\n";
        sstream << "    heap memory usage        : " << utilities::memoryUsageString( memory ) << "\n";

        return sstream.str( );
    };

    thermalHistory.def( pybind11::init<>( ) );
    thermalHistory.def( pybind11::init<HierarchicalGridSharedPtr<3>&,
                        RefinementLevel, std::vector<HistoryData>>( ) );
    thermalHistory.def( "__str__", thermalHistoryString );
    thermalHistory.def_readwrite( "grid", &ThermoplasticHistory<3>::grid );

    auto initializeHistoryF = []( const GridSharedPtr<3>& baseGrid,
                                  size_t maxdepth, double powderHeight )
    {
        auto domainFunction = utilities::returnValue( false );

        auto history = initializeHistory<3>( baseGrid, domainFunction, powderHeight, 4, maxdepth );

        return std::make_shared<ThermoplasticHistory<3>>( std::move( history ) );
    };

    m.def( "initializeHistory", initializeHistoryF, pybind11::arg( "baseGrid" ), 
        pybind11::arg( "maxdepth" ), pybind11::arg( "powderHeight" ) = 0.0 );

    // Thermal physics
    using MaterialMap = std::map<std::string, std::shared_ptr<Material>>;

    auto convertMaterials = []( MaterialMap&& map )
    {
        struct
        {
            Material& baseplate, &structure, &powder, &air;
        } 
        materialStruct = 
        { 
            .baseplate = *map["baseplate"], 
            .structure = *map["structure"],
            .powder    = *map["powder"], 
            .air       = *map["air"]
        };

        return materialStruct;
    };

    auto combineSources = []<size_t D>( std::vector<ScalarFunctionWrapper<D>>&& sources )
    {
        return std::function { [sources = std::move(sources)]( std::array<double, D> xyzt )
        {
            auto intensity = 0.0;

            for( auto& source : sources )
            {
                intensity += source.get( )( xyzt );
            }
        
            return intensity;
        } };
    };

    auto makeThermalInitializationIntegrandF = [=]( MaterialMap map,
                                                    std::vector<ScalarFunctionWrapper<4>> sources,
                                                    std::shared_ptr<ThermoplasticHistory<3>> history0,
                                                    const DoubleVector& dofs0,
                                                    double time0, double dt, double theta )
    {
        auto materials = convertMaterials( std::move( map ) );
        auto source = combineSources( std::move( sources ) );
 
        return makeThermalInitializationIntegrand<3>( materials, source,
            *history0, dofs0.get( ), time0, dt, theta );
    };

    m.def( "makeThermalInitializationIntegrand", makeThermalInitializationIntegrandF,
        pybind11::arg( "materials" ), pybind11::arg( "sources" ), pybind11::arg( "history" ), 
        pybind11::arg( "dofs0" ), pybind11::arg( "time0" ), pybind11::arg( "deltaT" ), 
        pybind11::arg( "theta" ) );

    auto makeTimeSteppingThermalIntegrandF = [=]( MaterialMap map,
                                                  std::shared_ptr<ThermoplasticHistory<3>> history,
                                                  const DoubleVector& projectedDofs0,
                                                  const DoubleVector& dofs1,
                                                  double dt, double theta )
    {
        auto materials = convertMaterials( std::move( map ) );
        
        return makeTimeSteppingThermalIntegrand<3>( materials,
            *history, projectedDofs0.get( ), dofs1.get( ), dt, theta );
    };

    m.def( "makeTimeSteppingThermalIntegrand", makeTimeSteppingThermalIntegrandF,
        pybind11::arg( "materials" ), pybind11::arg( "history" ), 
        pybind11::arg( "projectedDofs0" ), pybind11::arg( "dofs1" ), 
        pybind11::arg( "deltaT" ), pybind11::arg( "theta" ) );

    
    auto makeSteadyStateThermalIntegrandF = [=]( MaterialMap map,
                                                 std::vector<ScalarFunctionWrapper<3>> sources,
                                                 std::shared_ptr<ThermoplasticHistory<3>> history,
                                                 const DoubleVector& dofs,
                                                 std::array<double, 3> laserVelocity )
    {
        auto materials = convertMaterials( std::move( map ) );
        auto source = combineSources( std::move( sources ) );

        return makeSteadyStateThermalIntegrand<3>( materials, 
            source, *history, dofs.get( ), laserVelocity );
    };
    
    m.def( "makeSteadyStateThermalIntegrand", makeSteadyStateThermalIntegrandF,
        pybind11::arg( "materials" ), pybind11::arg( "sources" ), pybind11::arg( "history" ),
        pybind11::arg( "dofs" ), pybind11::arg( "laserVelocity" ) = std::array { 1.0, 0.0, 0.0 } );


    auto computeDirichletIncrementF = []( const DofIndicesValuesPair& dirichlet,
                                          const DoubleVector& dofs,
                                          double factor )
    { 
        auto dirichletIncrement = dirichlet;

        for( size_t idof = 0; idof < dirichlet.first.size( ); ++idof )
        {
            dirichletIncrement.second[idof] = factor * ( dirichlet.second[idof] - 
                dofs.get( )[dirichlet.first[idof]] );
        }    

        return dirichletIncrement;
    };

    m.def( "computeDirichletIncrement", computeDirichletIncrementF, pybind11::arg( "dirichletDofs" ), 
           pybind11::arg( "dofs" ), pybind11::arg( "factor" ) = 1.0 );

    auto thermalEvaluatorF = []( const std::shared_ptr<const AbsBasis<3>>& basis,
                                 const DoubleVector& dofs ) -> ScalarFunctionWrapper<3>
    {
        return std::function { makeEvaluationFunction<3>( basis, dofs.get( ) ) };
    };

    m.def( "internalThermalEvaluator", thermalEvaluatorF, pybind11::arg( "basis" ), pybind11::arg( "dofs" ) );
}

} // mlhp::bindings

