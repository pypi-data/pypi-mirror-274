// This file is part of the mlhp project. License: See LICENSE

#ifndef MLHP_CORE_PARALLEL_HPP
#define MLHP_CORE_PARALLEL_HPP

#ifdef MLHP_ENABLE_OMP
#include <omp.h>
#endif

namespace mlhp::parallel
{

#ifdef MLHP_ENABLE_OMP

inline size_t getMaxNumberOfThreads( )
{
    return static_cast<size_t>( omp_get_max_threads( ) );
}

inline size_t getNumberOfThreads( )
{
    return static_cast<size_t>( omp_get_num_threads( ) );
}

inline void setNumberOfThreads( [[maybe_unused]]size_t numberOfThreads )
{
    omp_set_num_threads( static_cast<int>( numberOfThreads ) );
}

inline size_t getThreadNum( )
{
    return static_cast<size_t>( omp_get_thread_num( ) );
}

using Lock = omp_lock_t;

inline void initialize( Lock& lock )
{
    omp_init_lock( &lock );
}
inline void aquire( Lock& lock )
{
    omp_set_lock( &lock );
}

inline void release( Lock & lock )
{
    omp_unset_lock( &lock );
}

#else // ------------ No OMP --------------------

using Lock = std::uint8_t;

inline size_t getNumberOfThreads( )
{
    return 1;
}

inline size_t getMaxNumberOfThreads( )
{
    return 1;
}

inline void setNumberOfThreads( size_t ){ }
inline void initialize( Lock& ) { }
inline void aquire( Lock& ) { }
inline void release( Lock& ) { }

#endif

} // namespace mlhp::parallel

#endif // MLHP_CORE_PARALLEL_HPP
