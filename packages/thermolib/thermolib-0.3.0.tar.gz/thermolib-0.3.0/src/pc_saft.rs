/// All module implemented for PC-SAFT equation of state.
mod alpha;
mod alpha_r;
mod disp;
mod hc;
pub use alpha::Alpha as PcSaftPure;
pub use alpha_r::AlphaR;
pub use disp::AlphaDisp;
pub use hc::AlphaHC;
const NA: f64 = 6.02214067E23;
