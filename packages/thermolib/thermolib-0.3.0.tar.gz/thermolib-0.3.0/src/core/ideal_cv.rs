use super::CalcAi;
/// isochoric heat capacity of ideal gas
/// used to calculate ideal helmholtz energy
pub struct IdealCv {}
#[allow(non_snake_case)]
impl CalcAi for IdealCv {
    /// > fn iT0(&self, _T: f64) -> f64; Equal to =  
    /// > $$a^i\left(T,D\right)-RT\ln D$$  
    fn iT0(&self, _T: f64) -> f64 {
        0.0
    }
    /// > fn iT1(&self, _T: f64) -> f64; Equal to =  
    /// > $$T\left(\frac{\partial a^i}{\partial T}\right)_D-RT\ln D$$  
    fn iT1(&self, _T: f64) -> f64 {
        0.0
    }
    /// > fn iT2(&self, _T: f64) -> f64; Equal to =  
    /// > $$T^2\left(\frac{\partial^2a^i}{\partial T^2}\right)_D$$  
    fn iT2(&self, _T: f64) -> f64 {
        0.0
    }
}
