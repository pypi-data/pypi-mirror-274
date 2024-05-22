use super::{AlphaI, AlphaR};
use crate::core::{CalcAr, GenericA, Phase, Prop, TlErr};
use crate::pr::calc_density_using_pr;
use anyhow::anyhow;
use std::fs::File;
use std::io::Read;
use std::path::Path;
/// Helmholtz equation of state
pub type Alpha = GenericA<AlphaI, AlphaR>;
/// Methods of helmholtz equation of state
#[allow(non_snake_case)]
impl Alpha {
    /// Calculate J for Alpha::t_flash
    fn J(&self, T: f64, D: f64) -> f64 {
        (D / self.ref_ar().Dc()) * (1.0 + self.ref_ar().rT0D1(T, D) / self.R() / T)
    }
    /// Calculate K for Alpha::t_flash
    fn K(&self, T: f64, D: f64) -> f64 {
        let alphar = self.ref_ar();
        (alphar.rT0D1(T, D) + alphar.rT0D0(T, D)) / self.R() / T + (D / self.ref_ar().Dc()).ln()
    }
    /// Calculate Jdelta for Alpha::t_flash
    fn Jdelta(&self, T: f64, D: f64) -> f64 {
        let alphar = self.ref_ar();
        1.0 + (2.0 * alphar.rT0D1(T, D) + alphar.rT0D2(T, D)) / self.R() / T
    }
    /// Calculate Kdelta for Alpha::t_flash
    fn Kdelta(&self, T: f64, D: f64) -> f64 {
        let alphar = self.ref_ar();
        ((2.0 * alphar.rT0D1(T, D) + alphar.rT0D2(T, D)) / self.R() / T + 1.0)
            / (D / self.ref_ar().Dc())
    }
}
#[allow(non_snake_case)]
impl Alpha {
    /// read helmholtz equation of state from fluid.json file
    pub fn read_json(path: &str) -> anyhow::Result<Alpha> {
        let mut file_json: Option<File>;
        file_json = match File::open(Path::new(path)) {
            Ok(file) => Some(file),
            Err(_) => None,
        };
        if file_json.is_none() {
            file_json =
                match File::open(Path::new(env!("CARGO_MANIFEST_DIR")).join("res").join(path)) {
                    Ok(file) => Some(file),
                    Err(_) => None,
                };
        };
        let mut file_json = file_json.ok_or(anyhow!(TlErr::NoJson))?;
        let mut str_json = String::new();
        let _ = file_json.read_to_string(&mut str_json);
        let eos: Option<Alpha> = match serde_json::from_str(&str_json) {
            Ok(alpha) => Some(alpha),
            Err(_) => None,
        };
        let eos = eos.ok_or(anyhow!(TlErr::NoHelmholtz))?;
        Ok(eos)
    }
    /// impl methods to overwrite Flash::t_flash
    pub fn t_flash(&mut self, Ts: f64) -> anyhow::Result<()> {
        // Reference [AKASAKA_2008]
        // Newton-Raphson algorithm
        let alphar = self.ref_ar();
        let rhoc = alphar.Dc();
        let (mut rhog, mut rhol): (f64, f64) = (1.0, 1.0);
        let (mut Jg, mut Jl, mut DJg, mut DJl): (f64, f64, f64, f64);
        let (mut Kg, mut Kl, mut DKg, mut DKl): (f64, f64, f64, f64);
        let mut Delta: f64;
        let mut is_conv: bool = false; // default = false
        'outer: for factor in 0..10 {
            rhog = alphar.rhogs(Ts) * (1.0 - (factor as f64) / 10.0);
            rhol = alphar.rhols(Ts) * (1.0 + (factor as f64) / 10.0);
            'inner: loop {
                Jg = self.J(Ts, rhog);
                Jl = self.J(Ts, rhol);
                Kg = self.K(Ts, rhog);
                Kl = self.K(Ts, rhol);
                // The following convergence condition refer to [AKASAKA_2008]
                if ((Kg - Kl).abs() + (Jg - Jl).abs()) < 1E-8 {
                    is_conv = true;
                    break 'outer; // convergence
                }
                DJg = self.Jdelta(Ts, rhog);
                DJl = self.Jdelta(Ts, rhol);
                // Jdelta = DP_DD_T /RT
                if DJg <= 0.0 || DJl <= 0.0 {
                    break 'inner; //divergence
                }
                DKg = self.Kdelta(Ts, rhog);
                DKl = self.Kdelta(Ts, rhol);
                Delta = DJg * DKl - DJl * DKg;
                rhog += ((Kg - Kl) * DJl - (Jg - Jl) * DKl) / Delta * rhoc;
                rhol += ((Kg - Kl) * DJg - (Jg - Jl) * DKg) / Delta * rhoc;
                // make sure rhog != NAN and rhol != NAN
                if rhog.is_nan() || rhol.is_nan() {
                    break 'inner; //divergence
                }
            }
        }
        if is_conv {
            self.set_phase(Phase::Two {
                Ts,
                Dg: rhog,
                Dl: rhol,
                X: 1.0,
            });
            Ok(())
        } else {
            Err(anyhow!(TlErr::NotConvForT))
        }
    }
    /// impl methods to overwrite Flash::td_flash
    pub fn td_flash(&mut self, T: f64, D: f64) -> anyhow::Result<()> {
        if T >=self.ref_ar().Tc() // supercritical region
            || D <= 0.85 * self.ref_ar().rhogs(T)
            || D >= 1.05 * self.ref_ar().rhols(T)
        {
            self.set_phase(Phase::One { T, D });
            Ok(()) // one phase
        } else if let Err(why) = self.t_flash(T) {
            Err(why) // Self::t_flash diverge
        } else {
            match *self.ref_phase() {
                Phase::Two { Dg, Dl, .. } => {
                    if D < Dg || D > Dl {
                        self.set_phase(Phase::One { T, D });
                        Ok(()) // one phase
                    } else {
                        self.set_phase(Phase::Two {
                            Ts: T,
                            Dg,
                            Dl,
                            X: (1.0 / D - 1.0 / Dl) / (1.0 / Dg + 1.0 / Dl),
                        });
                        Ok(()) // two phase
                    }
                }
                _ => Err(anyhow!(TlErr::NotConvForTD)), // shit-code in td_flash
            }
        }
    }
    /// impl methods to overwrite Flash::tp_flash
    pub fn tp_flash(&mut self, T: f64, P: f64) -> anyhow::Result<()> {
        let phase: char;
        let ps = self.ref_ar().ps(T);
        if T >= self.ref_ar().Tc() {
            phase = 's'; // supercritical region
        } else if P < 0.95 * ps {
            phase = 'g' // gas region
        } else if P > 1.05 * ps {
            phase = 'l'; // liquid region
        } else if let Err(why) = self.t_flash(T) {
            return Err(why);
        } else {
            let ps = self.ps().unwrap();
            if P < ps {
                phase = 'g';
            } else {
                phase = 'l';
            }
        }
        let alphar = self.ref_ar();
        let mut rho = calc_density_using_pr(
            T,
            P,
            self.ref_ar().Tc(),
            self.ref_ar().Pc(),
            self.R(),
            alphar.omega(),
        );
        if phase == 'g' {
            rho = rho.min(alphar.rhogs(T));
        }
        if phase == 'l' {
            rho = rho.max(alphar.rhols(T));
        }
        let mut p_0: f64;
        loop {
            self.set_phase(Phase::One { T, D: rho });
            p_0 = self.p().unwrap() - P;
            if (p_0 / P).abs() < 1E-9 {
                break;
            }
            rho -= p_0 / self.Dp_DD_T().unwrap();
        }
        Ok(())
    }
}
/// unit test
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    #[allow(non_snake_case)]
    fn test_helmholtz_alpha() {
        let mut SO2: Alpha = Alpha::read_json("SO2.json").expect("no SO2.json");
        // let serialized = serde_json::to_string_pretty(&SO2).unwrap();
        // println!("serialized = {}", serialized);
        // println!("read_json pass.");
        for T in 197..432 {
            if let Err(_) = SO2.t_flash(T as f64) {
                assert_eq!(T, 431);
                break;
            }
        }
    }
}
