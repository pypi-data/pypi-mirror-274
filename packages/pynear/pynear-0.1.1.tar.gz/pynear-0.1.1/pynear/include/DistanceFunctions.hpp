#include <vector>

#if defined(_MSC_VER)
#include <intrin.h>
#else
#include <nmmintrin.h>
#endif

#include <algorithm>
#include <cassert>
#include <cmath>
#include <immintrin.h>
#include <stdint.h>
#include <stdio.h>

using arrayd = std::vector<double>;
using arrayf = std::vector<float>;
using arrayli = std::vector<uint8_t>;
using ndarrayd = std::vector<arrayd>;
using ndarrayf = std::vector<arrayf>;
using ndarrayli = std::vector<arrayli>;

#if defined(_MSC_VER)
#define ALIGN_AS(bits) __declspec(align(bits))
#elif defined(__GNUC__)
#define ALIGN_AS(bits) __attribute__((__aligned__(bits)))
#endif

/* Hamming distances for multiples of 64 bits */
int64_t hamming_u64(const arrayli &p1, const arrayli &p2) {
    assert(p1.size() == p2.size());
    assert(p1.size() % 8 == 0);

    const uint64_t *bs1 = reinterpret_cast<const uint64_t *>(p1.data());
    const uint64_t *bs2 = reinterpret_cast<const uint64_t *>(p2.data());

    const size_t nwords = p1.size() / 8;
    size_t i;
    int64_t h = 0;
    for (i = 0; i < nwords; i++)
        h += _mm_popcnt_u64(bs1[i] ^ bs2[i]);
    return h;
}

template <size_t nbits> int64_t hamming_u64(const uint64_t *bs1, const uint64_t *bs2) {
    const size_t nwords = nbits / 64;
    size_t i;
    int64_t h = 0;
    for (i = 0; i < nwords; i++)
        h += _mm_popcnt_u64(bs1[i] ^ bs2[i]);
    return h;
}

/* Hamming distances for multiples of 32 bits */
int32_t hamming_u32(const arrayli &p1, const arrayli &p2) {
    assert(p1.size() == p2.size());
    assert(p1.size() % 4 == 0);

    const uint32_t *bs1 = reinterpret_cast<const uint32_t *>(p1.data());
    const uint32_t *bs2 = reinterpret_cast<const uint32_t *>(p2.data());

    const size_t nwords = p1.size() / 4;
    size_t i;
    int32_t h = 0;
    for (i = 0; i < nwords; i++)
        h += _mm_popcnt_u32(bs1[i] ^ bs2[i]);
    return h;
}

template <size_t nbits> int32_t hamming_u32(const uint32_t *bs1, const uint32_t *bs2) {
    const size_t nwords = nbits / 32;
    size_t i;
    int32_t h = 0;
    for (i = 0; i < nwords; i++)
        h += _mm_popcnt_u32(bs1[i] ^ bs2[i]);
    return h;
}

/* Hamming distances for multiples of 16 bits */
int16_t hamming_u16(const arrayli &p1, const arrayli &p2) {
    assert(p1.size() == p2.size());
    assert(p1.size() % 2 == 0);

    const uint16_t *bs1 = reinterpret_cast<const uint16_t *>(p1.data());
    const uint16_t *bs2 = reinterpret_cast<const uint16_t *>(p2.data());

    const size_t nwords = p1.size() / 2;
    size_t i;
    int16_t h = 0;
    for (i = 0; i < nwords; i++)
        h += _mm_popcnt_u32(bs1[i] ^ bs2[i]);
    return h;
}

template <size_t nbits> int16_t hamming_u16(const uint16_t *bs1, const uint16_t *bs2) {
    const size_t nwords = nbits / 16;
    size_t i;
    int16_t h = 0;
    for (i = 0; i < nwords; i++)
        h += _mm_popcnt_u32(bs1[i] ^ bs2[i]);
    return h;
}

/* Hamming distances for multiples of 8 bits */
int8_t hamming_u8(const arrayli &p1, const arrayli &p2) {
    assert(p1.size() == p2.size());

    const uint8_t *bs1 = p1.data();
    const uint8_t *bs2 = p2.data();

    const size_t nwords = p1.size();
    size_t i;
    int8_t h = 0;
    for (i = 0; i < nwords; i++)
        h += _mm_popcnt_u32(bs1[i] ^ bs2[i]);
    return h;
}

