use thiserror::Error;
/// All errors may be returned in thermolib
#[derive(Error, Debug)]
pub enum TlErr {
    #[error("no implementation")]
    NoImplementation,
    #[error("c_flash diverge")]
    NotConvForC,
    #[error("t_flash diverge")]
    NotConvForT,
    #[error("td_flash diverge")]
    NotConvForTD,
    #[error("tp_flash diverge")]
    NotConvForTP,
    /// + Some property only make sence in two-phase, like ps, rhogs, rhols.
    /// + so it's not be implemented for one-phase.
    #[error("not in one phase")]
    NotInOnePhase,
    /// + Some property only make sence in one-phase, like speed of sound...
    /// + so it's not be implemented for two-phase.
    #[error("not in two phase")]
    NotInTwoPhase,

    /// no fluid.json file
    #[error("no fluid.json")]
    NoJson,
    /// no helmholtz
    #[error("no helmholtz")]
    NoHelmholtz,
}
