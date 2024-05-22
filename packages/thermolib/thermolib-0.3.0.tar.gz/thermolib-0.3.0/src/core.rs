/// All core traits implemented in thermolib
mod core_traits;
mod generic_a;
mod ideal_cv;
mod tlerr;
pub use core_traits::{CalcAi, CalcAr, Flash, Prop};
pub use generic_a::{GenericA, Phase};
pub use ideal_cv::IdealCv;
pub use tlerr::TlErr;
