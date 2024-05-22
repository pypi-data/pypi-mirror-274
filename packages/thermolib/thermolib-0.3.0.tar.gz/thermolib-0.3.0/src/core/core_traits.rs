/// Partial derivatives of ideal part of fundumental helmholtz equation of state.  
/// Equal to $$ T^(dT) * D^(dD) * Ai_DT(dT)_DD(dD) $$
#[allow(non_snake_case)]
pub trait CalcAi {
    /// > fn iT0(&self, _T: f64) -> f64; Equal to =  
    /// > $$a^i\left(T,D\right)-RT\ln D$$  
    /// > fn iT0D1(&self, _T:f64) -> f64; Equal to = $+RT$  
    /// > fn iT0D2(&self, _T:f64) -> f64; Equal to = $-RT$  
    fn iT0(&self, _T: f64) -> f64 {
        println!("no implementation for CalcAi::iT0(), return 0.0");
        0.0
    }
    /// > fn iT1(&self, _T: f64) -> f64; Equal to =  
    /// > $$T\left(\frac{\partial a^i}{\partial T}\right)_D-RT\ln D$$  
    /// > fn iT1D1(&self, _T:f64) -> f64; Equal to = $+RT$  
    /// > fn iT1D2(&self, _T:f64) -> f64; Equal to = $-RT$  
    fn iT1(&self, _T: f64) -> f64 {
        println!("no implementation for CalcAi::iT1(), return 0.0");
        0.0
    }
    /// > fn iT2(&self, _T: f64) -> f64; Equal to =  
    /// > $$T^2\left(\frac{\partial^2a^i}{\partial T^2}\right)_D$$  
    /// > fn iT2D1(&self, _T:f64) -> f64; Equal to = $0$  
    /// > fn iT2D2(&self, _T:f64) -> f64; Equal to = $0$  
    fn iT2(&self, _T: f64) -> f64 {
        println!("no implementation for CalcAi::iT2(), return 0.0");
        0.0
    }
}
/// Partial derivatives of residual part of fundumental helmholtz equation of state.  
/// Equal to $$ T^(dT) * D^(dD) * Ar_DT(dT)_DD(dD) $$
#[allow(non_snake_case)]
pub trait CalcAr {
    /// > fn rT0D0(&self, _T: f64, _D: f64) -> f64; Equal to =  
    /// > $$a^r\left(T,D\right)$$  
    fn rT0D0(&self, _T: f64, _D: f64) -> f64 {
        println!("no implementation for CalcAr::rT0D0(), return 0.0");
        0.0
    }
    /// > fn rT0D1(&self, _T: f64, _D: f64) -> f64; Equal to =  
    /// > $$D\left(\frac{\partial a^r}{\partial D}\right)_T$$  
    fn rT0D1(&self, _T: f64, _D: f64) -> f64 {
        println!("no implementation for CalcAr::rT0D1(), return 0.0");
        0.0
    }
    /// > fn rT0D2(&self, _T: f64, _D: f64) -> f64; Equal to =  
    /// > $$D^2\left(\frac{\partial^2a^r}{\partial D^2}\right)_T$$  
    fn rT0D2(&self, _T: f64, _D: f64) -> f64 {
        println!("no implementation for CalcAr::rT0D2(), return 0.0");
        0.0
    }
    /// > fn rT1D0(&self, _T: f64, _D: f64) -> f64; Equal to =  
    /// > $$T\left(\frac{\partial a^r}{\partial T}\right)_D$$  
    fn rT1D0(&self, _T: f64, _D: f64) -> f64 {
        println!("no implementation for CalcAr::rT1D0(), return 0.0");
        0.0
    }
    /// > fn rT1D1(&self, _T: f64, _D: f64) -> f64; Equal to =  
    /// > $$TD\left(\frac{\partial^2a^r}{\partial T\partial D}\right)$$  
    fn rT1D1(&self, _T: f64, _D: f64) -> f64 {
        println!("no implementation for CalcAr::rT1D1(), return 0.0");
        0.0
    }
    /// > fn rT2D0(&self, _T: f64, _D: f64) -> f64; Equal to =  
    /// > $$T^2\left(\frac{\partial^2a^r}{\partial T^2}\right)_D$$  
    fn rT2D0(&self, _T: f64, _D: f64) -> f64 {
        println!("no implementation for CalcAr::rT2D0(), return 0.0");
        0.0
    }
}
/// Flash calculation of fundumental helmholtz equation of state.
#[allow(non_snake_case)]
pub trait Flash {
    /// Critical point
    fn c_flash(&mut self) -> anyhow::Result<()>;
    /// Temperature of saturated state
    fn t_flash(&mut self, _Ts: f64) -> anyhow::Result<()>;
    /// Temperature and Density
    fn td_flash(&mut self, _T: f64, _D: f64) -> anyhow::Result<()>;
    /// Temperature and Pressure
    fn tp_flash(&mut self, _T: f64, _P: f64) -> anyhow::Result<()>;
}
/// Get thermodynamic properties of corresponding fluid phase.
#[allow(non_snake_case)]
pub trait Prop {
    /// Temperature
    fn T(&self) -> anyhow::Result<f64>;
    /// Density
    fn D(&self) -> anyhow::Result<f64>;
    /// pressure
    fn p(&self) -> anyhow::Result<f64>;
    fn Dp_DT_D(&self) -> anyhow::Result<f64>;
    fn Dp_DD_T(&self) -> anyhow::Result<f64>;
    /// isochoric heat capacity
    fn cv(&self) -> anyhow::Result<f64>;
    /// isobaric heat capacity
    fn cp(&self) -> anyhow::Result<f64>;
    /// sound speed
    fn w(&self) -> anyhow::Result<f64>;
    /// entropy
    fn s(&self) -> anyhow::Result<f64>;
    fn Ds_DT_D(&self) -> anyhow::Result<f64>;
    fn Ds_DD_T(&self) -> anyhow::Result<f64>;
    fn s_res(&self) -> anyhow::Result<f64>;
    /// internal energy
    fn u(&self) -> anyhow::Result<f64>;
    fn u_res(&self) -> anyhow::Result<f64>;
    /// enthalpy
    fn h(&self) -> anyhow::Result<f64>;
    fn Dh_DT_D(&self) -> anyhow::Result<f64>;
    fn Dh_DD_T(&self) -> anyhow::Result<f64>;
    fn h_res(&self) -> anyhow::Result<f64>;
    /// helmholtz energy
    fn a(&self) -> anyhow::Result<f64>;
    fn a_res(&self) -> anyhow::Result<f64>;
    /// gibbs energy
    fn g(&self) -> anyhow::Result<f64>;
    fn Dg_DT_D(&self) -> anyhow::Result<f64>;
    fn Dg_DD_T(&self) -> anyhow::Result<f64>;
    fn g_res(&self) -> anyhow::Result<f64>;
    /// compressibility factor
    fn Z(&self) -> anyhow::Result<f64>;
    /// second virial coefficient
    fn B(&self) -> anyhow::Result<f64>;
    /// third virial coefficient
    fn C(&self) -> anyhow::Result<f64>;
    /// vapor pressure
    fn ps(&self) -> anyhow::Result<f64>;
    /// saturated gas density
    fn Dgs(&self) -> anyhow::Result<f64>;
    /// saturated liquid density
    fn Dls(&self) -> anyhow::Result<f64>;
}
