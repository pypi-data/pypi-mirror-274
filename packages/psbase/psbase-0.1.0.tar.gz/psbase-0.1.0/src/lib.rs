use pyo3::prelude::*;
use std::env;
use std::fs;
use std::process::{Command, Stdio};

/// Nachricht ausgeben
#[pyfunction]
fn print(text: &str) -> PyResult<()> {
    println!("{}", text);
    Ok(())
}

/// Umgebungsvariable holen
#[pyfunction]
fn get_env(var: &str) -> PyResult<Option<String>> {
    let value = env::var(var).ok();
    Ok(value)
}

#[pyclass]
struct System;

#[pymethods]
impl System {
    #[new]
    fn new() -> Self {
        System
    }

    /// Befehl ausführen
    fn cmd(&self, command: &str) -> PyResult<()> {
        let output = if cfg!(target_os = "windows") {
            Command::new("cmd")
                .arg("/C")
                .arg(command)
                .stdout(Stdio::inherit())
                .stderr(Stdio::inherit())
                .output()
                .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("Fehler beim Ausführen des Befehls: {}", e)))?
        } else {
            Command::new("sh")
                .arg("-c")
                .arg(command)
                .stdout(Stdio::inherit())
                .stderr(Stdio::inherit())
                .output()
                .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("Fehler beim Ausführen des Befehls: {}", e)))?
        };

        if !output.status.success() {
            return Err(pyo3::exceptions::PyRuntimeError::new_err(format!("Befehl fehlgeschlagen: {}", output.status)));
        }

        Ok(())
    }

    /// Verzeichnis erstellen
    fn mkdir(&self, path: &str) -> PyResult<()> {
        fs::create_dir(path)
            .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("Fehler beim Erstellen des Verzeichnisses: {}", e)))?;
        Ok(())
    }

    /// Arbeitsverzeichnis wechseln
    fn cd(&self, path: &str) -> PyResult<()> {
        env::set_current_dir(path)
            .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("Fehler beim Wechseln des Verzeichnisses: {}", e)))?;
        Ok(())
    }

    /// Dateien im aktuellen Verzeichnis auflisten
    fn list_files(&self) -> PyResult<Vec<String>> {
        let paths = fs::read_dir(".")
            .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("Fehler beim Lesen des Verzeichnisses: {}", e)))?;
        
        let mut files = Vec::new();
        for path in paths {
            let path = path.map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("Fehler beim Lesen des Pfades: {}", e)))?;
            files.push(path.path().display().to_string());
        }
        Ok(files)
    }
}

/// Ein in Rust implementiertes Python-Modul.
#[pymodule]
fn psbase(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(print, m)?)?;
    m.add_function(wrap_pyfunction!(get_env, m)?)?;
    m.add_class::<System>()?;
    Ok(())
}