#include "meta_func.hpp"

using Program = Expr<Mul,
                  Expr<Add, Int<2>, Int<3>>,  // (2 + 3)
                  Int<4>>;                    // * 4

// Partially apply Add3<Int<5>> => waiting for second argument
using PartialAdd = Add3<Int<5>>;

// Apply second argument
//using Result = Apply<PartialAdd, Int<7>>::result;  // Int<12>

// Apply second argument
using Result = Apply<DoubleFn, Int<7>>::result;  // OK

using Input = List<Int<1>, Int<2>, Int<3>>;
using AddThree = Add3<Int<3>>;  // if you’re currying
using Mapped = Map<DoubleFn, Input>::result;  // [4, 5, 6]

using Output = typename Tessellate<DoubleFn, Input>::result;
using FirstElement = typename At<0, Output>::result;


int main() {
    //print_result<Eval<Program>::result>();  // Outputs: 20
    //print_result<Eval<Result>::result>();  // Outputs: 14
    //print_result<std::tuple_element_t<0, Mapped>>();

    print_result<FirstElement>();  // Should print 2


}
