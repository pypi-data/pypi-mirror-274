#include <iostream>

#include "pcsaft.h"
int main() {
  add_args args;
  args.m.push_back(1.6069);  // parameters for ethane
  args.s.push_back(3.5206);  // parameters for ethane
  args.e.push_back(191.42);  // parameters for ethane
  double t = 300, rho = 1000;
  double ares = pcsaft_ares_cpp(t, rho, {1}, args);
  printf("ares=%.12f\n", ares);
  printf("Hello C++ World from VS Code\n");
}
