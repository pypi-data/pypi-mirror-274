// This file is part of the mlhpbf project. License: See LICENSE

#include "pybind11/pybind11.h"
#include "pybind11/functional.h"
#include "pybind11/stl.h"

#include "mlhp/pbf.hpp"
#include "mlhp/src/python/helper.hpp"

namespace mlhp::bindings
{

PYBIND11_MODULE( pymlhpbf, m )
{
    m.doc( ) = "Powder bed fusion application.";

    // Base grid
    m.def( "createMesh", []( std::array<double, 3> min, 
                             std::array<double, 3> max, 
                             double rootElementSize, 
                             double layerHeight, 
                             double zfactor )
        {
            return std::make_shared<CartesianGrid<3>>( createBaseMeshTicks<3>( 
                { min, max }, rootElementSize, layerHeight, zfactor ) );
        }, 
        pybind11::arg( "min" ), pybind11::arg( "max" ), pybind11::arg( "rootElementSize" ),
        pybind11::arg( "layerHeight" ), pybind11::arg( "elementSizeZFactor" ) = 0.64 );

    // Materials
    auto material = pybind11::class_<Material, std::shared_ptr<Material>>( m, "Material" );

    material.def( pybind11::init<>( ) );
    material.def( "__str__", []( const Material& self ){ return "Material (name: " + self.name + ")"; });

    m.def( "readMaterialFile", []( std::string path ) { return readMaterialFile( path ); }, 
        pybind11::arg( "Path to material json file." ) );

    m.def( "readMaterialString", readMaterialString, 
        pybind11::arg( "Json string with material data." ) );

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

    m.def( "initializeHistory", []( const GridSharedPtr<3>& baseGrid,
                                    size_t maxdepth, 
                                    double powderHeight )
        {
            auto domainFunction = utilities::returnValue( false );

            auto history = initializeHistory<3>( baseGrid, domainFunction, powderHeight, 4, maxdepth );

            return std::make_shared<ThermoplasticHistory<3>>( std::move( history ) );
        },
        pybind11::arg( "baseGrid" ), pybind11::arg( "maxdepth" ), 
        pybind11::arg( "powderHeight" ) = 0.0 );

    // Thermal physics
    using MaterialMap = std::map<std::string, std::shared_ptr<Material>>;

    auto convertMaterials = []( MaterialMap&& map )
    {
        struct
        {
            Material& baseplate, &structure, &powder, &air;
        } 
        material = 
        { 
            .baseplate = *map["baseplate"], 
            .structure = *map["structure"],
            .powder    = *map["powder"], 
            .air       = *map["air"]
        };

        return material;
    };

    m.def( "makeThermalInitializationIntegrand", [=]( MaterialMap map,
                                                      std::vector<ScalarFunctionWrapper<4>> sources,
                                                      std::shared_ptr<ThermoplasticHistory<3>> history0,
                                                      const DoubleVector& dofs0,
                                                      double time0, double dt, double theta )
        {
            auto materials = convertMaterials( std::move( map ) );
        
            auto volumeSource = [=]( std::array<double, 4> xyzt )
            {
                auto intensity = 0.0;
        
                for( auto& source : sources )
                {
                    intensity += source.get( )( xyzt );
                }
        
                return intensity;
            };
        
            return makeThermalInitializationIntegrand<3>( materials, 
                volumeSource, *history0, dofs0.get( ), time0, dt, theta );
        }, 
        pybind11::arg( "materials" ), pybind11::arg( "sources" ), pybind11::arg( "history" ), 
        pybind11::arg( "dofs0" ), pybind11::arg( "time0" ), pybind11::arg( "deltaT" ), 
        pybind11::arg( "theta" ) );

    m.def( "makeTimeSteppingThermalIntegrand", [=]( MaterialMap map,
                                                    std::shared_ptr<ThermoplasticHistory<3>> history,
                                                    const DoubleVector& projectedDofs0,
                                                    const DoubleVector& dofs1,
                                                    double dt, double theta )
        {
            auto materials = convertMaterials( std::move( map ) );
        
            return makeTimeSteppingThermalIntegrand<3>( materials,
                *history, projectedDofs0.get( ), dofs1.get( ), dt, theta );
        }, 
        pybind11::arg( "materials" ), pybind11::arg( "history" ), 
        pybind11::arg( "projectedDofs0" ), pybind11::arg( "dofs1" ), 
        pybind11::arg( "deltaT" ), pybind11::arg( "theta" ) );

    m.def( "computeDirichletIncrement", []( const DofIndicesValuesPair& dirichlet,
                                            const DoubleVector& dofs,
                                            double factor )
           { 
               auto dirichletIncrement = dirichlet;

               for( size_t idof = 0; idof < dirichlet.first.size( ); ++idof )
               {
                   dirichletIncrement.second[idof] = dirichlet.second[idof] - 
                       dofs.get( )[dirichlet.first[idof]];
               }    

               return dirichletIncrement;
           }, 
           pybind11::arg( "dirichletDofs" ), 
           pybind11::arg( "dofs" ), 
           pybind11::arg( "factor" ) = 1.0 );
    // Postprocessing

}

} // mlhp::bindings

