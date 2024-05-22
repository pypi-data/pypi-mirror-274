use super::{DgsEqu, DlsEqu, PsEqu};
use crate::core::CalcAr;
use serde::{Deserialize, Serialize};
/// No implemention for derivatives
fn no_implementation(flag: &str, d: i32) -> f64 {
    println!("no implementation for {}{}", flag, d);
    0.0
}
/// Partial derivatives of residual polynomial term
#[derive(Serialize, Deserialize, Debug)]
struct PolynomialTerm {
    n: f64,
    d: f64,
    t: f64,
}
impl PolynomialTerm {
    /// Equal to tau^(dtau) * delta(ddelta) * AlpharDtauDdelta
    fn calc_dtau_ddelta(&self, (dtau, ddelta): (i32, i32), tau: f64, delta: f64) -> f64 {
        (match dtau {
            0 => 1.0,
            1 => self.t,
            2 => (self.t - 1.0) * self.t,
            _ => no_implementation("AlpharPT::Dtau", dtau),
        }) * (match ddelta {
            0 => 1.0,
            1 => self.d,
            2 => (self.d - 1.0) * self.d,
            _ => no_implementation("AlpharPT::Ddelta", ddelta),
        }) * self.n
            * delta.powf(self.d)
            * tau.powf(self.t)
    }
}
/// Partial derivatives of residual exponential term
#[derive(Serialize, Deserialize, Debug)]
struct ExponentialTerm {
    n: f64,
    d: f64,
    t: f64,
    l: f64,
}
impl ExponentialTerm {
    /// Equal to tau^(dtau) * delta(ddelta) * AlpharDtauDdelta
    fn calc_dtau_ddelta(&self, (dtau, ddelta): (i32, i32), tau: f64, delta: f64) -> f64 {
        (match dtau {
            0 => 1.0,
            1 => self.t,
            2 => (self.t - 1.0) * self.t,
            _ => no_implementation("AlpharET::Dtau", dtau),
        }) * (match ddelta {
            0 => 1.0,
            1 => self.d - self.l * delta.powf(self.l),
            2 => {
                (self.d - 1.0) * self.d
                    - (2.0 * self.d + self.l - 1.0) * self.l * delta.powf(self.l)
                    + (self.l * delta.powf(self.l)).powi(2)
            }
            _ => no_implementation("AlpharET::Ddelta", ddelta),
        }) * self.n
            * delta.powf(self.d)
            * tau.powf(self.t)
            * (-delta.powf(self.l)).exp()
    }
}
/// Partial derivatives of residual gaussian term
#[derive(Serialize, Deserialize, Debug)]
struct GaussianTerm {
    n: f64,
    d: f64,
    t: f64,
    eta: f64,
    epsilon: f64,
    beta: f64,
    gamma: f64,
}
impl GaussianTerm {
    /// Equal to tau^(dtau) * delta(ddelta) * AlpharDtauDdelta
    fn calc_dtau_ddelta(&self, (dtau, ddelta): (i32, i32), tau: f64, delta: f64) -> f64 {
        (match dtau {
            0 => 1.0,
            1 => self.t - 2.0 * self.beta * tau * (tau - self.gamma),
            2 => {
                (self.t - 1.0) * self.t
                    - 2.0 * self.beta * tau.powi(2)
                    - 4.0 * self.t * self.beta * tau * (tau - self.gamma)
                    + 4.0 * (self.beta * tau * (tau - self.gamma)).powi(2)
            }
            _ => no_implementation("AlpharGT::Dtau", dtau),
        }) * (match ddelta {
            0 => 1.0,
            1 => self.d - 2.0 * self.eta * delta * (delta - self.epsilon),
            2 => {
                (self.d - 1.0) * self.d
                    - 2.0 * self.eta * delta.powi(2)
                    - 4.0 * self.d * self.eta * delta * (delta - self.epsilon)
                    + 4.0 * (self.eta * delta * (delta - self.epsilon)).powi(2)
            }
            _ => no_implementation("AlpharGT::Ddelta", ddelta),
        }) * self.n
            * delta.powf(self.d)
            * tau.powf(self.t)
            * (-self.eta * (delta - self.epsilon).powi(2) - self.beta * (tau - self.gamma).powi(2))
                .exp()
    }
}
#[allow(non_snake_case)]
#[derive(Serialize, Deserialize, Debug)]
pub struct ResidualTerms {
    poly_terms: Vec<PolynomialTerm>,
    exp_terms: Vec<ExponentialTerm>,
    gauss_terms: Vec<GaussianTerm>,
}
impl ResidualTerms {
    /// calculate tau^(dT) * delta^(dD) * alphar_dtau_delta
    fn calc_dtau_ddelta(&self, (dtau, ddelta): (i32, i32), tau: f64, delta: f64) -> f64 {
        self.poly_terms
            .iter()
            .map(|term| term.calc_dtau_ddelta((dtau, ddelta), tau, delta))
            .sum::<f64>()
            + self
                .exp_terms
                .iter()
                .map(|term| term.calc_dtau_ddelta((dtau, ddelta), tau, delta))
                .sum::<f64>()
            + self
                .gauss_terms
                .iter()
                .map(|term| term.calc_dtau_ddelta((dtau, ddelta), tau, delta))
                .sum::<f64>()
    }
}
/// Partial derivatives of residual helmholtz equation of state
#[allow(non_snake_case)]
#[derive(Serialize, Deserialize, Debug)]
pub struct AlphaR {
    alphar: ResidualTerms,
    ps: PsEqu,
    rhogs: DgsEqu,
    rhols: DlsEqu,
    omega: f64,
    Tc: f64,
    Dc: f64,
    Pc: f64,
    R: f64,
}
#[allow(non_snake_case)]
impl AlphaR {
    /// Calculate vapor pressure using ancillary equations
    pub fn ps(&self, T: f64) -> f64 {
        self.ps.calc(T, self.Tc, self.Pc)
    }
    /// Calculate saturated gas density using ancillary equations
    pub fn rhogs(&self, T: f64) -> f64 {
        self.rhogs.calc(T, self.Tc, self.Dc)
    }
    /// Calculate saturated liquid density using ancillary equations
    pub fn rhols(&self, T: f64) -> f64 {
        self.rhols.calc(T, self.Tc, self.Dc)
    }
    /// get acentric factor omega
    pub fn omega(&self) -> f64 {
        self.omega
    }
    /// get reducing temperature
    pub fn Tc(&self) -> f64 {
        self.Tc
    }
    /// get reducing density
    pub fn Dc(&self) -> f64 {
        self.Dc
    }
    /// get reducing pressure
    pub fn Pc(&self) -> f64 {
        self.Pc
    }
}
#[allow(non_snake_case)]
impl CalcAr for AlphaR {
    /// > fn rT0D0(&self, _T: f64, _D: f64) -> f64; Equal to =  
    /// > $$a^r\left(T,D\right)$$  
    fn rT0D0(&self, T: f64, D: f64) -> f64 {
        (self.R * T)
            * self
                .alphar
                .calc_dtau_ddelta((0, 0), self.Tc / T, D / self.Dc)
    }
    /// > fn rT0D1(&self, _T: f64, _D: f64) -> f64; Equal to =  
    /// > $$D\left(\frac{\partial a^r}{\partial D}\right)_T$$  
    fn rT0D1(&self, T: f64, D: f64) -> f64 {
        (self.R * T)
            * self
                .alphar
                .calc_dtau_ddelta((0, 1), self.Tc / T, D / self.Dc)
    }
    /// > fn rT0D2(&self, _T: f64, _D: f64) -> f64; Equal to =  
    /// > $$D^2\left(\frac{\partial^2a^r}{\partial D^2}\right)_T$$  
    fn rT0D2(&self, T: f64, D: f64) -> f64 {
        (self.R * T)
            * self
                .alphar
                .calc_dtau_ddelta((0, 2), self.Tc / T, D / self.Dc)
    }
    /// > fn rT1D0(&self, _T: f64, _D: f64) -> f64; Equal to =  
    /// > $$T\left(\frac{\partial a^r}{\partial T}\right)_D$$  
    fn rT1D0(&self, T: f64, D: f64) -> f64 {
        (self.R * T)
            * (self
                .alphar
                .calc_dtau_ddelta((0, 0), self.Tc / T, D / self.Dc)
                - self
                    .alphar
                    .calc_dtau_ddelta((1, 0), self.Tc / T, D / self.Dc))
    }
    /// > fn rT1D1(&self, _T: f64, _D: f64) -> f64; Equal to =  
    /// > $$TD\left(\frac{\partial^2a^r}{\partial T\partial D}\right)$$  
    fn rT1D1(&self, T: f64, D: f64) -> f64 {
        (self.R * T)
            * (self
                .alphar
                .calc_dtau_ddelta((0, 1), self.Tc / T, D / self.Dc)
                - self
                    .alphar
                    .calc_dtau_ddelta((1, 1), self.Tc / T, D / self.Dc))
    }
    /// > fn rT2D0(&self, _T: f64, _D: f64) -> f64; Equal to =  
    /// > $$T^2\left(\frac{\partial^2a^r}{\partial T^2}\right)_D$$  
    fn rT2D0(&self, T: f64, D: f64) -> f64 {
        (self.R * T)
            * self
                .alphar
                .calc_dtau_ddelta((2, 0), self.Tc / T, D / self.Dc)
    }
}
