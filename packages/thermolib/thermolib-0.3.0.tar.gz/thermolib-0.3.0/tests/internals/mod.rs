/// Internal module
use thermolib::HelmholtzPure;
use thermolib::Prop;
fn compare_eq(f64_short: f64, f64_long: f64) {
    let string_short = f64_short.to_string();
    let length = match string_short.rfind(".") {
        Some(index) => (string_short.len() - index - 1) as i32,
        None => 0,
    };
    let round_long = (f64_long * 10_f64.powi(length)).round() / 10_f64.powi(length);
    assert_eq!(f64_short, round_long);
}
#[allow(non_snake_case)]
pub struct VerificationValue {
    T: f64,
    D: f64,
    P: f64,
    CV: f64,
    CP: f64,
    W: f64,
}
#[allow(non_snake_case)]
impl VerificationValue {
    pub fn new(T: f64, D: f64, P: f64, CV: f64, CP: f64, W: f64) -> VerificationValue {
        VerificationValue { T, D, P, CV, CP, W }
    }
}
pub fn verify_fluid(fluid: &mut HelmholtzPure, values: &Vec<VerificationValue>) {
    for value in values.iter() {
        fluid.td_flash(value.T, value.D).unwrap();
        compare_eq(value.P, fluid.p().unwrap());
        compare_eq(value.CV, fluid.cv().unwrap());
        compare_eq(value.CP, fluid.cp().unwrap());
        compare_eq(value.W, fluid.w().unwrap());
        if value.P != 0.0 {
            fluid.tp_flash(value.T, value.P).unwrap();
            compare_eq(value.D, fluid.D().unwrap());
        }
    }
}
