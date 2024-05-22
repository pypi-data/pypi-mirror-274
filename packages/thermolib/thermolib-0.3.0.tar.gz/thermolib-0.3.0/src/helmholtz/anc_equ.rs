use serde::{Deserialize, Serialize};
/// Ancillary Equations
/// + Vapor Pressure Equation
/// + Saturated Gas Density Equation
/// + Saturated Liquid Density Equation
#[derive(Serialize, Deserialize, Debug)]
struct AncEquTerm {
    n: f64, // coefficients
    t: f64, // exponents
}
impl AncEquTerm {
    fn calc(&self, theta: f64) -> f64 {
        self.n * theta.powf(self.t)
    }
}
#[derive(Serialize, Deserialize, Debug)]
pub struct PsEqu {
    flag: i32,
    terms: Vec<AncEquTerm>,
}
impl PsEqu {
    #[allow(non_snake_case)]
    pub fn calc(&self, T: f64, Tr: f64, Pr: f64) -> f64 {
        let theta = 1.0 - T / Tr;
        let mut p_pr = 0.0;
        Pr * (match self.flag {
            1 => {
                for i in self.terms.iter() {
                    p_pr += i.calc(theta);
                }
                (p_pr / theta).exp()
            }
            _ => {
                println!("no flag={} in vapor_pressure_equation", self.flag);
                1.0
            }
        })
    }
}
#[derive(Serialize, Deserialize, Debug)]
pub struct DgsEqu {
    flag: i32,
    terms: Vec<AncEquTerm>,
}
impl DgsEqu {
    #[allow(non_snake_case)]
    pub fn calc(&self, T: f64, Tr: f64, Dr: f64) -> f64 {
        let theta = 1.0 - T / Tr;
        let mut rho_rhor = 0.0;
        Dr * (match self.flag {
            1 => {
                for i in self.terms.iter() {
                    rho_rhor += i.calc(theta);
                }
                rho_rhor.exp()
            }
            2 => {
                for i in self.terms.iter() {
                    rho_rhor += i.calc(theta / 3.0);
                }
                rho_rhor.exp()
            }
            _ => {
                println!("no flag={} in saturated_gas_density_equation", self.flag);
                1.0
            }
        })
    }
}
#[derive(Serialize, Deserialize, Debug)]
pub struct DlsEqu {
    flag: i32,
    terms: Vec<AncEquTerm>,
}
impl DlsEqu {
    #[allow(non_snake_case)]
    pub fn calc(&self, T: f64, Tr: f64, Dr: f64) -> f64 {
        let theta = 1.0 - T / Tr;
        let mut rho_rhor = 0.0;
        Dr * (match self.flag {
            1 => {
                for i in self.terms.iter() {
                    rho_rhor += i.calc(theta);
                }
                rho_rhor + 1.0
            }
            2 => {
                for i in self.terms.iter() {
                    rho_rhor += i.calc(theta / 3.0);
                }
                rho_rhor + 1.0
            }
            3 => {
                for i in self.terms.iter() {
                    rho_rhor += i.calc(theta / 3.0);
                }
                rho_rhor.exp()
            }
            _ => {
                println!("no flag={} in saturated_liquid_density_equation", self.flag);
                1.0
            }
        })
    }
}
