---
theme: seriph
background: https://images.unsplash.com/photo-1583147247730-0ffa2ee86d72?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80
---

# Rusty Python

A Case Study

<div class="pt-8">
    Robin Raymond &mdash; Taktile
</div>

<div class="abs-br m-6 flex gap-2">
  <a href="https://github.com/r-raymond/pyconde-2023" target="_blank" alt="GitHub"
    class="text-xl slidev-icon-btn opacity-50 !border-none !hover:text-white">
    Get the code <carbon-logo-github />
  </a>
</div>

---

# Table of Contents

## Part 1: Introduction
* A little intro about Rust
* Python <> Rust Tooling Overview

## Part 2: Let's speed up some Python code
* Quick intro into the code base
* Let's write some Rust to speed it up

## Part 3: A Case Study of using Rust to speed up Python 
* Problem Statement
* Approach Taken
* Outcome

---

# What is [Rust](https://www.rust-lang.org/)?


* **Modern** systems programming language
* Has similar **performance**[^1] and low-level control as C/C++
* Prioritizes **memory safety**, **thread safety**, and modern software engineering practices


[^1]: In theory [could be faster](https://www.reddit.com/r/rust/comments/px72r1/what_makes_rust_faster_than_cc/) than C/C++, in [practice](https://benchmarksgame-team.pages.debian.net/benchmarksgame/fastest/rust-gpp.html) often a bit slower.
---

## Some Things that Are Awesome About Rust

* Modern batteries-included tooling ([cargo](https://doc.rust-lang.org/cargo/))

```bash
cargo new
cargo build
cargo test
cargo doc
cargo publish
```

* Cross compilation support

```bash
> rustc --print target-list | head
aarch64-apple-darwin
aarch64-apple-ios
aarch64-apple-ios-macabi
aarch64-apple-ios-sim
aarch64-apple-tvos
aarch64-apple-watchos-sim
aarch64-fuchsia
aarch64-kmc-solid_asp3
aarch64-linux-android
aarch64-nintendo-switch-freestanding

> rustc --print target-list | wc -l
199
```

---

<div class="opacity-50">
Things that Are Awesome About Rust (cont.)
</div>

* Documentation [hosted versioned in a central place](https://docs.rs/pyo3/0.18.2/pyo3/), with cross links between packages


* Ownership Semantics
```rust
let s1 = String::from("hello");
let s2 = s1;

println!("{}, world!", s1);
```

```rust
--> src/main.rs:5:28
  |
2 |     let s1 = String::from("hello");
  |         -- move occurs because `s1` has type `String`, which does not implement the `Copy` trait
3 |     let s2 = s1;
  |              -- value moved here
4 |
5 |     println!("{}, world!", s1);
  |                            ^^ value borrowed here after move
```

---

<div class="opacity-50">
Things that Are Awesome About Rust (cont.)
</div>

* Lifetime Tracking
```rust {all|2|3-6|7|all}
fn main() {
    let r;
    {
        let x = 5;
        r = &x;
    }
    println!("r: {}", r);
}
```

<div v-click>
```rust
error[E0597]: `x` does not live long enough
 --> src/main.rs:6:13
  |
6 |         r = &x;
  |             ^^ borrowed value does not live long enough
7 |     }
  |     - `x` dropped here while still borrowed
8 |
9 |     println!("r: {}", r);
  |                       - borrow later used here
```
</div>

---

<div class="opacity-50">
Things that Are Awesome About Rust (cont.)
</div>

* Very expressive macro (compile time expression) system

<div v-click>
```rust
#[derive(Serialize, Deserialize)]
#[serde(tag = "type")]
enum Message {
    Request { id: String, method: String, params: Params },
    Response { id: String, result: Value },
}
```

```json
{"type": "Request", "id": "...", "method": "...", "params": {...}}
```
</div>

<div v-click>
```rust
struct Country { country: String, count: i64 }

let countries = sqlx::query_as!(Country,
        "
SELECT country, COUNT(*) as count
FROM users
GROUP BY country
WHERE organization = ?
        ",
        organization
    )
    .fetch_all(&pool) // -> Vec<Country>
    .await?;
```
</div>


---

### Some Things that Are Terrible About Rust

* Split 
* Compilation Time

* Compilation errors are sometimes hard to understand


---

## Python <> Rust Tooling Overview

<div class="py-4" v-click>
<h3>Bindings to Python</h3>
<li><a href="https://pyo3.rs/v0.18.2/">pyo</a>3</li>
<li><a href="https://cffi.readthedocs.io/en/latest/using.html">cffi</a> via <a href="https://github.com/rust-lang/rust-bindgen">bindgen</a></li>
<li><a href="https://github.com/dgrunwald/rust-cpython">rust-cpython</a></li>
<li><a href="https://mozilla.github.io/uniffi-rs/">uniffi</a></li>
</div>


<div class="py-4" v-click>
<h3>Setuptools Extensions</h3>
<ul>
<li><a href="https://www.maturin.rs/">Maturin</a> zero configuration</li>
<li><a href="https://github.com/PyO3/setuptools-rust">setuptools-rust</a> supports pyo3 and rust-cpython</li>
<li><a href="https://github.com/getsentry/milksnake">milksnake</a> not actively maintained</li>
</ul>
</div>

<div class="py-4" v-click>
<h3>Python Embeddings</h3>
<ul>
<li><a href="https://gregoryszorc.com/docs/pyoxidizer/main/">PyOxidizer</a></li>
</ul>
</div>

---



---
layout: two-cols-header
---


<template v-slot:default>

# 2. Let's Speed up some Python Code

<div class="flex">
<img src="/0.png" class="h-24 mx-4"/>
<img src="/1000.png" class="h-24 mx-4"/>
<img src="/2000.png" class="h-24 mx-4"/>
<img src="/3000.png" class="h-24 mx-4"/>
</div>

</template>

<template v-slot:left>
<div class="px-2">
```python
import pygame
import random
import time
import statistics

from python import Vec, Sphere, Line

pygame.init()
window = pygame.display.set_mode((800, 600))

run = True
window.fill(0)
times = []

def color(x, y):
  ...

```
</div>
</template>


<template v-slot:right>
<div class="px-2">
```python
start = 0

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for i in range(start, min(800 * 600, start + 200)):
        x = i % 800
        y = i // 800
        window.set_at((x, y), color(x, y))

    start += 200

    pygame.display.flip()

pygame.quit()
```
</div>
</template>

---
layout: image-right
image: /tracing.png
---

#### The Logic

```python
def color(x, y):
    screen_point = Vec(
        8.0 * x / 800, 6.0 * y / 600, 0.0)
    screen_dir = Vec(0.0, 0.0, 1.0)
    sphere = Vec(4.0, 3.0, 10.0)
    radius = 2.0
    light = Vec(8.0, 0.0, 7.0)

    line = Line(screen_point, screen_dir)
    sphere = Sphere(sphere, radius)

    intersect = sphere.intersect(line)

    if intersect is None:
        return (100, 100, 100)

    normal = sphere.get_normal(intersect)
    light_ray = (light - intersect).normal()

    return (
        max(int(normal * light_ray * 255), 30),
        0,
        0
    )
```


---
layout: two-cols-header
---
<template v-slot:left>
<div class="px-2">
```python
import math

class Vec:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vec(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )

    def __len__(self):
        return math.sqrt(self * self)

    def scale(self, fac):
        return Vec(
            self.x * fac,
            self.y * fac,
            self.z * fac
        )

    [...]
```
</div>
</template>
<template v-slot:right>
<div class="px-2">
```python
class Sphere:
    def __init__(self, q, r):
        self.q = q
        self.r = r

    def intersect(self, line):
        dif = line.p - self.q
        sp = line.v * dif
        rat = 4 * (sp * sp - (dif * dif - self.r**2))
        if rat >= 0:
            sqrat = math.sqrt(rat)
            t = min(
                -1 * sp + sqrat / 2, -1 * sp - sqrat / 2)
            return line.p + line.v.scale(t)
        else:
            return None

    def get_normal(self, p):
        dif = p - self.q
        return dif.normal()

class Line:
    def __init__(self, p, v):
        self.p = p
        self.v = v
```
</div>
</template>

---

#### Looking for the Bottleneck

```bash
python -m cProfile -o python.prof ray_trace.py
snakeviz python.prof
```

<img class="w-100" src="/python_snakeviz.png" />

---
layout: two-cols-header
---

#### Looking into more Detail

<template v-slot:left>
```python
times = []

def color(x, y):
    start = time.perf_counter_ns()

    [...]

    end = time.perf_counter_ns()
    times.append(end - start)
    return result

[...]

normal_dist = NormalDist.from_samples(times)
_, bins, _ = plt.hist(times, bins=100, density=True)
plt.plot(bins,
    scipy.stats.norm.pdf(
        bins, normal_dist.mean, normal_dist.stdev
  )
)
[...]

plt.xlim(0, 20000)
plt.savefig("performance.png")
```
</template>

<template v-slot:right>
<img src="/python_perf.png" />
</template>


---
layout: two-cols-header
---

#### Let's Write Some Rust

<template v-slot:left>
<div class="pr-2">
```bash
> maturin new rust
? 🤷 Which kind of bindings to use?
❯ pyo3
  rust-cpython
  cffi
  uniffi
  bin
📖 Documentation: https://maturin.rs/bindings.html · pyo3
✨ Done! New project created rust
```

```bash
> tree rust
rust
├── Cargo.toml
├── pyproject.toml
└── src
    └── lib.rs

1 directory, 3 files
```
</div>
</template>

<template v-slot:right>
```bash
> cat rust/pyprojet.toml
[build-system]
requires = ["maturin>=0.14,<0.15"]
build-backend = "maturin"

[project]
name = "rust"
requires-python = ">=3.7"
classifiers = [
"Programming Language::Rust",
"Programming Language::Python::Implementation::CPython",
"Programming Language::Python::Implementation::PyPy",
]


[tool.maturin]
features = ["pyo3/extension-module"]
```
</template>


---
layout: two-cols-header
---

#### Project is Adhering to PEP 517

<template v-slot:left>
<div class="pr-2">
```bash
> python -m build
* Creating venv isolated environment...
* Installing packages in isolated environment... (maturin>=0.14,<0.15)
* Getting build dependencies for sdist...
* Building sdist...
Running `maturin pep517 write-sdist --sdist-directory /home/robin/code/pyconde/rust/dist`
    Updating crates.io index
  Downloaded windows_i686_msvc v0.42.2
  [...]
  Downloaded 8 crates (4.2 MB) in 0.88s
🔗 Found pyo3 bindings
🐍 Found CPython 3.10 at /run/user/1000/build-env-2sml89ij/bin/python3
📡 Using build options features from pyproject.toml
⚠️  Warning: Attempting to include the sdist output tarball /home/robin/code/pyconde/rust/dist/test-0.1.0.tar.gz into itself! Check 'cargo package --list' output.
📦 Built source distribution to /home/robin/code/pyconde/rust/dist/test-0.1.0.tar.gz
rust-0.1.0.tar.gz
* Building wheel from sdist
* Creating venv isolated environment...
* Installing packages in isolated environment... (maturin>=0.14,<0.15)
* Getting build dependencies for wheel...
* Building wheel...
...
```
</div>
</template>

<template v-slot:right>
```bash
...
Running `maturin pep517 build-wheel -i /run/user/1000/build-env-4eylybhs/bin/python --compatibility off`
🔗 Found pyo3 bindings
🐍 Found CPython 3.10 at /run/user/1000/build-env-4eylybhs/bin/python
📡 Using build options features from pyproject.toml
   Compiling target-lexicon v0.12.6
   [...]
   Compiling pyo3-build-config v0.18.2
   Compiling parking_lot v0.12.1
   Compiling pyo3-ffi v0.18.2
   Compiling pyo3 v0.18.2
   Compiling pyo3-macros-backend v0.18.2
   Compiling pyo3-macros v0.18.2
   Compiling rust v0.1.0 (/run/user/1000/build-via-sdist-z39k_xis/test-0.1.0)
    Finished release [optimized] target(s) in 8.33s
📦 Built wheel for CPython 3.10 to /run/user/1000/build-via-sdist-z39k_xis/rust-0.1.0/target/wheels/test-0.1.0-cp310-cp310-linux_x86_64.whl
/run/user/1000/build-via-sdist-z39k_xis/rust-0.1.0/target/wheels/test-0.1.0-cp310-cp310-linux_x86_64.whl
Successfully built rust-0.1.0.tar.gz and test-0.1.0-cp310-cp310-linux_x86_64.whl
```
</template>
