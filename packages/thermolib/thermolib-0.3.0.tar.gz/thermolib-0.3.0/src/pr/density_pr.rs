/// Calculate density using pr equation of state
/// Used to give guessed density for Alpha::tp_flash
#[allow(non_snake_case)]
pub fn calc_density_using_pr(T: f64, P: f64, Tc: f64, Pc: f64, R: f64, omega: f64) -> f64 {
    let kappa = 0.37464 + 1.54226 * omega - 0.26992 * omega.powi(2);
    let a = 0.45724 * R.powi(2) * Tc.powi(2) / Pc * (1.0 + kappa * (1.0 - (T / Tc).sqrt())).powi(2);
    let b = 0.07780 * R * Tc / Pc; // b=bc
    let A = a * P / R.powi(2) / T.powi(2);
    let B = b * P / R / T;
    // Solve the cubic equation
    let b = -(1.0 - B);
    let c = A - 3.0 * B.powi(2) - 2.0 * B;
    let d = -(A * B - B.powi(2) - B.powi(3));
    let A = b.powi(2) - 3.0 * c;
    let B = b * c - 9.0 * d;
    let C = c.powi(2) - 3.0 * b * d;
    let Delta = B.powi(2) - 4.0 * A * C;
    let Zg: f64;
    let mut Zl: f64 = 0.0;
    if Delta > 0.0 {
        let Y1 = A * b + 1.5 * (-B + Delta.sqrt());
        let Y2 = A * b + 1.5 * (-B - Delta.sqrt());
        Zg = (-b - (Y1.cbrt() + Y2.cbrt())) / 3.0;
    } else {
        let theta3 = ((2.0 * A * b - 3.0 * B) / (2.0 * A * A.sqrt())).acos() / 3.0;
        let x1 = (-b - 2.0 * A.sqrt() * theta3.cos()) / 3.0;
        let x2 = (-b + A.sqrt() * (theta3.cos() + f64::sqrt(3.0) * theta3.sin())) / 3.0;
        let x3 = (-b + A.sqrt() * (theta3.cos() - f64::sqrt(3.0) * theta3.sin())) / 3.0;
        Zg = x1.max(x2).max(x3);
        Zl = x1.min(x2).min(x3);
    }
    if Zl <= 0.0 {
        P / (Zg * R * T)
    } else {
        let lnfpg = (Zg - 1.0)
            - (Zg - B).ln()
            - A / (2.0 * f64::sqrt(2.0) * B) * ((Zg + 2.414 * B) / (Zg - 0.414 * B)).ln();
        let lnfpl = (Zl - 1.0)
            - (Zl - B).ln()
            - A / (2.0 * f64::sqrt(2.0) * B) * ((Zl + 2.414 * B) / (Zl - 0.414 * B)).ln();
        if lnfpg < lnfpl {
            P / (Zg * R * T)
        } else {
            P / (Zl * R * T)
        }
    }
}
