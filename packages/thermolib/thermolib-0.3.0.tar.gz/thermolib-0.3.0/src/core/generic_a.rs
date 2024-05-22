use super::{CalcAi, CalcAr, Flash, Prop, TlErr};
use anyhow::anyhow;
use serde::{Deserialize, Serialize};
/// Phase enum of fluid state, so for it's limited to pure-component.
#[allow(non_snake_case)]
#[derive(Debug)]
pub enum Phase {
    /// + One-phase region of fluid, 2 independent variables is required.
    /// + T(Temperature) and D(Density).
    One { T: f64, D: f64 },
    /// + Two-phase region of fluid, 1 independent variables is required.
    /// + Ts(Temperature of Saturated Phase).
    /// + Dg(Density of Saturated Gas), Dl(Density of Saturated Liquid), X(Quality).
    Two { Ts: f64, Dg: f64, Dl: f64, X: f64 },
}
/// Generic struct of fundumental helmholtz equation of state.
#[allow(non_snake_case)]
#[derive(Serialize, Deserialize, Debug)]
pub struct GenericA<I: CalcAi, R: CalcAr> {
    ai: I,
    ar: R,
    R: f64,
    M: f64,
    #[serde(skip, default = "default_phase")]
    phase: Phase,
}
fn default_phase() -> Phase {
    Phase::One { T: 1.0, D: 1.0 }
}
/// Get internal fields of generic struct
#[allow(non_snake_case)]
impl<I: CalcAi, R: CalcAr> GenericA<I, R> {
    pub fn new(ai: I, ar: R, M: f64) -> Self {
        GenericA {
            ai,
            ar,
            M,
            R: 8.314462618,
            phase: Phase::One { T: 1.0, D: 1.0 },
        }
    }
    pub fn mut_ref_ai(&mut self) -> &mut I {
        &mut self.ai
    }
    pub fn mut_ref_ar(&mut self) -> &mut R {
        &mut self.ar
    }
    pub fn ref_ar(&self) -> &R {
        &self.ar
    }
    pub fn ref_phase(&self) -> &Phase {
        &self.phase
    }
    pub fn set_phase(&mut self, phase: Phase) {
        self.phase = phase;
    }
    pub fn R(&self) -> f64 {
        self.R
    }
}
/// Calculate partial derivatives of fundumental helmholtz equation of state.  
/// Equal to $$ T^(dT) * D^(dD) * A_DT(dT)_DD(dD) $$  
/// Used to calculate thermodynamic properties.  
#[allow(non_snake_case)]
impl<I: CalcAi, R: CalcAr> GenericA<I, R> {
    /// > fn aT0D0(&self, T: f64, D: f64) -> f64; Equal to
    /// > $$a\left(T,D\right)
    /// > =a^i\left(T,D\right)
    /// > +a^r\left(T,D\right)
    /// > =iT0(T)+RT\ln D+rT0D0(T,D)$$
    fn aT0D0(&self, T: f64, D: f64) -> f64 {
        self.ai.iT0(T) + self.R * T * D.ln() + self.ar.rT0D0(T, D)
    }
    /// > fn aT0D1(&self, T: f64, D: f64) -> f64; Equal to
    /// > $$D\left(\frac{\partial a}{\partial D}\right)_T
    /// > =D\left(\frac{\partial a^i}{\partial D}\right)_T
    /// > +D\left(\frac{\partial a^r}{\partial D}\right)_T
    /// > =RT+rT0D1(T,D)$$
    fn aT0D1(&self, T: f64, D: f64) -> f64 {
        self.R * T + self.ar.rT0D1(T, D)
    }
    /// > fn aT0D2(&self, T: f64, D: f64) -> f64; Equal to
    /// > $$D^2\left(\frac{\partial^2a}{\partial D^2}\right)_T
    /// > =D^2\left(\frac{\partial^2a^i}{\partial D^2}\right)_T
    /// > +D^2\left(\frac{\partial^2a^r}{\partial D^2}\right)_T
    /// > =-RT+rT0D2(T,D)$$
    fn aT0D2(&self, T: f64, D: f64) -> f64 {
        -self.R * T + self.ar.rT0D2(T, D)
    }
    /// > fn aT1D0(&self, T: f64, D: f64) -> f64; Equal to
    /// > $$T\left(\frac{\partial a}{\partial T}\right)_D
    /// > =T\left(\frac{\partial a^i}{\partial T}\right)_D
    /// > +T\left(\frac{\partial a^r}{\partial T}\right)_D
    /// > =iT1(T)+RT\ln D+rT1D0(T,D)$$
    fn aT1D0(&self, T: f64, D: f64) -> f64 {
        self.ai.iT1(T) + self.R * T * D.ln() + self.ar.rT1D0(T, D)
    }
    /// > fn aT1D1(&self, T: f64, D: f64) -> f64; Equal to
    /// > $$TD\left(\frac{\partial^2a}{\partial T\partial D}\right)
    /// > =TD\left(\frac{\partial^2a^i}{\partial T\partial D}\right)
    /// > +TD\left(\frac{\partial^2a^r}{\partial T\partial D}\right)
    /// > =RT+rT1D1(T,D)$$
    fn aT1D1(&self, T: f64, D: f64) -> f64 {
        self.R * T + self.ar.rT1D1(T, D)
    }
    /// > fn aT2D0(&self, T: f64, D: f64) -> f64; Equal to
    /// > $$T^2\left(\frac{\partial^2a}{\partial T^2}\right)_D
    /// > =T^2\left(\frac{\partial^2a^i}{\partial T^2}\right)_D
    /// > +T^2\left(\frac{\partial^2a^r}{\partial T^2}\right)_D
    /// > =iT2(T)+rT2D0(T,D)$$
    fn aT2D0(&self, T: f64, D: f64) -> f64 {
        self.ai.iT2(T) + self.ar.rT2D0(T, D)
    }
}
/// Calculate thermodynamic properties of fundumental helmholtz equation of state.
#[allow(non_snake_case)]
impl<I: CalcAi, R: CalcAr> GenericA<I, R> {
    /// > $$p
    /// > =D^2\left(\frac{\partial a}{\partial D}\right)_T$$
    fn p(&self, T: f64, D: f64) -> f64 {
        D * self.aT0D1(T, D)
    }
    /// > $$Dp\\_DT\\_D=\left(\frac{\partial p}{\partial T}\right)_D
    /// > =D^2\left(\frac{\partial^2a}{\partial D\partial T}\right)$$
    fn Dp_DT_D(&self, T: f64, D: f64) -> f64 {
        D * self.aT1D1(T, D) / T
    }
    /// > $$Dp\\_DD\\_T=\left(\frac{\partial p}{\partial D}\right)_T
    /// > =2D\left(\frac{\partial a}{\partial D}\right)_T
    /// > +D^2\left(\frac{\partial^2a}{\partial D^2}\right)_T$$
    fn Dp_DD_T(&self, T: f64, D: f64) -> f64 {
        2.0 * self.aT0D1(T, D) + self.aT0D2(T, D)
    }
    /// > $$c_v
    /// > =-T\left(\frac{\partial^2a}{\partial T^2}\right)_D$$
    fn cv(&self, T: f64, D: f64) -> f64 {
        -self.aT2D0(T, D) / T
    }
    /// > $$c_p
    /// > =-T\left(\frac{\partial^2a}{\partial T^2}\right)_D
    /// > +TD\left(\frac{\partial^2a}{\partial T\partial D}\right)^2
    /// > \left[2\left(\frac{\partial a}{\partial D}\right)_T
    /// > +D\left(\frac{\partial^2a}{\partial D^2}\right)_T\right]^{-1}$$
    fn cp(&self, T: f64, D: f64) -> f64 {
        -self.aT2D0(T, D) / T
            + self.aT1D1(T, D).powi(2) / T / (2.0 * self.aT0D1(T, D) + self.aT0D2(T, D))
    }
    /// > $$w
    /// > =2D\left(\frac{\partial a}{\partial D}\right)_T
    /// > +D^2\left(\frac{\partial^2a}{\partial D^2}\right)
    /// > -D^2\left(\frac{\partial^2a}{\partial D\partial T}\right)^2
    /// > \left(\frac{\partial^2a}{\partial T^2}\right)^{-1}$$
    fn w(&self, T: f64, D: f64) -> f64 {
        let w2 =
            2.0 * self.aT0D1(T, D) + self.aT0D2(T, D) - self.aT1D1(T, D).powi(2) / self.aT2D0(T, D);
        if self.R < 10.0 {
            (w2 / self.M).sqrt()
        } else {
            w2.sqrt()
        }
    }
    /// > $$s
    /// > =-\left(\frac{\partial a}{\partial T}\right)_D$$
    fn s(&self, T: f64, D: f64) -> f64 {
        -self.aT1D0(T, D) / T
    }
    /// > $$Ds\\_DT\\_D=\left(\frac{\partial s}{\partial T}\right)_D
    /// > =-\left(\frac{\partial^2a}{\partial T^2}\right)_D$$
    fn Ds_DT_D(&self, T: f64, D: f64) -> f64 {
        -self.aT2D0(T, D) / T.powi(2)
    }
    /// > $$Ds\\_DD\\_T=\left(\frac{\partial s}{\partial D}\right)_T
    /// > =-\left(\frac{\partial^2a}{\partial T\partial D}\right)$$
    fn Ds_DD_T(&self, T: f64, D: f64) -> f64 {
        -self.aT1D1(T, D) / T / D
    }
    /// > $$s\\_res
    /// > =-\left(\frac{\partial a^r}{\partial T}\right)_D$$
    fn s_res(&self, T: f64, D: f64) -> f64 {
        -self.ar.rT1D0(T, D) / T
    }
    /// > $$u
    /// > =a\left(T,D\right)
    /// > -T\left(\frac{\partial a}{\partial T}\right)_D$$
    fn u(&self, T: f64, D: f64) -> f64 {
        self.aT0D0(T, D) - self.aT1D0(T, D)
    }
    /// > $$u\\_res
    /// > =a^r\left(T,D\right)
    /// > -T\left(\frac{\partial a^r}{\partial T}\right)_D$$
    fn u_res(&self, T: f64, D: f64) -> f64 {
        self.ar.rT0D0(T, D) - self.ar.rT1D0(T, D)
    }
    /// > $$h
    /// > =a\left(T,D\right)
    /// > -T\left(\frac{\partial a}{\partial T}\right)_D
    /// > +D\left(\frac{\partial a}{\partial D}\right)_T$$
    fn h(&self, T: f64, D: f64) -> f64 {
        self.aT0D0(T, D) - self.aT1D0(T, D) + self.aT0D1(T, D)
    }
    /// > $$Dh\\_DT\\_D=\left(\frac{\partial h}{\partial T}\right)
    /// > =-T\left(\frac{\partial^2a}{\partial T^2}\right)_D
    /// > +D\left(\frac{\partial^2a}{\partial D\partial T}\right)$$
    fn Dh_DT_D(&self, T: f64, D: f64) -> f64 {
        (-self.aT2D0(T, D) + self.aT1D1(T, D)) / T
    }
    /// > $$Dh\\_DD\\_T=\left(\frac{\partial h}{\partial D}\right)_T
    /// > =2\left(\frac{\partial a}{\partial D}\right)_T
    /// > -T\left(\frac{\partial^2a}{\partial T\partial D}\right)
    /// > +D\left(\frac{\partial^2a}{\partial D^2}\right)_T$$
    fn Dh_DD_T(&self, T: f64, D: f64) -> f64 {
        (2.0 * self.aT0D1(T, D) - self.aT1D1(T, D) + self.aT0D2(T, D)) / D
    }
    /// > $$h\\_res
    /// > =a^r\left(T,D\right)
    /// > -T\left(\frac{\partial a^r}{\partial T}\right)_D
    /// > +D\left(\frac{\partial a^r}{\partial D}\right)_T$$
    fn h_res(&self, T: f64, D: f64) -> f64 {
        self.ar.rT0D0(T, D) - self.ar.rT1D0(T, D) + self.ar.rT0D1(T, D)
    }
    /// > $$a
    /// > =a\left(T,D\right)$$
    fn a(&self, T: f64, D: f64) -> f64 {
        self.aT0D0(T, D)
    }
    /// > $$a\\_res
    /// > =a^r\left(T,D\right)$$
    fn a_res(&self, T: f64, D: f64) -> f64 {
        self.ar.rT0D0(T, D)
    }
    /// > $$g
    /// > =a\left(T,D\right)
    /// > +D\left(\frac{\partial a}{\partial D}\right)_T$$
    fn g(&self, T: f64, D: f64) -> f64 {
        self.aT0D0(T, D) + self.aT0D1(T, D)
    }
    /// > $$Dg\\_DT\\_D=\left(\frac{\partial g}{\partial T}\right)_D
    /// > =\left(\frac{\partial a}{\partial T}\right)_D
    /// > +D\left(\frac{\partial^2a}{\partial D\partial T}\right)$$
    fn Dg_DT_D(&self, T: f64, D: f64) -> f64 {
        (self.aT1D0(T, D) + self.aT1D1(T, D)) / T
    }
    /// > $$Dg\\_DD\\_T=\left(\frac{\partial g}{\partial D}\right)_T
    /// > =2\left(\frac{\partial a}{\partial D}\right)
    /// > +D\left(\frac{\partial^2a}{\partial D^2}\right)_T$$
    fn Dg_DD_T(&self, T: f64, D: f64) -> f64 {
        (2.0 * self.aT0D1(T, D) + self.aT0D2(T, D)) / D
    }
    /// > $$g\\_res
    /// > =a^r\left(T,D\right)
    /// > +D\left(\frac{\partial a^r}{\partial D}\right)_T$$
    fn g_res(&self, T: f64, D: f64) -> f64 {
        self.ar.rT0D0(T, D) + self.ar.rT0D1(T, D)
    }
    /// > $$Z
    /// > =\frac{1}{RT}D\left(\frac{\partial a}{\partial D}\right)_T$$
    fn Z(&self, T: f64, D: f64) -> f64 {
        self.aT0D1(T, D) / self.R() / T
    }
    /// > $$B
    /// > =\frac{1}{RT}\left(\frac{\partial a^r}{\partial D}\right)_T$$
    fn B(&self, T: f64, _D: f64) -> f64 {
        let D = 1E-16;
        self.ar.rT0D1(T, D) / D / self.R / T
    }
    /// > $$C
    /// > =\frac{1}{RT}\left(\frac{\partial^2a^r}{\partial D^2}\right)_T$$
    fn C(&self, T: f64, _D: f64) -> f64 {
        let D = 1E-16;
        self.ar.rT0D2(T, D) / D.powi(2) / self.R / T
    }
}
/// Flash calculation of fundumental helmholtz equation of state.
#[allow(non_snake_case)]
impl<I: CalcAi, R: CalcAr> Flash for GenericA<I, R> {
    /// Critical point
    fn c_flash(&mut self) -> anyhow::Result<()> {
        Err(anyhow!(TlErr::NoImplementation))
    }
    /// Temperature of saturated state
    fn t_flash(&mut self, _Ts: f64) -> anyhow::Result<()> {
        Err(anyhow!(TlErr::NoImplementation))
    }
    /// Temperature and Density
    fn td_flash(&mut self, T: f64, D: f64) -> anyhow::Result<()> {
        self.phase = Phase::One { T, D };
        Ok(())
    }
    /// Temperature and Pressure
    fn tp_flash(&mut self, _T: f64, _P: f64) -> anyhow::Result<()> {
        Err(anyhow!(TlErr::NoImplementation))
    }
}
/// Get thermodynamic properties of corresponding fluid phase.
#[allow(non_snake_case)]
impl<I: CalcAi, R: CalcAr> Prop for GenericA<I, R> {
    fn T(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, .. } => Ok(T),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn D(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { D, .. } => Ok(D),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn p(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.p(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn Dp_DT_D(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.Dp_DT_D(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn Dp_DD_T(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.Dp_DD_T(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn cv(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.cv(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn cp(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.cp(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn w(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.w(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn s(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.s(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn Ds_DT_D(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.Ds_DT_D(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn Ds_DD_T(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.Ds_DD_T(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn s_res(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.s_res(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn u(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.u(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn u_res(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.u_res(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn h(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.h(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn Dh_DT_D(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.Dh_DT_D(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn Dh_DD_T(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.Dh_DD_T(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn h_res(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.h_res(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn a(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.a(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn a_res(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.a_res(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn g(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.g(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn Dg_DT_D(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.Dg_DT_D(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn Dg_DD_T(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.Dg_DD_T(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn g_res(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.g_res(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn Z(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.Z(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn B(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.B(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn C(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { T, D } => Ok(self.C(T, D)),
            Phase::Two { .. } => Err(anyhow!(TlErr::NotInTwoPhase)),
        }
    }
    fn ps(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { .. } => Err(anyhow!(TlErr::NotInOnePhase)),
            Phase::Two { Ts, Dg, Dl, .. } => Ok(self.p(Ts, Dg) / 2.0 + self.p(Ts, Dl) / 2.0),
        }
    }
    fn Dgs(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { .. } => Err(anyhow!(TlErr::NotInOnePhase)),
            Phase::Two { Dg, .. } => Ok(Dg),
        }
    }
    fn Dls(&self) -> anyhow::Result<f64> {
        match self.phase {
            Phase::One { .. } => Err(anyhow!(TlErr::NotInOnePhase)),
            Phase::Two { Dl, .. } => Ok(Dl),
        }
    }
}
