# Tessellator
An evaluation engine based on TMP that supports a declarative style of fractal (i.e. tile, tiling) programming

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

---

# 🧠 Metaprogramming Playground – Usage Examples for Tessellator

This document demonstrates how to use the type-level functions defined in `meta_func.hpp` with real-world examples. Each snippet performs computations *at compile time* using C++ template metaprogramming.

---

## 🧮 Example 1: Basic Arithmetic Expression

```cpp
using ExprType = Expr<Add, Int<3>, Int<4>>;
print_result<Eval<ExprType>::result>();  // Outputs: 7
```

**What it does:** Defines a type-level expression `3 + 4`, evaluates it at compile time, and prints the result.

---

## 🔁 Example 2: Compose Metafunctions

```cpp
using Triple = Compose<DoubleFn, Add3<Int<1>>>;
print_result<Apply<Triple, Int<5>>::result>();  // (5 + 1) * 2 = 12
```

**What it does:** Composes two metafunctions:
- `Add3<Int<1>>`: adds 1 to any input
- `DoubleFn`: doubles the result

Resulting in: `(5 + 1) * 2 = 12`.

---

## 🗃️ Example 3: Map a Function Over a List

```cpp
using MyList = List<Int<1>, Int<2>, Int<3>>;
using Result = Map<DoubleFn, MyList>::result;

print_result<At<0, Result>::result>();  // 2
print_result<At<1, Result>::result>();  // 4
print_result<At<2, Result>::result>();  // 6
```

**What it does:** Applies `DoubleFn` to every element in a type-level list.

---

## 🔀 Example 4: Tessellate a Function Over a List

```cpp
struct SquareFn {
    template <typename T>
    using apply = Int<T::value * T::value>;
};

using MyList = List<Int<1>, Int<2>, Int<3>>;
using Result = Tessellate<SquareFn, MyList>::result;

print_result<At<2, Result>::result>();  // 9
```

**What it does:** Uses `Tessellate` to square each number in a type-level list.

---

## 🕵️‍♂️ Bonus: Identity Metafunction

```cpp
using Same = Identity<Int<42>>::result;
print_result<Same>();  // 42
```

**What it does:** Demonstrates a no-op type wrapper—returns the input as-is.

---
