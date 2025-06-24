# 🎯 Tessellator

**Tessellator** is a C++ evaluation engine built using **Template Metaprogramming (TMP)**. It promotes a **declarative approach to fractal and tiling logic**, allowing complex computations to happen entirely at compile time through type-level constructs.

---

## 🧠 Key Features

- **🧮 Type-Level Arithmetic**  
  Arithmetic operations like `Add`, `Sub`, `Mul`, and `Div` are evaluated during compilation using the `Expr` and `Eval` templates.

- **🧩 Functional Metaprogramming**  
  Includes higher-order metafunctions such as `Apply`, `Compose`, and `Identity` to support functional-style programming.

- **📦 Type-Level Lists & Utilities**  
  Metaprogramming constructs like `List`, `Prepend`, `Map`, and `At` allow flexible list manipulation at the type level.

- **🌐 Tessellation Engine**  
  The `Tessellate` metafunction applies transformations across type-level structures to simulate a tile-based or recursive design system.

- **🛠️ Debugging Utilities**  
  The `print_result` runtime function bridges the compile-time realm with actual output for testing and inspection.

---

## 🧪 Example Use Cases

- Compile-time math expression evaluation  
- Procedural generation of fractal patterns  
- Learning or demonstrating advanced TMP techniques  
- Type-level explorations in generic C++ programming

---

## 🚀 Getting Started

Clone the repo:
```bash
git clone https://github.com/radubm1/Tessellator.git
```

Compile and run:
```bash
cd Tessellator
g++ -std=c++17 -o demo main.cpp
./demo
```

---

## 📖 License

[MIT License](LICENSE)

---

Happy tessellating! 🧵

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
