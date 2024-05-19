// This file is part of the mlhp project. License: See LICENSE

#ifndef MLHP_CORE_INTEGRANDCREATORS_HPP
#define MLHP_CORE_INTEGRANDCREATORS_HPP

#include "mlhp/core/integrandtypes.hpp"
#include "mlhp/core/spatial.hpp"

#include <span>

namespace mlhp
{

// Standard linear system domain integrands

template<size_t D> MLHP_EXPORT
DomainIntegrand<D> makeL2ProjectionIntegrand( const spatial::ScalarFunction<D>& source );

template<size_t D> MLHP_EXPORT
DomainIntegrand<D> makeL2ProjectionIntegrand( const spatial::ScalarFunction<D>& weight,
                                              const spatial::ScalarFunction<D>& source );

template<size_t D> MLHP_EXPORT
DomainIntegrand<D> makePoissonIntegrand( const spatial::ScalarFunction<D>& conductivity,
                                         const spatial::ScalarFunction<D>& source );

template<size_t D>  MLHP_EXPORT
DomainIntegrand<D> makeAdvectionDiffusionIntegrand( const spatial::VectorFunction<D>& velocity,
                                                    const spatial::ScalarFunction<D>& diffusivity,
                                                    const spatial::ScalarFunction<D>& source );

// (Linear) Elasticity 

template<size_t D> MLHP_EXPORT
Kinematics<D> makeSmallStrainKinematics( );

MLHP_EXPORT
Constitutive<3> makeIsotropicElasticMaterial( const spatial::ScalarFunction<3>& youngsModulus,
                                              const spatial::ScalarFunction<3>& poissonRatio );

MLHP_EXPORT
Constitutive<2> makePlaneStrainMaterial( const spatial::ScalarFunction<2>& youngsModulus,
                                         const spatial::ScalarFunction<2>& poissonRatio );

MLHP_EXPORT
Constitutive<2> makePlaneStressMaterial( const spatial::ScalarFunction<2>& youngsModulus,
                                         const spatial::ScalarFunction<2>& poissonRatio );

template<size_t D> MLHP_EXPORT
DomainIntegrand<D> makeIntegrand( const Kinematics<D>& kinematics,
                                  const Constitutive<D>& constitutive,
                                  const spatial::VectorFunction<D, D>& force );

// Standard scalar domain integrands

struct ErrorIntegrals
{
    double analyticalSquared = 0, numericalSquared = 0, differenceSquared = 0;

    double numerical( ) { return std::sqrt( numericalSquared ); }
    double analytical( ) { return std::sqrt( analyticalSquared ); }
    double difference( ) { return std::sqrt( differenceSquared ); }
    double relativeDifference( ) { return std::sqrt( differenceSquared / analyticalSquared ); }

    operator AssemblyTargetVector( ) { return { analyticalSquared, numericalSquared, differenceSquared }; }
};

template<size_t D> MLHP_EXPORT
DomainIntegrand<D> makeL2ErrorIntegrand( const std::vector<double>& solutionDofs,
                                         const spatial::ScalarFunction<D>& solutionFunction );

template<size_t D> MLHP_EXPORT
DomainIntegrand<D> makeEnergyErrorIntegrand( const std::vector<double>& solutionDofs,
                                             const spatial::VectorFunction<D, D>& analyticalDerivatives );

template<size_t D> MLHP_EXPORT
DomainIntegrand<D> makeInternalEnergyIntegrand( const std::vector<double>& solutionDofs,
                                                const Kinematics<D>& kinematics,
                                                const Constitutive<D>& constitutive,
                                                size_t ncomponents = ( D * ( D + 1 ) ) / 2 );

// Basis projection linear system domain integrands

template<size_t D> MLHP_EXPORT
BasisProjectionIntegrand<D> makeL2BasisProjectionIntegrand( const std::vector<double>& oldDofs );

template<size_t D> MLHP_EXPORT
BasisProjectionIntegrand<D> makeTransientPoissonIntegrand( const spatial::ScalarFunction<D + 1>& capacity,
                                                           const spatial::ScalarFunction<D + 1>& diffusivity,
                                                           const spatial::ScalarFunction<D + 1>& source,
                                                           const std::vector<double>& dofs0,
                                                           std::array<double, 2> timeStep,
                                                           double theta );

// Surface integrands

template<size_t D> MLHP_EXPORT
SurfaceIntegrand<D> makeNeumannIntegrand( const spatial::ScalarFunction<D>& function );

template<size_t D> MLHP_EXPORT
SurfaceIntegrand<D> makeNeumannIntegrand( const spatial::VectorFunction<D, D>& function );

template<size_t D> MLHP_EXPORT
SurfaceIntegrand<D> makeRobinIntegrand( const spatial::ScalarFunction<D>& neumann,
                                        const spatial::ScalarFunction<D>& dirichlet );

} // mlhp

#endif // MLHP_CORE_INTEGRANDCREATORS_HPP
