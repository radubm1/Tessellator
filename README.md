# Tessellator
An evaluation engine based on TMP that supports a declarative style of fractal (i.e. tile, tiling) programming

Absolutely, Radu! Here's an annotated Markdown file that explains each part of your `meta_func.hpp` header—great example of type-level programming in C++:

---

# `meta_func.hpp` – Annotated

A header for **type-level computations** in C++ using template metaprogramming.

## Includes and Pragma

```cpp
#pragma once
#include <type_traits>
#include <iostream>
```
- Ensures single inclusion.
- Brings in traits for compile-time type info and `std::cout` for debugging.

## Type-Level Integers

```cpp
template <int N>
struct Int {
    static constexpr int value = N;
};
```
- Wraps an integer in a type to allow compile-time arithmetic.

## Operators and Expressions

```cpp
struct Add; struct Sub; struct Mul; struct Div;

template <typename Op, typename LHS, typename RHS>
struct Expr;
```
- Defines placeholders for arithmetic and a generic binary expression wrapper.

## Evaluation Engine

```cpp
template <typename T> struct Eval;

template <int N>
struct Eval<Int<N>> {
    using result = Int<N>;
};
```
- Specializes `Eval` to reduce an `Expr` to an `Int`.

Each arithmetic operation is implemented as a specialization:

```cpp
template <typename LHS, typename RHS>
struct Eval<Expr<Add, LHS, RHS>> {
    using result = Int<Eval<LHS>::result::value + Eval<RHS>::result::value>;
};
```
_(And similar for `Sub`, `Mul`, `Div`.)_

## Functional Metaprogramming

```cpp
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
```
- Enables higher-order metafunction application and composition.

Example metafunctions:

```cpp
template <typename T>
struct Add3 {
    template <typename U>
    using apply = Int<T::value + U::value>;
};

struct DoubleFn {
    template <typename T>
    using apply = Int<T::value * 2>;
};
```

## Type-Level List & Utilities

```cpp
template <typename... Ts> struct List {};
```
- A type-level variadic list.

### Map

```cpp
template <typename F, typename ListT> struct Map;
```
- Applies a function `F` to every element in a `List`.

### Prepend

```cpp
template <typename T, typename... Ts>
struct Prepend<T, List<Ts...>> {
    using type = List<T, Ts...>;
};
```

### Tessellate

```cpp
template <typename F, typename ListT> struct Tessellate;
```
- Like `Map`, but assumes `F` is a metafunction with `template <typename>` syntax.

### At

```cpp
template <std::size_t Index, typename ListT> struct At;
```
- Retrieves the element at index `Index` in a type-level list.

## Debugging

```cpp
template <typename T>
void print_result() {
    std::cout << T::value << '\n';
}
```
- Helps observe compile-time evaluated `Int<N>` values at runtime.

---

If you'd like, I can also help build a sample use case or test suite for this. Want to explore that next?