template <size_t nbits> int8_t hamming_u8(const uint8_t *bs1, const uint8_t *bs2) {
    const size_t nwords = nbits / 8;
    size_t i;
    int8_t h = 0;
    for (i = 0; i < nwords; i++)
        h += _mm_popcnt_u32(bs1[i] ^ bs2[i]);
    return h;
}

inline double sum4(__m256d v) {
    __m128d vlow = _mm256_castpd256_pd128(v);
    __m128d vhigh = _mm256_extractf128_pd(v, 1); // high 128
    vlow = _mm_add_pd(vlow, vhigh);              // reduce down to 128

    __m128d high64 = _mm_unpackhi_pd(vlow, vlow);
    return _mm_cvtsd_f64(_mm_add_sd(vlow, high64)); // reduce to scalar
}

/* specialized (optimized) functions */
template <> int8_t hamming_u8<8>(const uint8_t *pa, const uint8_t *pb) { return _mm_popcnt_u32(pa[0] ^ pb[0]); }

template <> int16_t hamming_u16<16>(const uint16_t *pa, const uint16_t *pb) { return _mm_popcnt_u32(pa[0] ^ pb[0]); }

template <> int32_t hamming_u32<32>(const uint32_t *pa, const uint32_t *pb) { return _mm_popcnt_u32(pa[0] ^ pb[0]); }

template <> int64_t hamming_u64<64>(const uint64_t *pa, const uint64_t *pb) { return _mm_popcnt_u64(pa[0] ^ pb[0]); }

template <> int64_t hamming_u64<128>(const uint64_t *pa, const uint64_t *pb) {

    __m256d result = _mm256_set_pd(_mm_popcnt_u64(pa[0] ^ pb[0]), _mm_popcnt_u64(pa[1] ^ pb[1]), 0, 0);
    return (int64_t)sum4(result);
}

template <> int64_t hamming_u64<256>(const uint64_t *pa, const uint64_t *pb) {

    __m256d result =
        _mm256_set_pd(_mm_popcnt_u64(pa[0] ^ pb[0]), _mm_popcnt_u64(pa[1] ^ pb[1]), _mm_popcnt_u64(pa[2] ^ pb[2]), _mm_popcnt_u64(pa[3] ^ pb[3]));
    return (int64_t)sum4(result);
}

template <> int64_t hamming_u64<512>(const uint64_t *pa, const uint64_t *pb) {
    return _mm_popcnt_u64(pa[0] ^ pb[0]) + _mm_popcnt_u64(pa[1] ^ pb[1]) + _mm_popcnt_u64(pa[2] ^ pb[2]) + _mm_popcnt_u64(pa[3] ^ pb[3]) +
           _mm_popcnt_u64(pa[4] ^ pb[4]) + _mm_popcnt_u64(pa[5] ^ pb[5]) + _mm_popcnt_u64(pa[6] ^ pb[6]) + _mm_popcnt_u64(pa[7] ^ pb[7]);
}

inline float sum8(__m256 x) {
    // hiQuad = ( x7, x6, x5, x4 )
    const __m128 hiQuad = _mm256_extractf128_ps(x, 1);
    // loQuad = ( x3, x2, x1, x0 )
    const __m128 loQuad = _mm256_castps256_ps128(x);
    // sumQuad = ( x3 + x7, x2 + x6, x1 + x5, x0 + x4 )
    const __m128 sumQuad = _mm_add_ps(loQuad, hiQuad);
    // loDual = ( -, -, x1 + x5, x0 + x4 )
    const __m128 loDual = sumQuad;
    // hiDual = ( -, -, x3 + x7, x2 + x6 )
    const __m128 hiDual = _mm_movehl_ps(sumQuad, sumQuad);
    // sumDual = ( -, -, x1 + x3 + x5 + x7, x0 + x2 + x4 + x6 )
    const __m128 sumDual = _mm_add_ps(loDual, hiDual);
    // lo = ( -, -, -, x0 + x2 + x4 + x6 )
    const __m128 lo = sumDual;
    // hi = ( -, -, -, x1 + x3 + x5 + x7 )
    const __m128 hi = _mm_shuffle_ps(sumDual, sumDual, 0x1);
    // sum = ( -, -, -, x0 + x1 + x2 + x3 + x4 + x5 + x6 + x7 )
    const __m128 sum = _mm_add_ss(lo, hi);
    return _mm_cvtss_f32(sum);
}

