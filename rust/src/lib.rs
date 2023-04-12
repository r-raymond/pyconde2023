use pyo3::prelude::*;

#[pyclass]
#[derive(Clone)]
struct Vec {
    pub x: f32,
    pub y: f32,
    pub z: f32,
}

#[pymethods]
impl Vec {
    #[new]
    fn init(x: f32, y: f32, z: f32) -> Vec {
        Vec { x, y, z }
    }

    fn __add__(&self, other: &Vec) -> Vec {
        Vec {x: self.x + other.x, y: self.y + other.y, z: self.z + other.z} 
    }

    fn __sub__(&self, other: &Vec) -> Vec {
        Vec {x: self.x - other.x, y: self.y - other.y, z: self.z - other.z} 
    }

    fn __mul__(&self, other: &Vec) -> f32 {
        self.x * other.x + self.y * other.y + self.z * other.z
    }

    fn len(&self) -> f32 {
        self.__mul__(&self).sqrt()
    }

    fn scale(&self, fac: f32) -> Vec {
        Vec {x: self.x * fac, y: self.y * fac, z: self.z * fac}
    }

    fn normal(&self) -> Vec {
        self.scale(1.0 / self.len())
    }

    fn __repr__(&self) -> String {
        format!("({}, {}, {})", self.x, self.y, self.z)
    }
}

#[pyclass]
struct Sphere {
    pub center: Vec,
    pub radius: f32,
}

#[pymethods]
impl Sphere {
    #[new]
    fn init(center: &Vec, radius: f32) -> Sphere {
        Sphere {
            center: center.clone(), radius
        }
    }

    fn intersect(&self, line: &Line) -> Option<Vec> {
        let diff = line.start.__sub__(&self.center);
        let sp = line.dir.__mul__(&diff);

        let rat = 4. * (sp * sp - (diff.__mul__(&diff) - self.radius * self.radius));

        if rat < 0. {
            return None;
        }

        let sqrat = rat.sqrt() / 2.0;
        let t = (-1. * sp + sqrat).min(-1. * sp - sqrat);
        Some (line.start.__add__(&line.dir.scale(t)))
    }

    fn get_normal(&self, pos: &Vec) -> Vec {
        (pos.__sub__(&self.center)).normal()
    }
}

#[pyclass]
struct Line {
    pub start: Vec,
    pub dir: Vec,
}


#[pymethods]
impl Line {
    #[new]
    fn init(start: &Vec, dir: &Vec) -> Line {
        Line {
            start: start.clone(), dir: dir.clone()
        }
    }
}


/// A Python module implemented in Rust.
#[pymodule]
fn rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Vec>()?;
    m.add_class::<Sphere>()?;
    m.add_class::<Line>()?;
    Ok(())
}
