---
name: asml-embedded-control
description: >
  Real-time C++ conventions for ASML TWINSCAN NXE/EXE machine control and mechatronics.
  Use when writing or reviewing scanner control code, servo loops, stage motion, wafer-handler
  coordination, or any module that must meet a deterministic cycle budget. Triggers: /asml-control-module,
  "asml embedded", "twinscan control", "nxe control", "mechatronics", "servo loop", "wafer stage".
---

# ASML embedded machine control

Mock skill. Do not call production scanner APIs. Use the fictional `asml::mc` types below as the coding shape.

## When to load

Any C++ change on a control path: wafer stage, reticle stage, projection optics actuators, wafer handler, or the module that coordinates them.

## Cycle budget

| Path | Budget | Allowed |
|---|---|---|
| Inner servo (stage/optics) | ≤ 250 µs | stack, preallocated buffers, integer/fixed math |
| Machine cycle | 1 ms | same, plus lock-free SPSC queues |
| Supervisory | 10–100 ms | allocations OK, never on the two paths above |

If the user does not state a budget, assume **1 ms machine cycle** and treat anything in the called function as inner-loop until proven otherwise.

## Module shape

Every mechatronic module is four stages, one translation unit each:

1. **Sense** — copy hardware registers into a POD sample. No filtering here.
2. **Estimate** — observers / Kalman-style filters. No I/O.
3. **Control** — compute setpoints. Pure function of estimate + command.
4. **Actuate** — write setpoints to hardware. Clamp to the interlock envelope from `asml-motion-safety`.

Fictional types (replace with the repo's real names when they exist):

```cpp
namespace asml::mc {
  struct Sample { uint64_t t_ns; int32_t pos_nm; int32_t vel_nm_s; };
  struct Setpoint { int32_t pos_nm; int32_t force_mN; };
  class Stage {
   public:
    bool read(Sample& out) noexcept;
    bool write(const Setpoint& in) noexcept;
  };
}
```

Units are SI with nanometre positions. Do not invent counts-per-encoder-tick in new code; convert at the driver boundary.

## Hot-path rules

- `noexcept` on sense/control/actuate. No exceptions, RTTI, or `dynamic_cast` on those paths.
- No `new`/`malloc`/STL node containers after `init()`. Use `std::array` or a caller-owned buffer.
- No mutexes on the inner servo. Cross-thread data is a lock-free SPSC queue sized at init.
- No logging, `printf`, or file I/O inside the cycle. Publish a counter; the diagnostics path reads it.
- No blocking syscalls. If a driver `read()` can block, it does not belong here — flag it.

## Init vs run

`init()` may allocate, load calibration, and fail. After `start()`, the only allowed failure mode is a sticky fault flag consumed by the safety layer. Do not add retry loops on the cycle.

## Review checklist

When editing or reviewing control C++:

1. Name the cycle this function runs on.
2. Confirm no allocation, locks, or I/O on that path.
3. Confirm setpoints are clamped (see `asml-motion-safety`).
4. Confirm units and timestamp source (`t_ns` monotonic).
