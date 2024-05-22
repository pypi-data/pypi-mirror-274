use std::f64::consts::PI;
pub struct AlphaDisp {
    m: f64,
    sigma: f64,
    epsilon: f64,
}
#[allow(non_snake_case)]
impl AlphaDisp {
    pub fn new(m: f64, sigma: f64, epsilon: f64) -> AlphaDisp {
        AlphaDisp { m, sigma, epsilon }
    }
    pub fn calc_rT0D0(&self, T: f64, D: f64) -> f64 {
        let d = self.sigma * (1.0 - 0.12 * (-3.0 * self.epsilon / T).exp());
        let eta = PI / 6.0 * D * self.m * d.powi(3);
        let m1 = (self.m - 1.0) / self.m;
        let m1m2 = (self.m - 1.0) * (self.m - 2.0) / self.m.powi(2);
        let i1 = (A0[0] + m1 * A1[0] + m1m2 * A2[0])
            + (A0[1] + m1 * A1[1] + m1m2 * A2[1]) * eta
            + (A0[2] + m1 * A1[2] + m1m2 * A2[2]) * eta.powi(2)
            + (A0[3] + m1 * A1[3] + m1m2 * A2[3]) * eta.powi(3)
            + (A0[4] + m1 * A1[4] + m1m2 * A2[4]) * eta.powi(4)
            + (A0[5] + m1 * A1[5] + m1m2 * A2[5]) * eta.powi(5)
            + (A0[6] + m1 * A1[6] + m1m2 * A2[6]) * eta.powi(6);
        let i2 = (B0[0] + m1 * B1[0] + m1m2 * B2[0])
            + (B0[1] + m1 * B1[1] + m1m2 * B2[1]) * eta
            + (B0[2] + m1 * B1[2] + m1m2 * B2[2]) * eta.powi(2)
            + (B0[3] + m1 * B1[3] + m1m2 * B2[3]) * eta.powi(3)
            + (B0[4] + m1 * B1[4] + m1m2 * B2[4]) * eta.powi(4)
            + (B0[5] + m1 * B1[5] + m1m2 * B2[5]) * eta.powi(5)
            + (B0[6] + m1 * B1[6] + m1m2 * B2[6]) * eta.powi(6);
        let c = 1.0
            + 2.0 * self.m * (4.0 * eta - eta.powi(2)) / (1.0 - eta).powi(4)
            + (1.0 - self.m)
                * (20.0 * eta - 27.0 * eta.powi(2) + 12.0 * eta.powi(3) - 2.0 * eta.powi(4))
                / ((1.0 - eta) * (2.0 - eta)).powi(2);
        let c1 = 1.0 / c;
        let m2_epsilon1_sigma3 = self.m.powi(2) * (self.epsilon / T) * self.sigma.powi(3);
        let m2_epsilon2_sigma3 = self.m.powi(2) * (self.epsilon / T).powi(2) * self.sigma.powi(3);
        -2.0 * PI * D * i1 * m2_epsilon1_sigma3 - PI * D * self.m * c1 * i2 * m2_epsilon2_sigma3
    }
    pub fn calc_rT0D1(&self, T: f64, D: f64) -> f64 {
        let d = self.sigma * (1.0 - 0.12 * (-3.0 * self.epsilon / T).exp());
        let eta = PI / 6.0 * D * self.m * d.powi(3);
        let m1 = (self.m - 1.0) / self.m;
        let m1m2 = (self.m - 1.0) * (self.m - 2.0) / self.m.powi(2);
        let i1 = (A0[0] + m1 * A1[0] + m1m2 * A2[0])
            + (A0[1] + m1 * A1[1] + m1m2 * A2[1]) * eta
            + (A0[2] + m1 * A1[2] + m1m2 * A2[2]) * eta.powi(2)
            + (A0[3] + m1 * A1[3] + m1m2 * A2[3]) * eta.powi(3)
            + (A0[4] + m1 * A1[4] + m1m2 * A2[4]) * eta.powi(4)
            + (A0[5] + m1 * A1[5] + m1m2 * A2[5]) * eta.powi(5)
            + (A0[6] + m1 * A1[6] + m1m2 * A2[6]) * eta.powi(6);
        let i1_d1 = (A0[1] + m1 * A1[1] + m1m2 * A2[1]) * eta
            + (A0[2] + m1 * A1[2] + m1m2 * A2[2]) * 2.0 * eta.powi(2)
            + (A0[3] + m1 * A1[3] + m1m2 * A2[3]) * 3.0 * eta.powi(3)
            + (A0[4] + m1 * A1[4] + m1m2 * A2[4]) * 4.0 * eta.powi(4)
            + (A0[5] + m1 * A1[5] + m1m2 * A2[5]) * 5.0 * eta.powi(5)
            + (A0[6] + m1 * A1[6] + m1m2 * A2[6]) * 6.0 * eta.powi(6);
        let i2 = (B0[0] + m1 * B1[0] + m1m2 * B2[0])
            + (B0[1] + m1 * B1[1] + m1m2 * B2[1]) * eta
            + (B0[2] + m1 * B1[2] + m1m2 * B2[2]) * eta.powi(2)
            + (B0[3] + m1 * B1[3] + m1m2 * B2[3]) * eta.powi(3)
            + (B0[4] + m1 * B1[4] + m1m2 * B2[4]) * eta.powi(4)
            + (B0[5] + m1 * B1[5] + m1m2 * B2[5]) * eta.powi(5)
            + (B0[6] + m1 * B1[6] + m1m2 * B2[6]) * eta.powi(6);
        let i2_d1 = (B0[1] + m1 * B1[1] + m1m2 * B2[1]) * eta
            + (B0[2] + m1 * B1[2] + m1m2 * B2[2]) * 2.0 * eta.powi(2)
            + (B0[3] + m1 * B1[3] + m1m2 * B2[3]) * 3.0 * eta.powi(3)
            + (B0[4] + m1 * B1[4] + m1m2 * B2[4]) * 4.0 * eta.powi(4)
            + (B0[5] + m1 * B1[5] + m1m2 * B2[5]) * 5.0 * eta.powi(5)
            + (B0[6] + m1 * B1[6] + m1m2 * B2[6]) * 6.0 * eta.powi(6);
        let c = 1.0
            + 2.0 * self.m * (4.0 * eta - eta.powi(2)) / (1.0 - eta).powi(4)
            + (1.0 - self.m)
                * (20.0 * eta - 27.0 * eta.powi(2) + 12.0 * eta.powi(3) - 2.0 * eta.powi(4))
                / ((1.0 - eta) * (2.0 - eta)).powi(2);
        let c_d1 = eta
            * (4.0 * self.m * (-eta.powi(2) + 5.0 * eta + 2.0) / (1.0 - eta).powi(5)
                + 2.0 * (1.0 - self.m) * (eta.powi(3) + 6.0 * eta.powi(2) - 24.0 * eta + 20.0)
                    / ((1.0 - eta) * (2.0 - eta)).powi(3));
        let c1 = 1.0 / c;
        let c1_d1 = -c_d1 / c.powi(2);
        let m2_epsilon1_sigma3 = self.m.powi(2) * (self.epsilon / T) * self.sigma.powi(3);
        let m2_epsilon2_sigma3 = self.m.powi(2) * (self.epsilon / T).powi(2) * self.sigma.powi(3);
        -2.0 * PI * m2_epsilon1_sigma3 * D * (i1 + i1_d1)
            - PI * self.m * m2_epsilon2_sigma3 * D * (c1 * i2 + c1_d1 * i2 + c1 * i2_d1)
    }
    pub fn calc_rT0D2(&self, T: f64, D: f64) -> f64 {
        let d = self.sigma * (1.0 - 0.12 * (-3.0 * self.epsilon / T).exp());
        let eta = PI / 6.0 * D * self.m * d.powi(3);
        let m1 = (self.m - 1.0) / self.m;
        let m1m2 = (self.m - 1.0) * (self.m - 2.0) / self.m.powi(2);
        let i1_d1 = (A0[1] + m1 * A1[1] + m1m2 * A2[1]) * eta
            + (A0[2] + m1 * A1[2] + m1m2 * A2[2]) * 2.0 * eta.powi(2)
            + (A0[3] + m1 * A1[3] + m1m2 * A2[3]) * 3.0 * eta.powi(3)
            + (A0[4] + m1 * A1[4] + m1m2 * A2[4]) * 4.0 * eta.powi(4)
            + (A0[5] + m1 * A1[5] + m1m2 * A2[5]) * 5.0 * eta.powi(5)
            + (A0[6] + m1 * A1[6] + m1m2 * A2[6]) * 6.0 * eta.powi(6);
        let i1_d2 = (A0[2] + m1 * A1[2] + m1m2 * A2[2]) * 2.0 * eta.powi(2)
            + (A0[3] + m1 * A1[3] + m1m2 * A2[3]) * 2.0 * 3.0 * eta.powi(3)
            + (A0[4] + m1 * A1[4] + m1m2 * A2[4]) * 3.0 * 4.0 * eta.powi(4)
            + (A0[5] + m1 * A1[5] + m1m2 * A2[5]) * 4.0 * 5.0 * eta.powi(5)
            + (A0[6] + m1 * A1[6] + m1m2 * A2[6]) * 5.0 * 6.0 * eta.powi(6);
        let i2 = (B0[0] + m1 * B1[0] + m1m2 * B2[0])
            + (B0[1] + m1 * B1[1] + m1m2 * B2[1]) * eta
            + (B0[2] + m1 * B1[2] + m1m2 * B2[2]) * eta.powi(2)
            + (B0[3] + m1 * B1[3] + m1m2 * B2[3]) * eta.powi(3)
            + (B0[4] + m1 * B1[4] + m1m2 * B2[4]) * eta.powi(4)
            + (B0[5] + m1 * B1[5] + m1m2 * B2[5]) * eta.powi(5)
            + (B0[6] + m1 * B1[6] + m1m2 * B2[6]) * eta.powi(6);
        let i2_d1 = (B0[1] + m1 * B1[1] + m1m2 * B2[1]) * eta
            + (B0[2] + m1 * B1[2] + m1m2 * B2[2]) * 2.0 * eta.powi(2)
            + (B0[3] + m1 * B1[3] + m1m2 * B2[3]) * 3.0 * eta.powi(3)
            + (B0[4] + m1 * B1[4] + m1m2 * B2[4]) * 4.0 * eta.powi(4)
            + (B0[5] + m1 * B1[5] + m1m2 * B2[5]) * 5.0 * eta.powi(5)
            + (B0[6] + m1 * B1[6] + m1m2 * B2[6]) * 6.0 * eta.powi(6);
        let i2_d2 = (B0[2] + m1 * B1[2] + m1m2 * B2[2]) * 2.0 * eta.powi(2)
            + (B0[3] + m1 * B1[3] + m1m2 * B2[3]) * 2.0 * 3.0 * eta.powi(3)
            + (B0[4] + m1 * B1[4] + m1m2 * B2[4]) * 3.0 * 4.0 * eta.powi(4)
            + (B0[5] + m1 * B1[5] + m1m2 * B2[5]) * 4.0 * 5.0 * eta.powi(5)
            + (B0[6] + m1 * B1[6] + m1m2 * B2[6]) * 5.0 * 6.0 * eta.powi(6);
        let c = 1.0
            + 2.0 * self.m * (4.0 * eta - eta.powi(2)) / (1.0 - eta).powi(4)
            + (1.0 - self.m)
                * (20.0 * eta - 27.0 * eta.powi(2) + 12.0 * eta.powi(3) - 2.0 * eta.powi(4))
                / ((1.0 - eta) * (2.0 - eta)).powi(2);
        let c_d1 = eta
            * (4.0 * self.m * (-eta.powi(2) + 5.0 * eta + 2.0) / (1.0 - eta).powi(5)
                + 2.0 * (1.0 - self.m) * (eta.powi(3) + 6.0 * eta.powi(2) - 24.0 * eta + 20.0)
                    / ((1.0 - eta) * (2.0 - eta)).powi(3));
        let c_d2 = eta.powi(2)
            * (12.0 * self.m * (-eta.powi(2) + 6.0 * eta + 5.0) / (1.0 - eta).powi(6)
                + (6.0 * (1.0 - self.m))
                    * (-eta.powi(4) - 8.0 * eta.powi(3) + 48.0 * eta.powi(2) - 80.0 * eta + 44.0)
                    / ((1.0 - eta) * (2.0 - eta)).powi(4));
        let c1 = 1.0 / c;
        let c1_d1 = -c_d1 / c.powi(2);
        let c1_d2 = -(c_d2 * c - 2.0 * c_d1.powi(2)) / c.powi(3);
        let m2_epsilon1_sigma3 = self.m.powi(2) * (self.epsilon / T) * self.sigma.powi(3);
        let m2_epsilon2_sigma3 = self.m.powi(2) * (self.epsilon / T).powi(2) * self.sigma.powi(3);
        -2.0 * PI * m2_epsilon1_sigma3 * D * (2.0 * i1_d1 + i1_d2)
            - (PI * self.m * m2_epsilon2_sigma3 * D)
                * (2.0 * (c1_d1 * i2 + c1 * i2_d1) + c1_d2 * i2 + 2.0 * c1_d1 * i2_d1 + c1 * i2_d2)
    }
    pub fn calc_rT1D0(&self, T: f64, D: f64) -> f64 {
        let d = self.sigma * (1.0 - 0.12 * (-3.0 * self.epsilon / T).exp());
        let d_t = self.sigma * (-0.12 * (-3.0 * self.epsilon / T).exp()) * (3.0 * self.epsilon / T);
        let eta = PI / 6.0 * D * self.m * d.powi(3);
        let eta_t = PI / 2.0 * D * self.m * d.powi(2) * d_t;
        let m1 = (self.m - 1.0) / self.m;
        let m1m2 = (self.m - 1.0) * (self.m - 2.0) / self.m.powi(2);
        let i1 = (A0[0] + m1 * A1[0] + m1m2 * A2[0])
            + (A0[1] + m1 * A1[1] + m1m2 * A2[1]) * eta
            + (A0[2] + m1 * A1[2] + m1m2 * A2[2]) * eta.powi(2)
            + (A0[3] + m1 * A1[3] + m1m2 * A2[3]) * eta.powi(3)
            + (A0[4] + m1 * A1[4] + m1m2 * A2[4]) * eta.powi(4)
            + (A0[5] + m1 * A1[5] + m1m2 * A2[5]) * eta.powi(5)
            + (A0[6] + m1 * A1[6] + m1m2 * A2[6]) * eta.powi(6);
        let i1_t1 = (A0[1] + m1 * A1[1] + m1m2 * A2[1]) * eta_t
            + (A0[2] + m1 * A1[2] + m1m2 * A2[2]) * 2.0 * eta.powi(1) * eta_t
            + (A0[3] + m1 * A1[3] + m1m2 * A2[3]) * 3.0 * eta.powi(2) * eta_t
            + (A0[4] + m1 * A1[4] + m1m2 * A2[4]) * 4.0 * eta.powi(3) * eta_t
            + (A0[5] + m1 * A1[5] + m1m2 * A2[5]) * 5.0 * eta.powi(4) * eta_t
            + (A0[6] + m1 * A1[6] + m1m2 * A2[6]) * 6.0 * eta.powi(5) * eta_t;
        let i2 = (B0[0] + m1 * B1[0] + m1m2 * B2[0])
            + (B0[1] + m1 * B1[1] + m1m2 * B2[1]) * eta
            + (B0[2] + m1 * B1[2] + m1m2 * B2[2]) * eta.powi(2)
            + (B0[3] + m1 * B1[3] + m1m2 * B2[3]) * eta.powi(3)
            + (B0[4] + m1 * B1[4] + m1m2 * B2[4]) * eta.powi(4)
            + (B0[5] + m1 * B1[5] + m1m2 * B2[5]) * eta.powi(5)
            + (B0[6] + m1 * B1[6] + m1m2 * B2[6]) * eta.powi(6);
        let i2_t1 = (B0[1] + m1 * B1[1] + m1m2 * B2[1]) * eta_t
            + (B0[2] + m1 * B1[2] + m1m2 * B2[2]) * 2.0 * eta.powi(1) * eta_t
            + (B0[3] + m1 * B1[3] + m1m2 * B2[3]) * 3.0 * eta.powi(2) * eta_t
            + (B0[4] + m1 * B1[4] + m1m2 * B2[4]) * 4.0 * eta.powi(3) * eta_t
            + (B0[5] + m1 * B1[5] + m1m2 * B2[5]) * 5.0 * eta.powi(4) * eta_t
            + (B0[6] + m1 * B1[6] + m1m2 * B2[6]) * 6.0 * eta.powi(5) * eta_t;
        let c = 1.0
            + 2.0 * self.m * (4.0 * eta - eta.powi(2)) / (1.0 - eta).powi(4)
            + (1.0 - self.m)
                * (20.0 * eta - 27.0 * eta.powi(2) + 12.0 * eta.powi(3) - 2.0 * eta.powi(4))
                / ((1.0 - eta) * (2.0 - eta)).powi(2);
        let c_t1 = eta_t
            * (4.0 * self.m * (-eta.powi(2) + 5.0 * eta + 2.0) / (1.0 - eta).powi(5)
                + 2.0 * (1.0 - self.m) * (eta.powi(3) + 6.0 * eta.powi(2) - 24.0 * eta + 20.0)
                    / ((1.0 - eta) * (2.0 - eta)).powi(3));
        let c1 = 1.0 / c;
        let c1_t1 = -c_t1 / c.powi(2);
        let m2_epsilon1_sigma3 = self.m.powi(2) * (self.epsilon / T) * self.sigma.powi(3);
        let m2_epsilon1_sigma3_t1 = -self.m.powi(2) * (self.epsilon / T) * self.sigma.powi(3);
        let m2_epsilon2_sigma3 = self.m.powi(2) * (self.epsilon / T).powi(2) * self.sigma.powi(3);
        let m2_epsilon2_sigma3_t1 =
            -2.0 * self.m.powi(2) * (self.epsilon / T).powi(2) * self.sigma.powi(3);
        -2.0 * PI * D * (i1_t1 * m2_epsilon1_sigma3 + i1 * m2_epsilon1_sigma3_t1)
            - (PI * D * self.m)
                * (c1_t1 * i2 * m2_epsilon2_sigma3
                    + c1 * i2_t1 * m2_epsilon2_sigma3
                    + c1 * i2 * m2_epsilon2_sigma3_t1)
    }
    pub fn calc_rT1D1(&self, T: f64, D: f64) -> f64 {
        let d = self.sigma * (1.0 - 0.12 * (-3.0 * self.epsilon / T).exp());
        let d_t = self.sigma * (-0.12 * (-3.0 * self.epsilon / T).exp()) * (3.0 * self.epsilon / T);
        let eta = PI / 6.0 * D * self.m * d.powi(3);
        let eta_t = PI / 2.0 * D * self.m * d.powi(2) * d_t;
        let m1 = (self.m - 1.0) / self.m;
        let m1m2 = (self.m - 1.0) * (self.m - 2.0) / self.m.powi(2);
        let i1 = (A0[0] + m1 * A1[0] + m1m2 * A2[0])
            + (A0[1] + m1 * A1[1] + m1m2 * A2[1]) * eta
            + (A0[2] + m1 * A1[2] + m1m2 * A2[2]) * eta.powi(2)
            + (A0[3] + m1 * A1[3] + m1m2 * A2[3]) * eta.powi(3)
            + (A0[4] + m1 * A1[4] + m1m2 * A2[4]) * eta.powi(4)
            + (A0[5] + m1 * A1[5] + m1m2 * A2[5]) * eta.powi(5)
            + (A0[6] + m1 * A1[6] + m1m2 * A2[6]) * eta.powi(6);
        let i1_t1 = (A0[1] + m1 * A1[1] + m1m2 * A2[1]) * eta_t
            + (A0[2] + m1 * A1[2] + m1m2 * A2[2]) * 2.0 * eta.powi(1) * eta_t
            + (A0[3] + m1 * A1[3] + m1m2 * A2[3]) * 3.0 * eta.powi(2) * eta_t
            + (A0[4] + m1 * A1[4] + m1m2 * A2[4]) * 4.0 * eta.powi(3) * eta_t
            + (A0[5] + m1 * A1[5] + m1m2 * A2[5]) * 5.0 * eta.powi(4) * eta_t
            + (A0[6] + m1 * A1[6] + m1m2 * A2[6]) * 6.0 * eta.powi(5) * eta_t;
        let i1_d1 = (A0[1] + m1 * A1[1] + m1m2 * A2[1]) * eta
            + (A0[2] + m1 * A1[2] + m1m2 * A2[2]) * 2.0 * eta.powi(2)
            + (A0[3] + m1 * A1[3] + m1m2 * A2[3]) * 3.0 * eta.powi(3)
            + (A0[4] + m1 * A1[4] + m1m2 * A2[4]) * 4.0 * eta.powi(4)
            + (A0[5] + m1 * A1[5] + m1m2 * A2[5]) * 5.0 * eta.powi(5)
            + (A0[6] + m1 * A1[6] + m1m2 * A2[6]) * 6.0 * eta.powi(6);
        let i1_t1d1 = (A0[1] + m1 * A1[1] + m1m2 * A2[1]) * eta_t
            + (A0[2] + m1 * A1[2] + m1m2 * A2[2]) * 2.0_f64.powi(2) * eta.powi(1) * eta_t
            + (A0[3] + m1 * A1[3] + m1m2 * A2[3]) * 3.0_f64.powi(2) * eta.powi(2) * eta_t
            + (A0[4] + m1 * A1[4] + m1m2 * A2[4]) * 4.0_f64.powi(2) * eta.powi(3) * eta_t
            + (A0[5] + m1 * A1[5] + m1m2 * A2[5]) * 5.0_f64.powi(2) * eta.powi(4) * eta_t
            + (A0[6] + m1 * A1[6] + m1m2 * A2[6]) * 6.0_f64.powi(2) * eta.powi(5) * eta_t;
        let i2 = (B0[0] + m1 * B1[0] + m1m2 * B2[0])
            + (B0[1] + m1 * B1[1] + m1m2 * B2[1]) * eta
            + (B0[2] + m1 * B1[2] + m1m2 * B2[2]) * eta.powi(2)
            + (B0[3] + m1 * B1[3] + m1m2 * B2[3]) * eta.powi(3)
            + (B0[4] + m1 * B1[4] + m1m2 * B2[4]) * eta.powi(4)
            + (B0[5] + m1 * B1[5] + m1m2 * B2[5]) * eta.powi(5)
            + (B0[6] + m1 * B1[6] + m1m2 * B2[6]) * eta.powi(6);
        let i2_t1 = (B0[1] + m1 * B1[1] + m1m2 * B2[1]) * eta_t
            + (B0[2] + m1 * B1[2] + m1m2 * B2[2]) * 2.0 * eta.powi(1) * eta_t
            + (B0[3] + m1 * B1[3] + m1m2 * B2[3]) * 3.0 * eta.powi(2) * eta_t
            + (B0[4] + m1 * B1[4] + m1m2 * B2[4]) * 4.0 * eta.powi(3) * eta_t
            + (B0[5] + m1 * B1[5] + m1m2 * B2[5]) * 5.0 * eta.powi(4) * eta_t
            + (B0[6] + m1 * B1[6] + m1m2 * B2[6]) * 6.0 * eta.powi(5) * eta_t;
        let i2_d1 = (B0[1] + m1 * B1[1] + m1m2 * B2[1]) * eta
            + (B0[2] + m1 * B1[2] + m1m2 * B2[2]) * 2.0 * eta.powi(2)
            + (B0[3] + m1 * B1[3] + m1m2 * B2[3]) * 3.0 * eta.powi(3)
            + (B0[4] + m1 * B1[4] + m1m2 * B2[4]) * 4.0 * eta.powi(4)
            + (B0[5] + m1 * B1[5] + m1m2 * B2[5]) * 5.0 * eta.powi(5)
            + (B0[6] + m1 * B1[6] + m1m2 * B2[6]) * 6.0 * eta.powi(6);
        let i2_t1d1 = (B0[1] + m1 * B1[1] + m1m2 * B2[1]) * eta_t
            + (B0[2] + m1 * B1[2] + m1m2 * B2[2]) * 2.0_f64.powi(2) * eta.powi(1) * eta_t
            + (B0[3] + m1 * B1[3] + m1m2 * B2[3]) * 3.0_f64.powi(2) * eta.powi(2) * eta_t
            + (B0[4] + m1 * B1[4] + m1m2 * B2[4]) * 4.0_f64.powi(2) * eta.powi(3) * eta_t
            + (B0[5] + m1 * B1[5] + m1m2 * B2[5]) * 5.0_f64.powi(2) * eta.powi(4) * eta_t
            + (B0[6] + m1 * B1[6] + m1m2 * B2[6]) * 6.0_f64.powi(2) * eta.powi(5) * eta_t;
        let c = 1.0
            + 2.0 * self.m * (4.0 * eta - eta.powi(2)) / (1.0 - eta).powi(4)
            + (1.0 - self.m)
                * (20.0 * eta - 27.0 * eta.powi(2) + 12.0 * eta.powi(3) - 2.0 * eta.powi(4))
                / ((1.0 - eta) * (2.0 - eta)).powi(2);
        let c_t1 = eta_t
            * (4.0 * self.m * (-eta.powi(2) + 5.0 * eta + 2.0) / (1.0 - eta).powi(5)
                + 2.0 * (1.0 - self.m) * (eta.powi(3) + 6.0 * eta.powi(2) - 24.0 * eta + 20.0)
                    / ((1.0 - eta) * (2.0 - eta)).powi(3));
        let c_d1 = eta
            * (4.0 * self.m * (-eta.powi(2) + 5.0 * eta + 2.0) / (1.0 - eta).powi(5)
                + 2.0 * (1.0 - self.m) * (eta.powi(3) + 6.0 * eta.powi(2) - 24.0 * eta + 20.0)
                    / ((1.0 - eta) * (2.0 - eta)).powi(3));
        let c_t1d1 = (eta_t * eta)
            * (12.0 * self.m * (-eta.powi(2) + 6.0 * eta + 5.0) / (1.0 - eta).powi(6)
                + (6.0 * (1.0 - self.m))
                    * (-eta.powi(4) - 8.0 * eta.powi(3) + 48.0 * eta.powi(2) - 80.0 * eta + 44.0)
                    / ((1.0 - eta) * (2.0 - eta)).powi(4))
            + c_t1;
        let c1 = 1.0 / c;
        let c1_t1 = -c_t1 / c.powi(2);
        let c1_d1 = -c_d1 / c.powi(2);
        let c1_t1d1 = -(c_t1d1 * c - 2.0 * c_t1 * c_d1) / c.powi(3);
        let m2_epsilon1_sigma3 = self.m.powi(2) * (self.epsilon / T) * self.sigma.powi(3);
        let m2_epsilon1_sigma3_t1 = -self.m.powi(2) * (self.epsilon / T) * self.sigma.powi(3);
        let m2_epsilon2_sigma3 = self.m.powi(2) * (self.epsilon / T).powi(2) * self.sigma.powi(3);
        let m2_epsilon2_sigma3_t1 =
            -2.0 * self.m.powi(2) * (self.epsilon / T).powi(2) * self.sigma.powi(3);
        (-2.0 * PI * D)
            * (i1_t1 * m2_epsilon1_sigma3
                + i1 * m2_epsilon1_sigma3_t1
                + i1_t1d1 * m2_epsilon1_sigma3
                + i1_d1 * m2_epsilon1_sigma3_t1)
            - (PI * self.m * D)
                * (c1_t1 * i2 * m2_epsilon2_sigma3
                    + c1 * i2_t1 * m2_epsilon2_sigma3
                    + c1 * i2 * m2_epsilon2_sigma3_t1
                    + c1_t1d1 * i2 * m2_epsilon2_sigma3
                    + c1_d1 * i2_t1 * m2_epsilon2_sigma3
                    + c1_d1 * i2 * m2_epsilon2_sigma3_t1
                    + c1_t1 * i2_d1 * m2_epsilon2_sigma3
                    + c1 * i2_t1d1 * m2_epsilon2_sigma3
                    + c1 * i2_d1 * m2_epsilon2_sigma3_t1)
    }
    pub fn calc_rT2D0(&self, T: f64, D: f64) -> f64 {
        let d = self.sigma * (1.0 - 0.12 * (-3.0 * self.epsilon / T).exp());
        let d_t = self.sigma * (-0.12 * (-3.0 * self.epsilon / T).exp()) * (3.0 * self.epsilon / T);
        let d_tt = self.sigma
            * (-0.12 * (-3.0 * self.epsilon / T).exp())
            * (3.0 * self.epsilon / T)
            * (3.0 * self.epsilon / T - 2.0);
        let eta = PI / 6.0 * D * self.m * d.powi(3);
        let eta_t = PI / 2.0 * D * self.m * d.powi(2) * d_t;
        let eta_tt = PI / 2.0 * D * self.m * (2.0 * d * d_t.powi(2) + d.powi(2) * d_tt);
        let m1 = (self.m - 1.0) / self.m;
        let m1m2 = (self.m - 1.0) * (self.m - 2.0) / self.m.powi(2);
        let i1 = (A0[0] + m1 * A1[0] + m1m2 * A2[0])
            + (A0[1] + m1 * A1[1] + m1m2 * A2[1]) * eta
            + (A0[2] + m1 * A1[2] + m1m2 * A2[2]) * eta.powi(2)
            + (A0[3] + m1 * A1[3] + m1m2 * A2[3]) * eta.powi(3)
            + (A0[4] + m1 * A1[4] + m1m2 * A2[4]) * eta.powi(4)
            + (A0[5] + m1 * A1[5] + m1m2 * A2[5]) * eta.powi(5)
            + (A0[6] + m1 * A1[6] + m1m2 * A2[6]) * eta.powi(6);
        let i1_t1 = (A0[1] + m1 * A1[1] + m1m2 * A2[1]) * eta_t
            + (A0[2] + m1 * A1[2] + m1m2 * A2[2]) * 2.0 * eta.powi(1) * eta_t
            + (A0[3] + m1 * A1[3] + m1m2 * A2[3]) * 3.0 * eta.powi(2) * eta_t
            + (A0[4] + m1 * A1[4] + m1m2 * A2[4]) * 4.0 * eta.powi(3) * eta_t
            + (A0[5] + m1 * A1[5] + m1m2 * A2[5]) * 5.0 * eta.powi(4) * eta_t
            + (A0[6] + m1 * A1[6] + m1m2 * A2[6]) * 6.0 * eta.powi(5) * eta_t;
        let i1_t2 = (A0[1] + m1 * A1[1] + m1m2 * A2[1]) * eta_tt
            + (A0[2] + m1 * A1[2] + m1m2 * A2[2]) * 2.0 * (eta_t.powi(2) + eta_tt * eta)
            + (A0[3] + m1 * A1[3] + m1m2 * A2[3])
                * (3.0 * eta * (2.0 * eta_t.powi(2) + eta_tt * eta))
            + (A0[4] + m1 * A1[4] + m1m2 * A2[4])
                * (4.0 * eta.powi(2) * (3.0 * eta_t.powi(2) + eta_tt * eta))
            + (A0[5] + m1 * A1[5] + m1m2 * A2[5])
                * (5.0 * eta.powi(3) * (4.0 * eta_t.powi(2) + eta_tt * eta))
            + (A0[6] + m1 * A1[6] + m1m2 * A2[6])
                * (6.0 * eta.powi(4) * (5.0 * eta_t.powi(2) + eta_tt * eta));
        let i2 = (B0[0] + m1 * B1[0] + m1m2 * B2[0])
            + (B0[1] + m1 * B1[1] + m1m2 * B2[1]) * eta
            + (B0[2] + m1 * B1[2] + m1m2 * B2[2]) * eta.powi(2)
            + (B0[3] + m1 * B1[3] + m1m2 * B2[3]) * eta.powi(3)
            + (B0[4] + m1 * B1[4] + m1m2 * B2[4]) * eta.powi(4)
            + (B0[5] + m1 * B1[5] + m1m2 * B2[5]) * eta.powi(5)
            + (B0[6] + m1 * B1[6] + m1m2 * B2[6]) * eta.powi(6);
        let i2_t1 = (B0[1] + m1 * B1[1] + m1m2 * B2[1]) * eta_t
            + (B0[2] + m1 * B1[2] + m1m2 * B2[2]) * 2.0 * eta.powi(1) * eta_t
            + (B0[3] + m1 * B1[3] + m1m2 * B2[3]) * 3.0 * eta.powi(2) * eta_t
            + (B0[4] + m1 * B1[4] + m1m2 * B2[4]) * 4.0 * eta.powi(3) * eta_t
            + (B0[5] + m1 * B1[5] + m1m2 * B2[5]) * 5.0 * eta.powi(4) * eta_t
            + (B0[6] + m1 * B1[6] + m1m2 * B2[6]) * 6.0 * eta.powi(5) * eta_t;
        let i2_t2 = (B0[1] + m1 * B1[1] + m1m2 * B2[1]) * eta_tt
            + (B0[2] + m1 * B1[2] + m1m2 * B2[2]) * 2.0 * (eta_t.powi(2) + eta_tt * eta)
            + (B0[3] + m1 * B1[3] + m1m2 * B2[3])
                * (3.0 * eta * (2.0 * eta_t.powi(2) + eta_tt * eta))
            + (B0[4] + m1 * B1[4] + m1m2 * B2[4])
                * (4.0 * eta.powi(2) * (3.0 * eta_t.powi(2) + eta_tt * eta))
            + (B0[5] + m1 * B1[5] + m1m2 * B2[5])
                * (5.0 * eta.powi(3) * (4.0 * eta_t.powi(2) + eta_tt * eta))
            + (B0[6] + m1 * B1[6] + m1m2 * B2[6])
                * (6.0 * eta.powi(4) * (5.0 * eta_t.powi(2) + eta_tt * eta));
        let c = 1.0
            + 2.0 * self.m * (4.0 * eta - eta.powi(2)) / (1.0 - eta).powi(4)
            + (1.0 - self.m)
                * (20.0 * eta - 27.0 * eta.powi(2) + 12.0 * eta.powi(3) - 2.0 * eta.powi(4))
                / ((1.0 - eta) * (2.0 - eta)).powi(2);
        let c_t1 = eta_t
            * (4.0 * self.m * (-eta.powi(2) + 5.0 * eta + 2.0) / (1.0 - eta).powi(5)
                + 2.0 * (1.0 - self.m) * (eta.powi(3) + 6.0 * eta.powi(2) - 24.0 * eta + 20.0)
                    / ((1.0 - eta) * (2.0 - eta)).powi(3));
        let c_t2 = eta_t.powi(2)
            * (12.0 * self.m * (-eta.powi(2) + 6.0 * eta + 5.0) / (1.0 - eta).powi(6)
                + (6.0 * (1.0 - self.m))
                    * (-eta.powi(4) - 8.0 * eta.powi(3) + 48.0 * eta.powi(2) - 80.0 * eta + 44.0)
                    / ((1.0 - eta) * (2.0 - eta)).powi(4))
            + eta_tt
                * (4.0 * self.m * (-eta.powi(2) + 5.0 * eta + 2.0) / (1.0 - eta).powi(5)
                    + 2.0 * (1.0 - self.m) * (eta.powi(3) + 6.0 * eta.powi(2) - 24.0 * eta + 20.0)
                        / ((1.0 - eta) * (2.0 - eta)).powi(3));
        let c1 = 1.0 / c;
        let c1_t1 = -c_t1 / c.powi(2);
        let c1_t2 = -(c_t2 * c - 2.0 * c_t1.powi(2)) / c.powi(3);
        let m2_epsilon1_sigma3 = self.m.powi(2) * (self.epsilon / T) * self.sigma.powi(3);
        let m2_epsilon1_sigma3_t1 = -self.m.powi(2) * (self.epsilon / T) * self.sigma.powi(3);
        let m2_epsilon1_sigma3_t2 = 2.0 * self.m.powi(2) * (self.epsilon / T) * self.sigma.powi(3);
        let m2_epsilon2_sigma3 = self.m.powi(2) * (self.epsilon / T).powi(2) * self.sigma.powi(3);
        let m2_epsilon2_sigma3_t1 =
            -2.0 * self.m.powi(2) * (self.epsilon / T).powi(2) * self.sigma.powi(3);
        let m2_epsilon2_sigma3_t2 =
            6.0 * self.m.powi(2) * (self.epsilon / T).powi(2) * self.sigma.powi(3);
        (-2.0 * PI * D)
            * (i1_t2 * m2_epsilon1_sigma3
                + i1 * m2_epsilon1_sigma3_t2
                + 2.0 * i1_t1 * m2_epsilon1_sigma3_t1)
            - (PI * D * self.m)
                * (c1_t2 * i2 * m2_epsilon2_sigma3
                    + c1 * i2_t2 * m2_epsilon2_sigma3
                    + c1 * i2 * m2_epsilon2_sigma3_t2
                    + 2.0 * c1_t1 * i2_t1 * m2_epsilon2_sigma3
                    + 2.0 * c1_t1 * i2 * m2_epsilon2_sigma3_t1
                    + 2.0 * c1 * i2_t1 * m2_epsilon2_sigma3_t1)
    }
}
/// unit test
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    #[allow(non_snake_case)]
    fn test_pc_saft_disp() {
        let hc = AlphaDisp::new(1.6069, 3.5206, 191.42); // parameters for ethane
        let (T, Tx) = (300.0, 0.001);
        let (D, Dx) = (0.001, 0.0000001);
        let convergence_criteria_for_t = 1E-10; // convergence criteria equal to 1E-10
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
        );
    }
}

const A0: [f64; 7] = [
    0.9105631445,
    0.6361281449,
    2.6861347891,
    -26.547362491,
    97.759208784,
    -159.59154087,
    91.297774084,
];
const A1: [f64; 7] = [
    -0.3084016918,
    0.1860531159,
    -2.5030047259,
    21.419793629,
    -65.25588533,
    83.318680481,
    -33.74692293,
];
const A2: [f64; 7] = [
    -0.0906148351,
    0.4527842806,
    0.5962700728,
    -1.7241829131,
    -4.1302112531,
    13.77663187,
    -8.6728470368,
];
const B0: [f64; 7] = [
    0.7240946941,
    2.2382791861,
    -4.0025849485,
    -21.003576815,
    26.855641363,
    206.55133841,
    -355.60235612,
];
const B1: [f64; 7] = [
    -0.5755498075,
    0.6995095521,
    3.892567339,
    -17.215471648,
    192.67226447,
    -161.82646165,
    -165.20769346,
];
const B2: [f64; 7] = [
    0.0976883116,
    -0.2557574982,
    -9.155856153,
    20.642075974,
    -38.804430052,
    93.626774077,
    -29.666905585,
];
