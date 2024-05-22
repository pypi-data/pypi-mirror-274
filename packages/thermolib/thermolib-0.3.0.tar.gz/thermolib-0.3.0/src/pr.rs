/// All module implemented for pr equation of state.
mod density_pr;
mod pr_pure;
pub use density_pr::calc_density_using_pr;
pub use pr_pure::PrPure;