double dist_l2_d_avx2(const arrayd &p1, const arrayd &p2) {

    unsigned int i = p1.size() / 4;
    __m256d result = _mm256_set_pd(0, 0, 0, 0);

    while (i--) {
        __m256d x = _mm256_load_pd(&p1[4 * i]);
        __m256d y = _mm256_load_pd(&p2[4 * i]);

        /* Compute the difference between the two vectors */
        __m256d diff = _mm256_sub_pd(x, y);

        __m256d temp = _mm256_mul_pd(diff, diff);
        result = _mm256_add_pd(temp, result);
        /* Multipl_mm256_mul_psy and add to result */
        /* result = _mm256_fmadd_pd(diff, diff, result); */
    }

    double out = sum4(result);
    return std::sqrt(out);
}

// reads 0 <= d < 4 floats as __m128
static inline __m128 masked_read(int d, const float *x) {
    assert(0 <= d && d < 4);
    ALIGN_AS(16) float buf[4] = {0, 0, 0, 0};
    switch (d) {
    case 3:
        buf[2] = x[2];
    case 2:
        buf[1] = x[1];
    case 1:
        buf[0] = x[0];
    }
    return _mm_load_ps(buf);
    // cannot use AVX2 _mm_mask_set1_epi32
}

float dist_l2_f_avx2(const arrayf &p1, const arrayf &p2) {
    unsigned int d = p1.size();
    __m256 msum1 = _mm256_setzero_ps();

    const float *x = &(p1[0]);
    const float *y = &(p2[0]);

    while (d >= 8) {
        __m256 mx = _mm256_loadu_ps(x);
        x += 8;
        __m256 my = _mm256_loadu_ps(y);
        y += 8;
        const __m256 a_m_b1 = _mm256_sub_ps(mx, my);
        msum1 = _mm256_add_ps(msum1, _mm256_mul_ps(a_m_b1, a_m_b1));
        d -= 8;
    }

    __m128 msum2 = _mm256_extractf128_ps(msum1, 1);
    msum2 = _mm_add_ps(msum2, _mm256_extractf128_ps(msum1, 0));

    if (d >= 4) {
        __m128 mx = _mm_loadu_ps(x);
        x += 4;
        __m128 my = _mm_loadu_ps(y);
        y += 4;
        const __m128 a_m_b1 = _mm_sub_ps(mx, my);
        msum2 = _mm_add_ps(msum2, _mm_mul_ps(a_m_b1, a_m_b1));
        d -= 4;
    }

    if (d > 0) {
        __m128 mx = masked_read(d, x);
        __m128 my = masked_read(d, y);
        const __m128 a_m_b1 = _mm_sub_ps(mx, my);
        msum2 = _mm_add_ps(msum2, _mm_mul_ps(a_m_b1, a_m_b1));
    }

    msum2 = _mm_hadd_ps(msum2, msum2);
    msum2 = _mm_hadd_ps(msum2, msum2);
    float result = _mm_cvtss_f32(msum2);
    return std::sqrt(result);
}

double dist_l2_d(const arrayd &p1, const arrayd &p2) {

    double result = 0;
    size_t i = p1.size();
    while (i--) {
        double d = (p1[i] - p2[i]);
        result += d * d;
    }

    return std::sqrt(result);
}

float dist_l2_f(const arrayf &p1, const arrayf &p2) {

    float result = 0.;
    size_t i = p1.size();
    while (i--) {
        float d = (p1[i] - p2[i]);
        result += d * d;
    }

    return std::sqrt(result);
}

float dist_l1_f(const arrayf &p1, const arrayf &p2) {
    /* L1 metric, also called Manhattan or taxicab metric */

    float result = 0.;
    size_t i = p1.size();
    while (i--) {
        result += std::fabs(p1[i] - p2[i]);
    }

    return result;
}

float dist_l1_f_avx2(const arrayf &p1, const arrayf &p2) {
    /* SIMD L1 metric, also called Manhattan or taxicab metric */

    const float *vec1 = &(p1[0]);
    const float *vec2 = &(p2[0]);
    size_t size = p1.size();

    const size_t blocksize = 8;
    size_t i = 0;

    __m256 sum = _mm256_setzero_ps();

    for (; i + blocksize <= size; i += blocksize) {
        __m256 v1 = _mm256_loadu_ps(&vec1[i]);
        __m256 v2 = _mm256_loadu_ps(&vec2[i]);

        __m256 diff = _mm256_sub_ps(v1, v2);
        sum = _mm256_add_ps(sum, _mm256_and_ps(diff, _mm256_castsi256_ps(_mm256_set1_epi32(0x7FFFFFFF))));
    }

    ALIGN_AS(32) float result[8];
    _mm256_store_ps(result, sum);

    float total_sum = 0.;
    for (int j = 0; j < 8; ++j) {
        total_sum += result[j];
    }

    // Calculate the remaining elements
    for (; i < size; ++i) {
        total_sum += std::fabs(vec1[i] - vec2[i]);
    }

    return total_sum;
}

