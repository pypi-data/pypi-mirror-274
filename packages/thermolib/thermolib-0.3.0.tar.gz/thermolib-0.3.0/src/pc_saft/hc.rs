use std::f64::consts::PI;
pub struct AlphaHC {
    m: f64,
    sigma: f64,
    epsilon: f64,
}
#[allow(non_snake_case)]
impl AlphaHC {
    pub fn new(m: f64, sigma: f64, epsilon: f64) -> AlphaHC {
        AlphaHC { m, sigma, epsilon }
    }
    pub fn calc_rT0D0(&self, T: f64, D: f64) -> f64 {
        let d = self.sigma * (1.0 - 0.12 * (-3.0 * self.epsilon / T).exp());
        let zeta0 = PI / 6.0 * D * self.m;
        let zeta1 = zeta0 * d;
        let zeta2 = zeta0 * d.powi(2);
        let zeta3 = zeta0 * d.powi(3);
        let alpha = 1.0 / zeta0
            * (3.0 * zeta1 * zeta2 / (1.0 - zeta3)
                + zeta2.powi(3) / zeta3 / (1.0 - zeta3).powi(2)
                + zeta2.powi(3) / zeta3.powi(2) * (1.0 - zeta3).ln())
            - (1.0 - zeta3).ln();
        let gii = 1.0 / (1.0 - zeta3)
            + 1.5 * d * zeta2 / (1.0 - zeta3).powi(2)
            + 0.5 * d.powi(2) * zeta2.powi(2) / (1.0 - zeta3).powi(3);
        self.m * alpha - (self.m - 1.0) * gii.ln()
    }
    pub fn calc_rT0D1(&self, T: f64, D: f64) -> f64 {
        let d = self.sigma * (1.0 - 0.12 * (-3.0 * self.epsilon / T).exp());
        let zeta0 = PI / 6.0 * D * self.m;
        let zeta1 = zeta0 * d;
        let zeta2 = zeta0 * d.powi(2);
        let zeta3 = zeta0 * d.powi(3);
        let alpha_d1 = 1.0 / zeta0
            * (3.0 * zeta1 * zeta2 / (1.0 - zeta3).powi(2)
                + 3.0 * zeta2.powi(3) / (1.0 - zeta3).powi(3)
                - zeta2.powi(3) * zeta3 / (1.0 - zeta3).powi(3))
            + zeta3 / (1.0 - zeta3);
        let gii = 1.0 / (1.0 - zeta3)
            + 1.5 * d * zeta2 / (1.0 - zeta3).powi(2)
            + 0.5 * d.powi(2) * zeta2.powi(2) / (1.0 - zeta3).powi(3);
        let gii_d1 = zeta3 / (1.0 - zeta3).powi(2)
            + (1.5 * d)
                * (zeta2 / (1.0 - zeta3).powi(2) + 2.0 * zeta2 * zeta3 / (1.0 - zeta3).powi(3))
            + (0.5 * d.powi(2))
                * (2.0 * zeta2.powi(2) / (1.0 - zeta3).powi(3)
                    + 3.0 * zeta2.powi(2) * zeta3 / (1.0 - zeta3).powi(4));
        self.m * alpha_d1 - (self.m - 1.0) / gii * gii_d1
    }
    pub fn calc_rT0D2(&self, T: f64, D: f64) -> f64 {
        let d = self.sigma * (1.0 - 0.12 * (-3.0 * self.epsilon / T).exp());
        let zeta0 = PI / 6.0 * D * self.m;
        let zeta1 = zeta0 * d;
        let zeta2 = zeta0 * d.powi(2);
        let zeta3 = zeta0 * d.powi(3);
        let alpha_d2 = 1.0 / zeta0
            * (6.0 * zeta1 * zeta2 * zeta3 / (1.0 - zeta3).powi(3)
                + 3.0 * zeta2.powi(3) / (1.0 - zeta3).powi(4)
                + 4.0 * zeta2.powi(3) * zeta3 / (1.0 - zeta3).powi(4)
                - zeta2.powi(3) * zeta3.powi(2) / (1.0 - zeta3).powi(4))
            + zeta3.powi(2) / (1.0 - zeta3).powi(2);
        let gii = 1.0 / (1.0 - zeta3)
            + 1.5 * d * zeta2 / (1.0 - zeta3).powi(2)
            + 0.5 * d.powi(2) * zeta2.powi(2) / (1.0 - zeta3).powi(3);
        let gii_d1 = zeta3 / (1.0 - zeta3).powi(2)
            + (1.5 * d)
                * (zeta2 / (1.0 - zeta3).powi(2) + 2.0 * zeta2 * zeta3 / (1.0 - zeta3).powi(3))
            + (0.5 * d.powi(2))
                * (2.0 * zeta2.powi(2) / (1.0 - zeta3).powi(3)
                    + 3.0 * zeta2.powi(2) * zeta3 / (1.0 - zeta3).powi(4));
        let gii_d2 = 2.0 * zeta3.powi(2) / (1.0 - zeta3).powi(3)
            + (3.0 * d)
                * (2.0 * zeta2 * zeta3 / (1.0 - zeta3).powi(3)
                    + 3.0 * zeta2 * zeta3.powi(2) / (1.0 - zeta3).powi(4))
            + d.powi(2)
                * (zeta2.powi(2) / (1.0 - zeta3).powi(3)
                    + 6.0 * zeta2.powi(2) * zeta3 / (1.0 - zeta3).powi(4)
                    + 6.0 * zeta2.powi(2) * zeta3.powi(2) / (1.0 - zeta3).powi(5));
        self.m * alpha_d2 - (self.m - 1.0) / gii.powi(2) * (gii_d2 * gii - gii_d1.powi(2))
    }
    pub fn calc_rT1D0(&self, T: f64, D: f64) -> f64 {
        let d = self.sigma * (1.0 - 0.12 * (-3.0 * self.epsilon / T).exp());
        let zeta0 = PI / 6.0 * D * self.m;
        let zeta1 = zeta0 * d;
        let zeta2 = zeta0 * d.powi(2);
        let zeta3 = zeta0 * d.powi(3);
        let d_t = self.sigma * (-0.12 * (-3.0 * self.epsilon / T).exp()) * (3.0 * self.epsilon / T);
        let zeta1_t = PI / 6.0 * D * self.m * d_t;
        let zeta2_t = zeta1_t * 2.0 * d;
        let zeta3_t = zeta1_t * 3.0 * d.powi(2);
        let alpha_t1 = zeta1_t / zeta0 * 3.0 * zeta2 / (1.0 - zeta3)
            + zeta2_t / zeta0
                * (3.0 * zeta1 / (1.0 - zeta3)
                    + 3.0 * zeta2.powi(2) / zeta3 / (1.0 - zeta3).powi(2)
                    + 3.0 * zeta2.powi(2) / zeta3.powi(2) * (1.0 - zeta3).ln())
            + zeta3_t / (1.0 - zeta3)
            + zeta3_t / zeta0
                * (3.0 * zeta1 * zeta2 / (1.0 - zeta3).powi(2)
                    - zeta2.powi(3) / zeta3.powi(2) / (1.0 - zeta3)
                    + 3.0 * zeta2.powi(3) / zeta3 / (1.0 - zeta3).powi(3)
                    - zeta2.powi(3) / zeta3.powi(2) / (1.0 - zeta3).powi(3)
                    - 2.0 * zeta2.powi(3) / zeta3.powi(3) * (1.0 - zeta3).ln());
        let gii = 1.0 / (1.0 - zeta3)
            + 1.5 * d * zeta2 / (1.0 - zeta3).powi(2)
            + 0.5 * d.powi(2) * zeta2.powi(2) / (1.0 - zeta3).powi(3);
        let gii_t1 = zeta3_t / (1.0 - zeta3).powi(2)
            + 1.5 * d_t * zeta2 / (1.0 - zeta3).powi(2)
            + (1.5 * d)
                * (zeta2_t / (1.0 - zeta3).powi(2) + 2.0 * zeta2 * zeta3_t / (1.0 - zeta3).powi(3))
            + d * d_t * zeta2.powi(2) / (1.0 - zeta3).powi(3)
            + (0.5 * d.powi(2))
                * (2.0 * zeta2 * zeta2_t / (1.0 - zeta3).powi(3)
                    + 3.0 * zeta2.powi(2) * zeta3_t / (1.0 - zeta3).powi(4));
        self.m * alpha_t1 - (self.m - 1.0) / gii * gii_t1
    }
    pub fn calc_rT1D1(&self, T: f64, D: f64) -> f64 {
        let d = self.sigma * (1.0 - 0.12 * (-3.0 * self.epsilon / T).exp());
        let zeta0 = PI / 6.0 * D * self.m;
        let zeta1 = zeta0 * d;
        let zeta2 = zeta0 * d.powi(2);
        let zeta3 = zeta0 * d.powi(3);
        let d_t = self.sigma * (-0.12 * (-3.0 * self.epsilon / T).exp()) * (3.0 * self.epsilon / T);
        let zeta1_t = PI / 6.0 * D * self.m * d_t;
        let zeta2_t = zeta1_t * 2.0 * d;
        let zeta3_t = zeta1_t * 3.0 * d.powi(2);
        let alpha_t1d1 = zeta1_t / zeta0 * 3.0 * zeta2 / (1.0 - zeta3).powi(2)
            + zeta2_t / zeta0
                * (3.0 * zeta1 / (1.0 - zeta3).powi(2)
                    + 9.0 * zeta2.powi(2) / (1.0 - zeta3).powi(3)
                    - 3.0 * zeta2.powi(2) * zeta3 / (1.0 - zeta3).powi(3))
            + zeta3_t / (1.0 - zeta3).powi(2)
            + zeta3_t / zeta0
                * (6.0 * zeta1 * zeta2 / (1.0 - zeta3).powi(3)
                    + 8.0 * zeta2.powi(3) / (1.0 - zeta3).powi(4)
                    - 2.0 * zeta2.powi(3) * zeta3 / (1.0 - zeta3).powi(4));
        let gii = 1.0 / (1.0 - zeta3)
            + 1.5 * d * zeta2 / (1.0 - zeta3).powi(2)
            + 0.5 * d.powi(2) * zeta2.powi(2) / (1.0 - zeta3).powi(3);
        let gii_t1 = zeta3_t / (1.0 - zeta3).powi(2)
            + 1.5 * d_t * zeta2 / (1.0 - zeta3).powi(2)
            + (1.5 * d)
                * (zeta2_t / (1.0 - zeta3).powi(2) + 2.0 * zeta2 * zeta3_t / (1.0 - zeta3).powi(3))
            + d * d_t * zeta2.powi(2) / (1.0 - zeta3).powi(3)
            + (0.5 * d.powi(2))
                * (2.0 * zeta2 * zeta2_t / (1.0 - zeta3).powi(3)
                    + 3.0 * zeta2.powi(2) * zeta3_t / (1.0 - zeta3).powi(4));
        let gii_d1 = zeta3 / (1.0 - zeta3).powi(2)
            + (1.5 * d)
                * (zeta2 / (1.0 - zeta3).powi(2) + 2.0 * zeta2 * zeta3 / (1.0 - zeta3).powi(3))
            + (0.5 * d.powi(2))
                * (2.0 * zeta2.powi(2) / (1.0 - zeta3).powi(3)
                    + 3.0 * zeta2.powi(2) * zeta3 / (1.0 - zeta3).powi(4));
        let gii_t1d1 = zeta3_t * (1.0 + zeta3) / (1.0 - zeta3).powi(3)
            + (1.5 * d_t)
                * (zeta2 / (1.0 - zeta3).powi(2) + 2.0 * zeta2 * zeta3 / (1.0 - zeta3).powi(3))
            + (1.5 * d)
                * (zeta2_t / (1.0 - zeta3).powi(2)
                    + 4.0 * zeta2 * zeta3_t / (1.0 - zeta3).powi(3)
                    + 2.0 * zeta3 * zeta2_t / (1.0 - zeta3).powi(3)
                    + 6.0 * zeta2 * zeta3 * zeta3_t / (1.0 - zeta3).powi(4))
            + (d * d_t)
                * (2.0 * zeta2.powi(2) / (1.0 - zeta3).powi(3)
                    + 3.0 * zeta2.powi(2) * zeta3 / (1.0 - zeta3).powi(4))
            + (0.5 * d.powi(2))
                * (4.0 * zeta2 * zeta2_t / (1.0 - zeta3).powi(3)
                    + 9.0 * zeta2.powi(2) * zeta3_t / (1.0 - zeta3).powi(4)
                    + 6.0 * zeta2 * zeta3 * zeta2_t / (1.0 - zeta3).powi(4)
                    + 12.0 * zeta2.powi(2) * zeta3 * zeta3_t / (1.0 - zeta3).powi(5));
        self.m * alpha_t1d1 - (self.m - 1.0) / gii.powi(2) * (gii_t1d1 * gii - gii_t1 * gii_d1)
    }
    pub fn calc_rT2D0(&self, T: f64, D: f64) -> f64 {
        let d = self.sigma * (1.0 - 0.12 * (-3.0 * self.epsilon / T).exp());
        let zeta0 = PI / 6.0 * D * self.m;
        let zeta1 = zeta0 * d;
        let zeta2 = zeta0 * d.powi(2);
        let zeta3 = zeta0 * d.powi(3);
        let d_t = self.sigma * (-0.12 * (-3.0 * self.epsilon / T).exp()) * (3.0 * self.epsilon / T);
        let zeta1_t = PI / 6.0 * D * self.m * d_t;
        let zeta2_t = zeta1_t * 2.0 * d;
        let zeta3_t = zeta1_t * 3.0 * d.powi(2);
        let d_tt = self.sigma
            * (-0.12 * (-3.0 * self.epsilon / T).exp())
            * (3.0 * self.epsilon / T)
            * (3.0 * self.epsilon / T - 1.0);
        let zeta1_tt = zeta0 * d_tt;
        let zeta2_tt = zeta0 * 2.0 * (d_tt * d + d_t.powi(2));
        let zeta3_tt = zeta0 * 3.0 * d * (d_tt * d + 2.0 * d_t.powi(2));
        let alpha_t2 = zeta1_tt / zeta0 * 3.0 * zeta2 / (1.0 - zeta3)
            + zeta1_t * zeta2_t / zeta0 * 6.0 / (1.0 - zeta3)
            + zeta1_t * zeta3_t / zeta0 * 6.0 * zeta2 / (1.0 - zeta3).powi(2)
            + zeta2_tt / zeta0
                * (3.0 * zeta1 / (1.0 - zeta3)
                    + 3.0 * zeta2.powi(2) / zeta3 / (1.0 - zeta3).powi(2)
                    + 3.0 * zeta2.powi(2) / zeta3.powi(2) * (1.0 - zeta3).ln())
            + zeta2_t.powi(2) / zeta0
                * (6.0 * zeta2 / zeta3 / (1.0 - zeta3).powi(2)
                    + 6.0 * zeta2 / zeta3.powi(2) * (1.0 - zeta3).ln())
            + zeta2_t * zeta3_t / zeta0 * 6.0 * zeta1 / (1.0 - zeta3).powi(2)
            + zeta2_t * zeta3_t / zeta0
                * (-6.0 * zeta2.powi(2) / zeta3.powi(2) / (1.0 - zeta3)
                    + 18.0 * zeta2.powi(2) / zeta3 / (1.0 - zeta3).powi(3)
                    - 6.0 * zeta2.powi(2) / zeta3.powi(2) / (1.0 - zeta3).powi(3)
                    - 12.0 * zeta2.powi(2) / zeta3.powi(3) * (1.0 - zeta3).ln())
            + zeta3_tt / zeta0
                * (-zeta2.powi(3) / zeta3.powi(2) / (1.0 - zeta3)
                    + 3.0 * zeta2.powi(3) / zeta3 / (1.0 - zeta3).powi(3)
                    - zeta2.powi(3) / zeta3.powi(2) / (1.0 - zeta3).powi(3)
                    - 2.0 * zeta2.powi(3) / zeta3.powi(3) * (1.0 - zeta3).ln())
            + zeta3_tt / zeta0 * 3.0 * zeta1 * zeta2 / (1.0 - zeta3).powi(2)
            + zeta3_tt / (1.0 - zeta3)
            + zeta3_t.powi(2) / (1.0 - zeta3).powi(2)
            + zeta3_t.powi(2) / zeta0
                * (6.0 * zeta2.powi(3) / zeta3.powi(4) * (1.0 - zeta3).ln()
                    + 6.0 * zeta1 * zeta2 / (1.0 - zeta3).powi(3)
                    + 2.0 * zeta2.powi(3) / zeta3.powi(3) / (1.0 - zeta3)
                    - 3.0 * zeta2.powi(3) / zeta3.powi(2) / (1.0 - zeta3).powi(2)
                    + 2.0 * zeta2.powi(3) / zeta3.powi(3) / (1.0 - zeta3).powi(2)
                    + 12.0 * zeta2.powi(3) / zeta3 / (1.0 - zeta3).powi(4)
                    - 8.0 * zeta2.powi(3) / zeta3.powi(2) / (1.0 - zeta3).powi(4)
                    + 2.0 * zeta2.powi(3) / zeta3.powi(3) / (1.0 - zeta3).powi(4))
            - zeta1_t / zeta0 * 3.0 * zeta2 / (1.0 - zeta3)
            - zeta2_t / zeta0
                * (3.0 * zeta1 / (1.0 - zeta3)
                    + 3.0 * zeta2.powi(2) / zeta3 / (1.0 - zeta3).powi(2)
                    + 3.0 * zeta2.powi(2) / zeta3.powi(2) * (1.0 - zeta3).ln())
            - zeta3_t / (1.0 - zeta3)
            - zeta3_t / zeta0
                * (3.0 * zeta1 * zeta2 / (1.0 - zeta3).powi(2)
                    - zeta2.powi(3) / zeta3.powi(2) / (1.0 - zeta3)
                    + 3.0 * zeta2.powi(3) / zeta3 / (1.0 - zeta3).powi(3)
                    - zeta2.powi(3) / zeta3.powi(2) / (1.0 - zeta3).powi(3)
                    - 2.0 * zeta2.powi(3) / zeta3.powi(3) * (1.0 - zeta3).ln());
        let gii = 1.0 / (1.0 - zeta3)
            + 1.5 * d * zeta2 / (1.0 - zeta3).powi(2)
            + 0.5 * d.powi(2) * zeta2.powi(2) / (1.0 - zeta3).powi(3);
        let gii_t1 = zeta3_t / (1.0 - zeta3).powi(2)
            + 1.5 * d_t * zeta2 / (1.0 - zeta3).powi(2)
            + (1.5 * d)
                * (zeta2_t / (1.0 - zeta3).powi(2) + 2.0 * zeta2 * zeta3_t / (1.0 - zeta3).powi(3))
            + d * d_t * zeta2.powi(2) / (1.0 - zeta3).powi(3)
            + (0.5 * d.powi(2))
                * (2.0 * zeta2 * zeta2_t / (1.0 - zeta3).powi(3)
                    + 3.0 * zeta2.powi(2) * zeta3_t / (1.0 - zeta3).powi(4));
        let gii_t2 = zeta3_tt / (1.0 - zeta3).powi(2)
            + 2.0 * zeta3_t.powi(2) / (1.0 - zeta3).powi(3)
            - zeta3_t / (1.0 - zeta3).powi(2)
            + 1.5 * d_tt * zeta2 / (1.0 - zeta3).powi(2)
            + (1.5 * d_t)
                * (2.0 * zeta2_t / (1.0 - zeta3).powi(2)
                    + 4.0 * zeta2 * zeta3_t / (1.0 - zeta3).powi(3)
                    - zeta2 / (1.0 - zeta3).powi(2))
            + (1.5 * d)
                * (zeta2_tt / (1.0 - zeta3).powi(2)
                    + 4.0 * zeta2_t * zeta3_t / (1.0 - zeta3).powi(3)
                    + 2.0 * zeta2 * zeta3_tt / (1.0 - zeta3).powi(3)
                    + 6.0 * zeta2 * zeta3_t.powi(2) / (1.0 - zeta3).powi(4)
                    - zeta2_t / (1.0 - zeta3).powi(2)
                    - 2.0 * zeta2 * zeta3_t / (1.0 - zeta3).powi(3))
            + (d_t.powi(2) + d * d_tt) * zeta2.powi(2) / (1.0 - zeta3).powi(3)
            + (d * d_t)
                * (4.0 * zeta2 * zeta2_t / (1.0 - zeta3).powi(3)
                    + 6.0 * zeta2.powi(2) * zeta3_t / (1.0 - zeta3).powi(4)
                    - zeta2.powi(2) / (1.0 - zeta3).powi(3))
            + (0.5 * d.powi(2))
                * (2.0 * zeta2_t.powi(2) / (1.0 - zeta3).powi(3)
                    + 2.0 * zeta2 * zeta2_tt / (1.0 - zeta3).powi(3)
                    + 12.0 * zeta2 * zeta2_t * zeta3_t / (1.0 - zeta3).powi(4)
                    + 3.0 * zeta2.powi(2) * zeta3_tt / (1.0 - zeta3).powi(4)
                    + 12.0 * zeta2.powi(2) * zeta3_t.powi(2) / (1.0 - zeta3).powi(5)
                    - 2.0 * zeta2 * zeta2_t / (1.0 - zeta3).powi(3)
                    - 3.0 * zeta2.powi(2) * zeta3_t / (1.0 - zeta3).powi(4));
        self.m * alpha_t2 - (self.m - 1.0) / gii.powi(2) * (gii_t2 * gii - gii_t1.powi(2))
    }
}
/// unit test
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    #[allow(non_snake_case)]
    fn test_pc_saft_hc() {
        let hc = AlphaHC::new(1.6069, 3.5206, 191.42); // parameters for ethane
        let (T, Tx) = (300.0, 0.001);
        let (D, Dx) = (0.001, 0.0000001);
        let convergence_criteria_for_t = 1E-9; // convergence criteria equal to 1E-9
        let convergence_criteria_for_d = 1E-10;
        /*
        println!(
            "[rT0D0->rT0D1]true={},false={}",
            hc.calc_rT0D1(T, D) / D,
            (hc.calc_rT0D0(T, D + Dx) - hc.calc_rT0D0(T, D - Dx)) / (2.0 * Dx)
        );
        println!(
            "[rT0D0->rT0D1]true/false-1.0={}",
            (hc.calc_rT0D1(T, D) / D)
                / ((hc.calc_rT0D0(T, D + Dx) - hc.calc_rT0D0(T, D - Dx)) / (2.0 * Dx))
                - 1.0
        );
        */
        assert!(
            ((hc.calc_rT0D1(T, D) / D)
                / ((hc.calc_rT0D0(T, D + Dx) - hc.calc_rT0D0(T, D - Dx)) / (2.0 * Dx))
                - 1.0)
                .abs()
                < convergence_criteria_for_d
        );
        /*
        println!(
            "[rT0D1->rT0D2]true={},false={}",
            hc.calc_rT0D2(T, D) / D.powi(2),
            (hc.calc_rT0D1(T, D + Dx) / (D + Dx) - hc.calc_rT0D1(T, D - Dx) / (D - Dx))
                / (2.0 * Dx)
        );
        println!(
            "[rT0D1->rT0D2]true/false-1.0={}",
            (hc.calc_rT0D2(T, D) / D.powi(2))
                / ((hc.calc_rT0D1(T, D + Dx) / (D + Dx) - hc.calc_rT0D1(T, D - Dx) / (D - Dx))
                    / (2.0 * Dx))
                - 1.0
        );
        */
        assert!(
            ((hc.calc_rT0D2(T, D) / D.powi(2))
                / ((hc.calc_rT0D1(T, D + Dx) / (D + Dx) - hc.calc_rT0D1(T, D - Dx) / (D - Dx))
                    / (2.0 * Dx))
                - 1.0)
                .abs()
                < convergence_criteria_for_d
        );
        /*
        println!(
            "[rT0D0->rT1D0]true={},false={}",
            hc.calc_rT1D0(T, D) / T,
            (hc.calc_rT0D0(T + Tx, D) - hc.calc_rT0D0(T - Tx, D)) / (2.0 * Tx)
        );
        println!(
            "[rT0D0->rT1D0]true/false-1.0={}",
            (hc.calc_rT1D0(T, D) / T)
                / ((hc.calc_rT0D0(T + Tx, D) - hc.calc_rT0D0(T - Tx, D)) / (2.0 * Tx))
                - 1.0
        );
        */
        assert!(
            ((hc.calc_rT1D0(T, D) / T)
                / ((hc.calc_rT0D0(T + Tx, D) - hc.calc_rT0D0(T - Tx, D)) / (2.0 * Tx))
                - 1.0)
                .abs()
                < convergence_criteria_for_t
        );
        /*
        println!(
            "[rT0D1->rT1D1]true={},false={}",
            hc.calc_rT1D1(T, D) / T / D,
            (hc.calc_rT0D1(T + Tx, D) / D - hc.calc_rT0D1(T - Tx, D) / D) / (2.0 * Tx)
        );
        println!(
            "[rT0D1->rT1D1]true/false-1.0={}",
            (hc.calc_rT1D1(T, D) / T / D)
                / ((hc.calc_rT0D1(T + Tx, D) / D - hc.calc_rT0D1(T - Tx, D) / D) / (2.0 * Tx))
                - 1.0
        );
        */
        assert!(
            ((hc.calc_rT1D1(T, D) / T / D)
                / ((hc.calc_rT0D1(T + Tx, D) / D - hc.calc_rT0D1(T - Tx, D) / D) / (2.0 * Tx))
                - 1.0)
                .abs()
                < convergence_criteria_for_t
        );
        /*
        println!(
            "[rT1D0->rT1D1]true={},false={}",
            hc.calc_rT1D1(T, D) / T / D,
            (hc.calc_rT1D0(T, D + Dx) / T - hc.calc_rT1D0(T, D - Dx) / T) / (2.0 * Dx)
        );
        println!(
            "[rT1D0->rT1D1]true/false-1.0={}",
            (hc.calc_rT1D1(T, D) / T / D)
                / ((hc.calc_rT1D0(T, D + Dx) / T - hc.calc_rT1D0(T, D - Dx) / T) / (2.0 * Dx))
                - 1.0
        );
        */
        assert!(
            ((hc.calc_rT1D1(T, D) / T / D)
                / ((hc.calc_rT1D0(T, D + Dx) / T - hc.calc_rT1D0(T, D - Dx) / T) / (2.0 * Dx))
                - 1.0)
                .abs()
                < convergence_criteria_for_d
        );
        /*
        println!(
            "[rT1D0->rT2D0]true={},false={}",
            hc.calc_rT2D0(T, D) / T.powi(2),
            (hc.calc_rT1D0(T + Tx, D) / (T + Tx) - hc.calc_rT1D0(T - Tx, D) / (T - Tx))
                / (2.0 * Tx)
        );
        println!(
            "[rT1D0->rT2D0]true/false-1.0={}",
            (hc.calc_rT2D0(T, D) / T.powi(2))
                / ((hc.calc_rT1D0(T + Tx, D) / (T + Tx) - hc.calc_rT1D0(T - Tx, D) / (T - Tx))
                    / (2.0 * Tx))
                - 1.0
        );
        */
        assert!(
            ((hc.calc_rT2D0(T, D) / T.powi(2))
                / ((hc.calc_rT1D0(T + Tx, D) / (T + Tx) - hc.calc_rT1D0(T - Tx, D) / (T - Tx))
                    / (2.0 * Tx))
                - 1.0)
                .abs()
                < convergence_criteria_for_t
        ); // convergence criteria equal to 1E-9
    }
}
