/// A Python module implemented in Rust.
use crate::{HelmholtzPure, PcSaftPure, PrPure};
enum Models {
    Helmholtz(Box<HelmholtzPure>),
    PcSaft(PcSaftPure),
    Pr(PrPure),
}
use crate::{Flash, Prop};
use pyo3::prelude::*;
#[pymodule]
#[pyo3(name = "thermolib")] // Rename pymodule
pub fn pylib(_py: Python, pm: &PyModule) -> PyResult<()> {
    // The name of this function must match the `lib.name` in the `Cargo.toml`,
    // else python will not be able to import the module.
    pm.add_class::<NewModel>()?;
    Ok(())
}
#[pyclass]
pub struct NewModel {
    model: Models,
}
#[pymethods]
#[allow(non_snake_case)]
impl NewModel {
    #[new]
    fn new(model: &str) -> Self {
        match model {
            "HELMHOLTZ" => NewModel {
                model: Models::Helmholtz(Box::new(
                    HelmholtzPure::read_json("SO2.json").expect("no SO2.json"),
                )),
            },
            "PCSAFT" => NewModel {
                model: Models::PcSaft(PcSaftPure::new_pc_saft(2.8611, 2.6826, 205.35, 64.065)),
            },
            "PR" => NewModel {
                model: Models::Pr(PrPure::new_pr(430.64, 7.8866E6, 8.314462618, 64.064, 0.256)),
            },
            _ => {
                println!("error input, use default = Helmholtz(SO2).");
                NewModel {
                    model: Models::Helmholtz(Box::new(
                        HelmholtzPure::read_json("SO2.json").expect("no SO2.json"),
                    )),
                }
            }
        }
    }
    fn t_flash(&mut self, Ts: f64) -> anyhow::Result<()> {
        match &mut self.model {
            Models::Helmholtz(model) => model.t_flash(Ts),
            Models::PcSaft(model) => model.t_flash(Ts),
            Models::Pr(model) => model.t_flash(Ts),
        }
    }
    fn td_flash(&mut self, T: f64, D: f64) -> anyhow::Result<()> {
        match &mut self.model {
            Models::Helmholtz(model) => model.td_flash(T, D),
            Models::PcSaft(model) => model.td_flash(T, D),
            Models::Pr(model) => model.td_flash(T, D),
        }
    }
    fn tp_flash(&mut self, T: f64, P: f64) -> anyhow::Result<()> {
        match &mut self.model {
            Models::Helmholtz(model) => model.tp_flash(T, P),
            Models::PcSaft(model) => model.tp_flash(T, P),
            Models::Pr(model) => model.tp_flash(T, P),
        }
    }
    fn T(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.T(),
            Models::PcSaft(model) => model.T(),
            Models::Pr(model) => model.T(),
        }
    }
    fn D(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.D(),
            Models::PcSaft(model) => model.D(),
            Models::Pr(model) => model.D(),
        }
    }
    fn p(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.p(),
            Models::PcSaft(model) => model.p(),
            Models::Pr(model) => model.p(),
        }
    }
    fn Dp_DT_D(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.Dp_DT_D(),
            Models::PcSaft(model) => model.Dp_DT_D(),
            Models::Pr(model) => model.Dp_DT_D(),
        }
    }
    fn Dp_DD_T(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.Dp_DD_T(),
            Models::PcSaft(model) => model.Dp_DD_T(),
            Models::Pr(model) => model.Dp_DD_T(),
        }
    }
    fn cv(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.cv(),
            Models::PcSaft(model) => model.cv(),
            Models::Pr(model) => model.cv(),
        }
    }
    fn cp(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.cp(),
            Models::PcSaft(model) => model.cp(),
            Models::Pr(model) => model.cp(),
        }
    }
    fn w(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.w(),
            Models::PcSaft(model) => model.w(),
            Models::Pr(model) => model.w(),
        }
    }
    fn s(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.s(),
            Models::PcSaft(model) => model.s(),
            Models::Pr(model) => model.s(),
        }
    }
    fn Ds_DT_D(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.Ds_DT_D(),
            Models::PcSaft(model) => model.Ds_DT_D(),
            Models::Pr(model) => model.Ds_DT_D(),
        }
    }
    fn Ds_DD_T(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.Ds_DD_T(),
            Models::PcSaft(model) => model.Ds_DD_T(),
            Models::Pr(model) => model.Ds_DD_T(),
        }
    }
    fn s_res(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.s_res(),
            Models::PcSaft(model) => model.s_res(),
            Models::Pr(model) => model.s_res(),
        }
    }
    fn u(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.u(),
            Models::PcSaft(model) => model.u(),
            Models::Pr(model) => model.u(),
        }
    }
    fn u_res(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.u_res(),
            Models::PcSaft(model) => model.u_res(),
            Models::Pr(model) => model.u_res(),
        }
    }
    fn h(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.h(),
            Models::PcSaft(model) => model.h(),
            Models::Pr(model) => model.h(),
        }
    }
    fn Dh_DT_D(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.Dh_DT_D(),
            Models::PcSaft(model) => model.Dh_DT_D(),
            Models::Pr(model) => model.Dh_DT_D(),
        }
    }
    fn Dh_DD_T(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.Dh_DD_T(),
            Models::PcSaft(model) => model.Dh_DD_T(),
            Models::Pr(model) => model.Dh_DD_T(),
        }
    }
    fn h_res(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.h_res(),
            Models::PcSaft(model) => model.h_res(),
            Models::Pr(model) => model.h_res(),
        }
    }
    fn a(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.a(),
            Models::PcSaft(model) => model.a(),
            Models::Pr(model) => model.a(),
        }
    }
    fn a_res(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.a_res(),
            Models::PcSaft(model) => model.a_res(),
            Models::Pr(model) => model.a_res(),
        }
    }
    fn g(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.g(),
            Models::PcSaft(model) => model.g(),
            Models::Pr(model) => model.g(),
        }
    }
    fn Dg_DT_D(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.Dg_DT_D(),
            Models::PcSaft(model) => model.Dg_DT_D(),
            Models::Pr(model) => model.Dg_DT_D(),
        }
    }
    fn Dg_DD_T(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.Dg_DD_T(),
            Models::PcSaft(model) => model.Dg_DD_T(),
            Models::Pr(model) => model.Dg_DD_T(),
        }
    }
    fn g_res(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.g_res(),
            Models::PcSaft(model) => model.g_res(),
            Models::Pr(model) => model.g_res(),
        }
    }
    fn Z(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.Z(),
            Models::PcSaft(model) => model.Z(),
            Models::Pr(model) => model.Z(),
        }
    }
    fn B(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.B(),
            Models::PcSaft(model) => model.B(),
            Models::Pr(model) => model.B(),
        }
    }
    fn C(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.C(),
            Models::PcSaft(model) => model.C(),
            Models::Pr(model) => model.C(),
        }
    }
    fn ps(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.ps(),
            Models::PcSaft(model) => model.ps(),
            Models::Pr(model) => model.ps(),
        }
    }
    fn Dgs(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.Dgs(),
            Models::PcSaft(model) => model.Dgs(),
            Models::Pr(model) => model.Dgs(),
        }
    }
    fn Dls(&self) -> anyhow::Result<f64> {
        match &self.model {
            Models::Helmholtz(model) => model.Dls(),
            Models::PcSaft(model) => model.Dls(),
            Models::Pr(model) => model.Dls(),
        }
    }
}
