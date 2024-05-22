use super::AlphaR;
use crate::core::{GenericA, IdealCv, Phase, Prop, TlErr};
use anyhow::anyhow;
/// PC-SAFT equation of state
pub type Alpha = GenericA<IdealCv, AlphaR>;
#[allow(non_snake_case)]
impl Alpha {
    pub fn new_pc_saft(m: f64, sigma: f64, epsilon: f64, M: f64) -> Self {
        Self::new(IdealCv {}, AlphaR::new(m, sigma, epsilon, M), M)
    }
}
/// Methods of PC-SAFT equation of state
#[allow(non_snake_case)]
impl Alpha {
    /// impl methods to overwrite Flash::td_flash
    pub fn td_flash(&mut self, T: f64, D: f64) -> anyhow::Result<()> {
        self.set_phase(Phase::One { T, D });
        Ok(()) // one phase
    }
    /// impl methods to overwrite Flash::tp_flash
    pub fn tp_flash(&mut self, T: f64, P: f64) -> anyhow::Result<()> {
        let mut p_0: f64;
        // Iteration from gas phase: Zg=1
        let mut rho_g = P / (self.R() * T);
        loop {
            self.set_phase(Phase::One { T, D: rho_g });
            p_0 = self.p().unwrap() - P;
            if (p_0 / P).abs() < 1E-9 {
                break;
            }
            rho_g -= p_0 / self.Dp_DD_T().unwrap();
        }
        let gibbs_g = if self.Dp_DD_T().unwrap() < 0.0 {
            1E16
        } else {
            self.g().unwrap()
        };
        // Iteration from liquid phase: Zl=0.1
        let mut rho_l = P / (self.R() * T * 0.1);
        loop {
            self.set_phase(Phase::One { T, D: rho_l });
            p_0 = self.p().unwrap() - P;
            if (p_0 / P).abs() < 1E-9 {
                break;
            }
            rho_l -= p_0 / self.Dp_DD_T().unwrap();
        }
        let gibbs_l = if self.Dp_DD_T().unwrap() < 0.0 {
            1E16
        } else {
            self.g().unwrap()
        };
        // Check output
        if gibbs_g < 1E16 && gibbs_l < 1E16 {
            if gibbs_g < gibbs_l {
                self.set_phase(Phase::One { T, D: rho_g });
            } else {
                self.set_phase(Phase::One { T, D: rho_l });
            }
            Ok(())
        } else if gibbs_g < 1E16 && gibbs_l == 1E16 {
            self.set_phase(Phase::One { T, D: rho_g });
            Ok(())
        } else if gibbs_l < 1E16 && gibbs_g == 1E6 {
            self.set_phase(Phase::One { T, D: rho_l });
            Ok(())
        } else {
            Err(anyhow!(TlErr::NotConvForTD))
        }
    }
}
/// unit test
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    #[allow(non_snake_case)]
    fn test_pc_saft_alpha() {
        let mut pc_saft = Alpha::new(
            IdealCv {},
            AlphaR::new(1.6069, 3.5206, 191.42, 30.07),
            30.07,
        ); // parameters for ethane
        let T = 300.0; // K
        let D = 1000.0; // mol/m3
        let _ = pc_saft.td_flash(T, D);
        let _ = pc_saft.tp_flash(T, pc_saft.p().unwrap());
        assert!(pc_saft.D().unwrap() / D - 1.0 < 1E-12);
    }
}
