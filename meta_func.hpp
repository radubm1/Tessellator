// meta_func.hpp
#pragma once
#include <type_traits>
#include <iostream>

// === Type-level Ints ===
template <int N>
struct Int {
    static constexpr int value = N;
};

// === Basic Arithmetic Operators ===
struct Add;
struct Sub;
struct Mul;
struct Div;

template <typename Op, typename LHS, typename RHS>
struct Expr;

// === Evaluation Engine ===
template <typename T>
struct Eval;

template <int N>
struct Eval<Int<N>> {
    using result = Int<N>;
};

template <typename LHS, typename RHS>
struct Eval<Expr<Add, LHS, RHS>> {
    using result = Int<Eval<LHS>::result::value + Eval<RHS>::result::value>;
};

template <typename LHS, typename RHS>
struct Eval<Expr<Sub, LHS, RHS>> {
    using result = Int<Eval<LHS>::result::value - Eval<RHS>::result::value>;
};

template <typename LHS, typename RHS>
struct Eval<Expr<Mul, LHS, RHS>> {
    using result = Int<Eval<LHS>::result::value * Eval<RHS>::result::value>;
};

template <typename LHS, typename RHS>
struct Eval<Expr<Div, LHS, RHS>> {
    using result = Int<Eval<LHS>::result::value / Eval<RHS>::result::value>;
};

template <typename T>
struct Identity {
    using result = T;
};

template <typename F, typename Arg>
struct Apply {
    using result = typename F::template apply<Arg>;
};

template <typename F, typename G>
struct Compose {
    template <typename X>
    using apply = typename F::template apply<typename G::template apply<X>>;
};

template <typename T>
struct Add3 {
    template <typename U>
    using apply = Int<T::value + U::value>;
};

struct DoubleFn {
    template <typename T>
    using apply = Int<T::value * 2>;
};

template <typename... Ts>
struct List {};

template <typename F, typename ListT>
struct Map;

template <typename F>
struct Map<F, List<>> {
    using result = List<>;
};

template <typename T, typename ListT>
struct Prepend;

template <typename T, typename... Ts>
struct Prepend<T, List<Ts...>> {
    using type = List<T, Ts...>;
};

template <typename F, typename Head, typename... Tail>
struct Map<F, List<Head, Tail...>> {
    using result = typename Prepend<
        typename Apply<F, Head>::result,
        typename Map<F, List<Tail...>>::result
    >::type;
};

template <typename F, typename ListT>
struct Tessellate;

template <typename F>
struct Tessellate<F, List<>> {
    using result = List<>;
};

template <typename F, typename Head, typename... Tail>
struct Tessellate<F, List<Head, Tail...>> {
    using result = typename Prepend<
        typename F::template apply<Head>,
        typename Tessellate<F, List<Tail...>>::result
    >::type;
};

template <std::size_t Index, typename ListT>
struct At;

template <std::size_t Index, typename Head, typename... Tail>
struct At<Index, List<Head, Tail...>> {
    using result = typename At<Index - 1, List<Tail...>>::result;
};

template <typename Head, typename... Tail>
struct At<0, List<Head, Tail...>> {
    using result = Head;
};

// === Debugging ===
template <typename T>
void print_result() {
    std::cout << T::value << '\n';
}