float dist_chebyshev_f(const arrayf &p1, const arrayf &p2) {
    /* Chebyshev distance metric, also called maximum metric or L_inf metric */

    float result = 0.;
    size_t i = p1.size();
    while (i--) {
        float distance = std::fabs(p1[i] - p2[i]);
        if (distance > result) {
            result = distance;
        }
    }

    return result;
}

float dist_chebyshev_f_avx2(const arrayf &p1, const arrayf &p2) {
    /* SIMD Chebyshev distance metric, also called maximum metric or L_inf metric */

    const float *vec1 = &(p1[0]);
    const float *vec2 = &(p2[0]);
    size_t size = p1.size();

    const size_t blocksize = 8;
    size_t i = 0;

    __m256 max_diff = _mm256_setzero_ps();

    for (; i + blocksize <= size; i += blocksize) {
        __m256 v1 = _mm256_loadu_ps(&vec1[i]);
        __m256 v2 = _mm256_loadu_ps(&vec2[i]);
        __m256 diff = _mm256_sub_ps(v1, v2);
        diff = _mm256_and_ps(diff, _mm256_castsi256_ps(_mm256_set1_epi32(0x7FFFFFFF))); // Absolute value
        max_diff = _mm256_max_ps(max_diff, diff);
    }

    ALIGN_AS(32) float result[8];
    _mm256_store_ps(result, max_diff);

    float max_distance = result[0];
    for (int i = 1; i < 8; ++i) {
        max_distance = std::max(max_distance, result[i]);
    }

    // Calculate the remaining elements
    for (; i < size; ++i) {
        float diff = std::fabs(vec1[i] - vec2[i]);
        max_distance = std::max(max_distance, diff);
    }

    return max_distance;
}

int64_t dist_hamming(const arrayli &p1, const arrayli &p2) {
    size_t size = p1.size();

    if (size % 8 == 0) {
        return hamming_u64(p1, p2);
    } else if (size % 4 == 0) {
        return static_cast<int64_t>(hamming_u32(p1, p2));
    } else if (size % 2 == 0) {
        return static_cast<int64_t>(hamming_u16(p1, p2));
    } else {
        return static_cast<int64_t>(hamming_u8(p1, p2));
    }
}

inline int64_t dist_hamming_512(const arrayli &p1, const arrayli &p2) {

    return hamming_u64<512>(reinterpret_cast<const uint64_t *>(&p1[0]), reinterpret_cast<const uint64_t *>(&p2[0]));
}

inline int64_t dist_hamming_256(const arrayli &p1, const arrayli &p2) {

    return hamming_u64<256>(reinterpret_cast<const uint64_t *>(&p1[0]), reinterpret_cast<const uint64_t *>(&p2[0]));
}

inline int64_t dist_hamming_128(const arrayli &p1, const arrayli &p2) {

    return hamming_u64<128>(reinterpret_cast<const uint64_t *>(&p1[0]), reinterpret_cast<const uint64_t *>(&p2[0]));
}

inline int64_t dist_hamming_64(const arrayli &p1, const arrayli &p2) {
    return hamming_u64<64>(reinterpret_cast<const uint64_t *>(&p1[0]), reinterpret_cast<const uint64_t *>(&p2[0]));
}

inline int64_t dist_hamming_32(const arrayli &p1, const arrayli &p2) {

    return static_cast<int64_t>(hamming_u32<32>(reinterpret_cast<const uint32_t *>(&p1[0]), reinterpret_cast<const uint32_t *>(&p2[0])));
}

inline int64_t dist_hamming_16(const arrayli &p1, const arrayli &p2) {

    return static_cast<int64_t>(hamming_u16<16>(reinterpret_cast<const uint16_t *>(&p1[0]), reinterpret_cast<const uint16_t *>(&p2[0])));
}

inline int64_t dist_hamming_8(const arrayli &p1, const arrayli &p2) {

    return static_cast<int64_t>(hamming_u8<8>(reinterpret_cast<const uint8_t *>(&p1[0]), reinterpret_cast<const uint8_t *>(&p2[0])));
}
