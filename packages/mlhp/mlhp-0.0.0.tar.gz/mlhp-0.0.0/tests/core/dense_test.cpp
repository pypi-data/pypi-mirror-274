// This file is part of the mlhp project. License: See LICENSE

#include "tests/core/core_test.hpp"

#include "mlhp/core/dense.hpp"
#include "mlhp/core/compilermacros.hpp"
#include "mlhp/core/memory.hpp"

#include<array>

namespace mlhp
{
namespace linalg
{
//
//TEST_CASE( "outerProduct_1D_test" )
//{
//    size_t paddedSize = MLHP_SIMD_ALIGNMENT / sizeof( double );
//
//    memory::AlignedVector<double> N { 1.0, 2.0, 3.0 };
//    memory::AlignedVector<double> target( 3 * paddedSize, -0.6 );
//
//    CHECK_NOTHROW( dense::outerProductFull<1>( target.data( ), N.data( ), 2.3, 3 ) );
//
//    for( size_t i = 0; i < 3; ++i )
//    {
//        for( size_t j = 0; j < 3; ++j )
//        {
//            CHECK( target[i * paddedSize + j] == Approx( N[i] * N[j] * 2.3 - 0.6 ).epsilon( 1e-12 ) );
//        }
//    }
//}
//
//TEST_CASE( "outerProduct_2D_test" )
//{
//    size_t paddedSize = MLHP_SIMD_ALIGNMENT / sizeof( double );
//
//    memory::AlignedVector<double> N ( 2 * paddedSize, 0.0 );
//    memory::AlignedVector<double> target( 3 * paddedSize, -0.6 );
//
//    N[0] = 1.0;
//    N[1] = 2.0;
//    N[2] = 3.0;
//    N[paddedSize + 0] = 4.0;
//    N[paddedSize + 1] = 5.0;
//    N[paddedSize + 2] = 6.0;
//
//    CHECK_NOTHROW( outerProductFull<2>( target.data( ), N.data( ), 2.3, 3 ) );
//
//    for( size_t i = 0; i < 3; ++i )
//    {
//        for( size_t j = 0; j < 3; ++j )
//        {
//            double expectedValue = ( N[i] * N[j] + N[paddedSize + i] * N[paddedSize + j] ) * 2.3 - 0.6;
//
//            CHECK( target[i * paddedSize + j] == Approx( expectedValue ).epsilon( 1e-12 ) );
//        }
//    }
//}

TEST_CASE( "lu_test" )
{

    // -------------------- test lu ----------------------

    double M[] = 
    {
        -6.57236887,  0.84564944, -1.02177673,  3.75118371,  2.67678544,
         9.64342431, -1.2257033,   4.58716922, -5.83018145, -7.51428046,
         5.68716742,  2.04974341,  0.10133382, -9.21934916,  9.65478781,
        -9.0823581,   6.64997405, -8.45984082, -9.00872702, -2.79864918,
        -8.70517483,  6.64140389, -9.14154383,  1.50739727,  5.46489685 
    };

    size_t P[5] = { };

    CHECK_NOTHROW( lu( M, P, 5 ) );

    double expectedLU[] = 
    {  
        9.64342430e+00, -1.22570330e+00,  4.58716921e+00, -5.83018145e+00, -7.51428045e+00, // LU(0, j)
       -9.02705776e-01,  5.53495443e+00, -5.00067967e+00, -3.75554119e+00, -1.31828751e+00, // LU(1, j)
       -6.81538907e-01,  1.85818261e-03,  2.11384974e+00, -2.15333300e-01, -2.44203943e+00, // LU(2, j)
       -9.41818778e-01,  9.92886884e-01,  3.90543631e-01, -1.06867767e+01, -7.61310628e+00, // LU(3, j)
        5.89745637e-01,  5.00924916e-01, -4.68170311e-02,  3.65859817e-01,  1.74176656e+01, // LU(4, j)
    };

    size_t expectedP[] = { 1, 4, 0, 3, 2 };

    for( size_t i = 0; i < 5; ++i )
    {
        CHECK( P[i] == expectedP[i] );

        for( size_t j = 0; j < 5; ++j )
        {
            CHECK( M[i * 5 + j] == Approx( expectedLU[i * 5 + j] )
                   .epsilon( 1e-7 ).margin( 1e-7 ) );
        }
    }

    // --------------- test substitution -----------------

    double rhs[] = { -5.73507895,  6.63643545,  3.95315262, -0.00832055,  0.47981328 };

    double solution[5] = { };

    CHECK_NOTHROW( luSubstitute( expectedLU, expectedP, 5, rhs, solution ) );

    double expectedSolution[] =
    {
        1.04182070e+00,  4.82824712e-01, -7.91224906e-01,  1.10071363e-01, -1.93329855e-01
    };

    for( size_t i = 0; i < 5; ++i )
    {
        CHECK( solution[i] == Approx( expectedSolution[i] ).epsilon( 1e-8 ) );
    }


    // ----------------- test inverse --------------------

    double inverse[25] = { };

    CHECK_NOTHROW( luInvert( expectedLU, expectedP, 5, inverse ) );

    double expectedInverse[] =
    {
        -1.47601385e-01,  2.57481231e-02, -4.20978210e-03, -5.96623725e-02,  8.45846450e-02,
         4.63548835e-01,  4.30408775e-01,  4.20831567e-02, -8.74995005e-02,  2.45605207e-01,
         4.88585129e-01,  2.65933738e-01,  6.21603209e-02, -3.22741026e-02, -1.00033493e-06,
         2.87857519e-02,  5.86061643e-02, -4.09001788e-02, -7.86098520e-02,  9.84851204e-02,
         1.08913134e-02, -5.33723617e-02,  5.74129749e-02, -2.10051005e-02, -7.92413881e-03
    };

    for( size_t i = 0; i < 5; ++i )
    {
        for( size_t j = 0; j < 5; ++j )
        {
            CHECK( inverse[i * 5 + j] == Approx( expectedInverse[i * 5 + j] )
                   .epsilon( 2e-9 ).margin( 2e-9 ) );
        }
    }
}

TEST_CASE( "lu_test2" )
{
    auto J = std::array { 0.0, 0.02, 0.02, 0.0 };
    auto P = std::array<size_t, 2> { };

    lu( J.data( ), P.data( ), 2 );

    auto r = std::array { 4.2, 7.4 };
    auto x = std::array<double, 2> { };

    luSubstitute( J.data( ), P.data( ), 2, r.data( ), x.data( ) );

    CHECK( x[0] == Approx( 370.0 ).epsilon( 1e-8 ) );
    CHECK( x[1] == Approx( 210.0 ).epsilon( 1e-8 ) );
}

} // namespace linalg
} // namespace mlhp
