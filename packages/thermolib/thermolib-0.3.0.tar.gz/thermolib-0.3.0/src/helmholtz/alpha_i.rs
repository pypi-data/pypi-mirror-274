use crate::core::CalcAi;
use serde::{Deserialize, Serialize};
/// Partial derivatives of ideal polynomial term
#[derive(Serialize, Deserialize, Debug)]
struct PolynomialTerm {
    is_alpha: bool,
    a: f64,
    t: f64,
}
#[allow(non_snake_case)]
impl PolynomialTerm {
    /// > Equal to  
    /// > $$\alpha^0\left(\tau,\delta\right)$$  
    fn calc_0(&self, T: f64, Tr: f64) -> f64 {
        if self.is_alpha {
            -self.a / (Tr / T).powf(self.t)
        } else {
            -self.a * T.powf(self.t) / self.t / (self.t + 1.0)
        }
    }
    /// > Equal to  
    /// > $$\tau\left(\frac{\partial\alpha^0}{\partial\tau}\right)_\delta$$  
    fn calc_1(&self, T: f64, Tr: f64) -> f64 {
        if self.is_alpha {
            self.a * self.t / (Tr / T).powf(self.t)
        } else {
            self.a * T.powf(self.t) / (self.t + 1.0)
        }
    }
    /// > Equal to  
    /// > $$\tau^2\left(\frac{\partial^2\alpha^0}{\partial\tau^2}\right)_\delta$$  
    fn calc_2(&self, T: f64, Tr: f64) -> f64 {
        if self.is_alpha {
            -self.a * self.t * (self.t + 1.0) / (Tr / T).powf(self.t)
        } else {
            -self.a * T.powf(self.t)
        }
    }
}
/// Partial derivatives of ideal plank einstein term
#[derive(Serialize, Deserialize, Debug)]
struct PlankEinsteinTerm {
    is_alpha: bool,
    v: f64,
    b: f64,
}
#[allow(non_snake_case)]
impl PlankEinsteinTerm {
    /// > Equal to  
    /// > $$\alpha^0\left(\tau,\delta\right)$$  
    fn calc_0(&self, T: f64, Tr: f64) -> f64 {
        let bitau = if self.is_alpha { self.b } else { self.b / Tr } * Tr / T;
        let exp_bitau = (-bitau).exp();
        self.v * (1.0 - exp_bitau).ln()
    }
    /// > Equal to  
    /// > $$\tau\left(\frac{\partial\alpha^0}{\partial\tau}\right)_\delta$$  
    fn calc_1(&self, T: f64, Tr: f64) -> f64 {
        let bitau = if self.is_alpha { self.b } else { self.b / Tr } * Tr / T;
        let exp_bitau = (-bitau).exp();
        self.v * exp_bitau * bitau / (1.0 - exp_bitau)
    }
    /// > Equal to  
    /// > $$\tau^2\left(\frac{\partial^2\alpha^0}{\partial\tau^2}\right)_\delta$$  
    fn calc_2(&self, T: f64, Tr: f64) -> f64 {
        let bitau = if self.is_alpha { self.b } else { self.b / Tr } * Tr / T;
        let exp_bitau = (-bitau).exp();
        -self.v * exp_bitau * (bitau / (1.0 - exp_bitau)).powi(2)
    }
}
/// Partial derivatives of ideal helmholtz equation of state
#[allow(non_snake_case)]
#[derive(Serialize, Deserialize, Debug)]
pub struct AlphaI {
    a_1: f64,
    a_tau: f64,
    a_lntau: f64,
    poly_terms: Vec<PolynomialTerm>,
    pe_terms: Vec<PlankEinsteinTerm>,
    Tc: f64,
    Dc: f64,
    R: f64,
}
#[allow(non_snake_case)]
impl AlphaI {
    /// > Equal to  
    /// > $$\alpha^0\left(\tau,\delta\right)-\ln D$$  
    fn calc_alpha0(&self, T: f64) -> f64 {
        self.a_1 + self.a_tau * (self.Tc / T) + self.a_lntau * (self.Tc / T).ln() - self.Dc.ln()
            + self
                .poly_terms
                .iter()
                .map(|term| term.calc_0(T, self.Tc))
                .sum::<f64>()
            + self
                .pe_terms
                .iter()
                .map(|term| term.calc_0(T, self.Tc))
                .sum::<f64>()
    }
}
#[allow(non_snake_case)]
impl CalcAi for AlphaI {
    /// > fn iT0(&self, _T: f64) -> f64; Equal to =  
    /// > $$a^i\left(T,D\right)-RT\ln D$$  
    fn iT0(&self, T: f64) -> f64 {
        self.R * T * self.calc_alpha0(T)
    }
    /// > fn iT1(&self, _T: f64) -> f64; Equal to =  
    /// > $$T\left(\frac{\partial a^i}{\partial T}\right)_D-RT\ln D$$  
    fn iT1(&self, T: f64) -> f64 {
        let tau1_alpha0_dtau1 = self.a_tau * (self.Tc / T)
            + self.a_lntau
            + self
                .poly_terms
                .iter()
                .map(|term| term.calc_1(T, self.Tc))
                .sum::<f64>()
            + self
                .pe_terms
                .iter()
                .map(|term| term.calc_1(T, self.Tc))
                .sum::<f64>();
        self.R * T * (self.calc_alpha0(T) - tau1_alpha0_dtau1)
    }
    /// > fn iT2(&self, _T: f64) -> f64; Equal to =  
    /// > $$T^2\left(\frac{\partial^2a^i}{\partial T^2}\right)_D$$  
    fn iT2(&self, T: f64) -> f64 {
        let tau2_alpha0_dtau2 = -self.a_lntau
            + self
                .poly_terms
                .iter()
                .map(|term| term.calc_2(T, self.Tc))
                .sum::<f64>()
            + self
                .pe_terms
                .iter()
                .map(|term| term.calc_2(T, self.Tc))
                .sum::<f64>();
        self.R * T * tau2_alpha0_dtau2
    }
}
