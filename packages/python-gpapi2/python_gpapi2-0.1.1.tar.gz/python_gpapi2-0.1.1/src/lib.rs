use gpapi::error::ErrorKind as GpapiErrorKind;
use gpapi::Gpapi;
use once_cell::sync::Lazy;
use pyo3::prelude::*;

pub static TOKIO_RUNTIME: Lazy<tokio::runtime::Runtime> = Lazy::new(|| {
    tokio::runtime::Builder::new_multi_thread()
        .worker_threads(1)
        .enable_all()
        .build()
        .expect("Failed to create tokio runtime")
});

#[pymodule]
fn gpapi2(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<GooglePlayAPI>()?;

    Ok(())
}

#[pyclass]
struct GooglePlayAPI {
    pub gpapi: Gpapi,
}

#[pymethods]
impl GooglePlayAPI {
    /// Create a new GooglePlayAPI instance.
    #[new]
    #[pyo3(signature = (email, device_code = "px_7a"))]
    pub fn new(email: &str, device_code: Option<&str>) -> Self {
        let device_code = device_code.unwrap_or("px_7a");

        GooglePlayAPI {
            gpapi: Gpapi::new(device_code, email),
        }
    }

    /// Login to Google Play API using the provided AAS token.
    /// This method will also accept the terms of service if needed.
    /// Returns None if the login was successful, otherwise an error.
    ///
    /// See project README for more information on how to obtain the AAS token.
    #[pyo3(signature = (aas_token))]
    pub fn login(&mut self, aas_token: &str) -> PyResult<()> {
        self.gpapi.set_aas_token(aas_token);

        Python::with_gil(|_py| {
            TOKIO_RUNTIME.block_on(async move {
                if let Err(err) = self.gpapi.login().await {
                    match err.kind() {
                        GpapiErrorKind::TermsOfService => {
                            // try to accept the terms of service
                            if let Err(err) = self.gpapi.accept_tos().await {
                                let py_err = PyErr::new::<pyo3::exceptions::PyOSError, _>(format!(
                                    "GooglePlayAPI::login failed: could not accept TOS: {:?}",
                                    err
                                ));
                                return Err(py_err);
                            }
                            // and then try to login again
                            if let Err(err) = self.gpapi.login().await {
                                let py_err = PyErr::new::<pyo3::exceptions::PyOSError, _>(format!(
                                    "GooglePlayAPI::login failed: tos accepted but login failed: {:?}",
                                    err
                                ));
                                return Err(py_err);
                            }
                        }
                        _ => {
                            let py_err = PyErr::new::<pyo3::exceptions::PyOSError, _>(format!(
                                "GooglePlayAPI::login failed: {:?}",
                                err
                            ));
                            return Err(py_err);
                        }
                    }
                }

                Ok::<_, PyErr>(())
            })
        })?;

        Ok(())
    }

    /// Get the details of an app by its package name.
    /// Returns None if the app was not found, otherwise a JSON string with the app details.
    /// The JSON string can be converted to a Python dict using the json module.
    ///
    /// Example:
    /// ```python
    /// import json
    /// from gpapi2 import GooglePlayAPI
    ///
    /// gpapi = GooglePlayAPI("...")
    /// gpapi.login("...")
    /// details_json = gpapi.details("com.example.app")
    /// details = json.loads(details_json)
    /// ```
    #[pyo3(signature = (package))]
    fn details(&self, package: &str) -> PyResult<Option<String>> {
        Python::with_gil(|_py| {
            let details = TOKIO_RUNTIME.block_on(async move {
                match self.gpapi.details(package).await {
                    Ok(app_details) => Ok(app_details),
                    Err(err) => {
                        let py_err = PyErr::new::<pyo3::exceptions::PyOSError, _>(format!(
                            "GooglePlayAPI::app_details failed: {:?}",
                            err
                        ));
                        return Err(py_err);
                    }
                }
            })?;
            match details {
                None => Ok::<_, PyErr>(None),
                // convert app details to a PyDictObject
                Some(details) => Ok(Some(serde_json::to_string(&details.item).unwrap())),
            }
        })
    }

    #[pyo3(signature = (package))]
    fn latest_version(&self, package: &str) -> PyResult<(Option<String>, Option<i32>)> {
        Python::with_gil(|_py| {
            TOKIO_RUNTIME.block_on(async move {
                let details = match self.gpapi.details(package).await {
                    Ok(details) => details,
                    Err(err) => {
                        let py_err = PyErr::new::<pyo3::exceptions::PyOSError, _>(format!(
                            "GooglePlayAPI::app_details failed: {:?}",
                            err
                        ));
                        return Err(py_err);
                    }
                };
                if let Some(details) = details {
                    if let Some(item) = details.item {
                        if let Some(details) = item.details {
                            if let Some(app_details) = details.app_details {
                                return Ok((app_details.version_string, app_details.version_code));
                            }
                        }
                    }
                };
                Ok::<_, PyErr>((None, None))
            })
        })
    }

    /// Get the download URL of an app by its package name and version code.
    /// Returns None if the app was not found, otherwise the download URL.
    #[pyo3(signature = (package, version_code))]
    fn download_url(&self, package: &str, version_code: i32) -> PyResult<Option<String>> {
        Python::with_gil(|_py| {
            let download_url = TOKIO_RUNTIME.block_on(async move {
                match self
                    .gpapi
                    .get_download_info(package, Some(version_code))
                    .await
                {
                    Ok(download_info) => Ok(download_info.0),
                    Err(err) => {
                        let py_err = PyErr::new::<pyo3::exceptions::PyOSError, _>(format!(
                            "GooglePlayAPI::download_url failed: {:?}",
                            err
                        ));
                        return Err(py_err);
                    }
                }
            })?;
            Ok(download_url)
        })
    }

    /// Request an AAS token using the provided email and OAuth token.
    /// Returns the AAS token if successful, otherwise an error.
    ///
    /// See project README for more information on how to obtain the AAS token.
    #[staticmethod]
    #[pyo3(signature = (email, oauth_token))]
    fn request_aas_token(email: &str, oauth_token: &str) -> PyResult<String> {
        Python::with_gil(|_py| {
            TOKIO_RUNTIME.block_on(async move {
                let mut gpapi = Gpapi::new("px_7a", email);

                if let Err(err) = gpapi.request_aas_token(oauth_token).await {
                    let py_err = PyErr::new::<pyo3::exceptions::PyOSError, _>(format!(
                        "GooglePlayAPI::request_aas_token failed: {:?}\nPlease provide new OAuth token and try again.",
                        err
                    ));
                    return Err(py_err);
                };

                match gpapi.get_aas_token() {
                    Some(aas_token) => return Ok(aas_token.to_string()),
                    None => {
                        let py_err = PyErr::new::<pyo3::exceptions::PyOSError, _>(
                            "GooglePlayAPI::request_aas_token failed: request_aas_token succeeded but get_aas_token returned None",
                        );
                        return Err(py_err);
                    }
                }
            })
        })
    }
}
