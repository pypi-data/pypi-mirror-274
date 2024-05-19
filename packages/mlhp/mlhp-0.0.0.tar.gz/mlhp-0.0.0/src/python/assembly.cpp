// This file is part of the mlhp project. License: See LICENSE

#include "pybind11/pybind11.h"
#include "pybind11/functional.h"
#include "pybind11/stl.h"

#include "src/python/helper.hpp"

#include "mlhp/core/assembly.hpp"
#include "mlhp/core/basis.hpp"
#include "mlhp/core/integrands.hpp"

namespace mlhp::bindings
{

template<size_t D, typename MatrixType>
void bindAssemblyDimensionMatrixType( pybind11::module& m, std::string matrixName )
{
    m.def( ( "allocate" + matrixName ).c_str( ), []( const std::shared_ptr<AbsBasis<D>>& basis,
                                                     const DofIndexVector& dirichletDofs )
        { 
            return std::make_shared<MatrixType>( allocateMatrix<MatrixType>( *basis, dirichletDofs ) );
        },
        pybind11::arg( "basis" ), pybind11::arg( "dirichletDofs" ) = DofIndexVector { }
    );
}

template<size_t D>
void bindAssemblyDimension( pybind11::module& m )
{
    bindAssemblyDimensionMatrixType<D, linalg::SymmetricSparseMatrix>( m, "SymmetricSparseMatrix" );
    bindAssemblyDimensionMatrixType<D, linalg::UnsymmetricSparseMatrix>( m, "UnsymmetricSparseMatrix" );

    m.def( add<D>( "makeOffsetOrderDeterminor" ).c_str( ), []( size_t offset )
    { 
        return IntegrationOrderDeterminorWrapper<D>{ makeIntegrationOrderDeterminor<D>( offset ) };
    }, pybind11::arg( "offset" ) = 1 );

    using PythonAssemblyTarget = std::variant
    <
        ScalarDouble*,
        DoubleVector*,
        linalg::UnsymmetricSparseMatrix*,
        linalg::SymmetricSparseMatrix*
    >;

    auto convertTargets = []( const std::vector<PythonAssemblyTarget>& pythonTargets )
    { 
        AssemblyTargetVector targets; 

        for( size_t i = 0; i < pythonTargets.size( ); ++i )
        {
            if( pythonTargets[i].index( ) == 0 ) 
                targets.push_back( std::get<ScalarDouble*>( pythonTargets[i] )->get( ) );
            else if( pythonTargets[i].index( ) == 1 ) 
                targets.push_back( std::get<DoubleVector*>( pythonTargets[i] )->get( ) );
            else if( pythonTargets[i].index( ) == 2 )
                targets.push_back( *std::get<linalg::UnsymmetricSparseMatrix*>( pythonTargets[i] ) );
            else if( pythonTargets[i].index( ) == 3 )
                targets.push_back( *std::get<linalg::SymmetricSparseMatrix*>( pythonTargets[i] ) );
        }

        return targets;
    };

    m.def( "integrateOnDomain", [convertTargets]( const AbsBasis<D>& basis,
                                                  const DomainIntegrand<D>& integrand,
                                                  const std::vector<PythonAssemblyTarget>& targets,
                                                  const AbsQuadrature<D>& quadrature,
                                                  const IntegrationOrderDeterminorWrapper<D>& orderDeterminor,
                                                  const DofIndicesValuesPair& boundaryDofs )
        { 
            return integrateOnDomain( basis, integrand, convertTargets( targets ),
            quadrature, orderDeterminor, boundaryDofs );
        },
        pybind11::arg( "basis" ),
        pybind11::arg( "integrand" ),
        pybind11::arg( "targets" ),
        pybind11::arg( "quadrature" ) = StandardQuadrature<D> { },
        pybind11::arg( "orderDeterminor" ) = IntegrationOrderDeterminorWrapper<D>{ makeIntegrationOrderDeterminor<D>( 1 ) },
        pybind11::arg( "dirichletDofs" ) = DofIndicesValuesPair { } 
    );
    
    m.def( "projectOnto", []( const AbsBasis<D>& basis,
                              const ScalarFunctionWrapper<D>& function )
           { return DoubleVector ( projectOnto<D>( basis, function ) ); } );
    
    m.def( "integrateOnDomain", [convertTargets]( const MultilevelHpBasis<D>& basis0,
                                                  const MultilevelHpBasis<D>& basis1,
                                                  const BasisProjectionIntegrand<D>& integrand,
                                                  const std::vector<PythonAssemblyTarget>& globalTargets,
                                                  const AbsQuadrature<D>& quadrature,
                                                  const IntegrationOrderDeterminorWrapper<D>& orderDeterminor,
                                                  const DofIndicesValuesPair& boundaryDofs )
        { 
            integrateOnDomain( basis0, basis1, integrand, convertTargets( globalTargets ),
                quadrature, orderDeterminor, boundaryDofs );
        },
        pybind11::arg( "basis0" ),
        pybind11::arg( "basis1" ),
        pybind11::arg( "integrand" ),
        pybind11::arg( "targets" ),
        pybind11::arg( "quadrature" ) = StandardQuadrature<D> { },
        pybind11::arg( "orderDeterminor" ) = IntegrationOrderDeterminorWrapper<D>{ makeIntegrationOrderDeterminor<D>( 1 ) },
        pybind11::arg( "dirichletDofs" ) = DofIndicesValuesPair { } 
    );
}

template<size_t... D>
void bindAssemblyDimensions( pybind11::module& m )
{
    [[maybe_unused]] std::initializer_list<int> tmp { ( bindAssemblyDimension<D>( m ), 0 )... };
}

void bindAssemblyDimensionIndependent( pybind11::module& m )
{
    m.def( "allocateVectorWithSameSize", []( const linalg::AbsSparseMatrix& matrix )
    { 
        return DoubleVector( matrix.size1( ), 0.0 );
    } );
}

void bindAssembly( pybind11::module& m )
{
    bindAssemblyDimensions<MLHP_DIMENSIONS_LIST>( m );
    bindAssemblyDimensionIndependent( m );
}

} // mlhp::bindings

