use super::{AlphaDisp, AlphaHC, NA};
use crate::core::CalcAr;
#[allow(non_snake_case)]
pub struct AlphaR {
    disp: AlphaDisp,
    hc: AlphaHC,
    R: f64,
    M: f64,
}
#[allow(non_snake_case)]
impl AlphaR {
    pub fn new(m: f64, sigma: f64, epsilon: f64, M: f64) -> AlphaR {
        AlphaR {
            disp: AlphaDisp::new(m, sigma, epsilon),
            hc: AlphaHC::new(m, sigma, epsilon),
            R: 8.314462618,
            M,
        }
    }
    pub fn change_density(&self, D: f64) -> f64 {
        // change density to number density
        if self.R < 10.0 {
            // molar density to number density
            D * NA / 1E30
        } else {
            // mass density to number density
            D / self.M * NA / 1E30
        }
    }
}
#[allow(non_snake_case)]
impl CalcAr for AlphaR {
    /// > fn rT0D0(&self, _T: f64, _D: f64) -> f64; Equal to =  
    /// > $$a^r\left(T,D\right)$$  
    fn rT0D0(&self, T: f64, D: f64) -> f64 {
        let D = self.change_density(D);
        self.R * T * (self.disp.calc_rT0D0(T, D) + self.hc.calc_rT0D0(T, D))
    }
    /// > fn rT0D1(&self, _T: f64, _D: f64) -> f64; Equal to =  
    /// > $$D\left(\frac{\partial a^r}{\partial D}\right)_T$$  
    fn rT0D1(&self, T: f64, D: f64) -> f64 {
        let D = self.change_density(D);
        self.R * T * (self.disp.calc_rT0D1(T, D) + self.hc.calc_rT0D1(T, D))
    }
    /// > fn rT0D2(&self, _T: f64, _D: f64) -> f64; Equal to =  
    /// > $$D^2\left(\frac{\partial^2a^r}{\partial D^2}\right)_T$$  
    fn rT0D2(&self, T: f64, D: f64) -> f64 {
        let D = self.change_density(D);
        self.R * T * (self.disp.calc_rT0D2(T, D) + self.hc.calc_rT0D2(T, D))
    }
    /// > fn rT1D0(&self, _T: f64, _D: f64) -> f64; Equal to =  
    /// > $$T\left(\frac{\partial a^r}{\partial T}\right)_D$$  
    fn rT1D0(&self, T: f64, D: f64) -> f64 {
        let D = self.change_density(D);
        (self.R * T)
            * (self.disp.calc_rT0D0(T, D)
                + self.disp.calc_rT1D0(T, D)
                + self.hc.calc_rT0D0(T, D)
                + self.hc.calc_rT1D0(T, D))
    }
    /// > fn rT1D1(&self, _T: f64, _D: f64) -> f64; Equal to =  
    /// > $$TD\left(\frac{\partial^2a^r}{\partial T\partial D}\right)$$  
    fn rT1D1(&self, T: f64, D: f64) -> f64 {
        let D = self.change_density(D);
        (self.R * T)
            * (self.disp.calc_rT0D1(T, D)
                + self.disp.calc_rT1D1(T, D)
                + self.hc.calc_rT0D1(T, D)
                + self.hc.calc_rT1D1(T, D))
    }
    /// > fn rT2D0(&self, _T: f64, _D: f64) -> f64; Equal to =  
    /// > $$T^2\left(\frac{\partial^2a^r}{\partial T^2}\right)_D$$  
    fn rT2D0(&self, T: f64, D: f64) -> f64 {
        let D = self.change_density(D);
        (self.R * T)
            * (2.0 * self.disp.calc_rT1D0(T, D)
                + self.disp.calc_rT2D0(T, D)
                + 2.0 * self.hc.calc_rT1D0(T, D)
                + self.hc.calc_rT2D0(T, D))
    }
}
/// unit test
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    #[allow(non_snake_case)]
    fn test_pc_saft_alpha_r() {
        let r = AlphaR::new(1.6069, 3.5206, 191.42, 30.07); // parameters for ethane
        let (T, Tx) = (300.0, 0.001);
        let (D, Dx) = (1000.0, 0.01);
        let convergence_criteria_for_t = 1E-9; // convergence criteria equal to 1E-9
        let convergence_criteria_for_d = 1E-9;
        /*
        println!(
            "[rT0D0->rT0D1]true={},false={}",
            r.rT0D1(T, D) / D,
            (r.rT0D0(T, D + Dx) - r.rT0D0(T, D - Dx)) / (2.0 * Dx)
        );
        println!(
            "[rT0D0->rT0D1]true/false-1.0={}",
            (r.rT0D1(T, D) / D) / ((r.rT0D0(T, D + Dx) - r.rT0D0(T, D - Dx)) / (2.0 * Dx)) - 1.0
        );
        */
        assert!(
            ((r.rT0D1(T, D) / D) / ((r.rT0D0(T, D + Dx) - r.rT0D0(T, D - Dx)) / (2.0 * Dx)) - 1.0)
                .abs()
                < convergence_criteria_for_d
        );
        /*
        println!(
            "[rT0D1->rT0D2]true={},false={}",
            r.rT0D2(T, D) / D.powi(2),
            (r.rT0D1(T, D + Dx) / (D + Dx) - r.rT0D1(T, D - Dx) / (D - Dx)) / (2.0 * Dx)
        );
        println!(
            "[rT0D1->rT0D2]true/false-1.0={}",
            (r.rT0D2(T, D) / D.powi(2))
                / ((r.rT0D1(T, D + Dx) / (D + Dx) - r.rT0D1(T, D - Dx) / (D - Dx)) / (2.0 * Dx))
                - 1.0
        );
        */
        assert!(
            ((r.rT0D2(T, D) / D.powi(2))
                / ((r.rT0D1(T, D + Dx) / (D + Dx) - r.rT0D1(T, D - Dx) / (D - Dx)) / (2.0 * Dx))
                - 1.0)
                .abs()
                < convergence_criteria_for_d
        );
        /*
        println!(
            "[rT0D0->rT1D0]true={},false={}",
            r.rT1D0(T, D) / T,
            (r.rT0D0(T + Tx, D) - r.rT0D0(T - Tx, D)) / (2.0 * Tx)
        );
        println!(
            "[rT0D0->rT1D0]true/false-1.0={}",
            (r.rT1D0(T, D) / T) / ((r.rT0D0(T + Tx, D) - r.rT0D0(T - Tx, D)) / (2.0 * Tx)) - 1.0
        );
        */
        assert!(
            ((r.rT1D0(T, D) / T) / ((r.rT0D0(T + Tx, D) - r.rT0D0(T - Tx, D)) / (2.0 * Tx)) - 1.0)
                .abs()
                < convergence_criteria_for_t
        );
        /*
        println!(
            "[rT0D1->rT1D1]true={},false={}",
            r.rT1D1(T, D) / T / D,
            (r.rT0D1(T + Tx, D) / D - r.rT0D1(T - Tx, D) / D) / (2.0 * Tx)
        );
        println!(
            "[rT0D1->rT1D1]true/false-1.0={}",
            (r.rT1D1(T, D) / T / D)
                / ((r.rT0D1(T + Tx, D) / D - r.rT0D1(T - Tx, D) / D) / (2.0 * Tx))
                - 1.0
        );
        */
        assert!(
            ((r.rT1D1(T, D) / T / D)
                / ((r.rT0D1(T + Tx, D) / D - r.rT0D1(T - Tx, D) / D) / (2.0 * Tx))
                - 1.0)
                .abs()
                < convergence_criteria_for_t
        );
        /*
        println!(
            "[rT1D0->rT1D1]true={},false={}",
            r.rT1D1(T, D) / T / D,
            (r.rT1D0(T, D + Dx) / T - r.rT1D0(T, D - Dx) / T) / (2.0 * Dx)
        );
        println!(
            "[rT1D0->rT1D1]true/false-1.0={}",
            (r.rT1D1(T, D) / T / D)
                / ((r.rT1D0(T, D + Dx) / T - r.rT1D0(T, D - Dx) / T) / (2.0 * Dx))
                - 1.0
        );
        */
        assert!(
            ((r.rT1D1(T, D) / T / D)
                / ((r.rT1D0(T, D + Dx) / T - r.rT1D0(T, D - Dx) / T) / (2.0 * Dx))
                - 1.0)
                .abs()
                < convergence_criteria_for_d
        );
        /*
        println!(
            "[rT1D0->rT2D0]true={},false={}",
            r.rT2D0(T, D) / T.powi(2),
            (r.rT1D0(T + Tx, D) / (T + Tx) - r.rT1D0(T - Tx, D) / (T - Tx)) / (2.0 * Tx)
        );
        println!(
            "[rT1D0->rT2D0]true/false-1.0={}",
            (r.rT2D0(T, D) / T.powi(2))
                / ((r.rT1D0(T + Tx, D) / (T + Tx) - r.rT1D0(T - Tx, D) / (T - Tx)) / (2.0 * Tx))
                - 1.0
        );
        */
        assert!(
            ((r.rT2D0(T, D) / T.powi(2))
                / ((r.rT1D0(T + Tx, D) / (T + Tx) - r.rT1D0(T - Tx, D) / (T - Tx)) / (2.0 * Tx))
                - 1.0)
                .abs()
                < convergence_criteria_for_t
        );
    }
}
