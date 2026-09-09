#include "wafer_stage_x.hpp"

#include <cstdio>
#include <cstdlib>

// Canned 1 ms samples from scripts/mock_cycle.py (healthy + missed-heartbeat).

namespace {

using asml::mc::Fault;
using asml::mc::Sample;
using asml::mc::Setpoint;
using asml::mc::Stage;
using asml::mc::WaferStageX;

class FakeStage final : public Stage {
 public:
  Sample next{};
  Setpoint written{};
  bool read_ok = true;
  bool write_ok = true;
  bool did_write = false;

  bool read(Sample& out) noexcept override {
    if (!read_ok) return false;
    out = next;
    return true;
  }
  bool write(const Setpoint& in) noexcept override {
    if (!write_ok) return false;
    written = in;
    did_write = true;
    return true;
  }
};

int fail(const char* msg) {
  std::fprintf(stderr, "FAIL: %s\n", msg);
  return 1;
}

}  // namespace

int main() {
  WaferStageX mod{};
  if (!mod.init(150000000)) return fail("init");

  FakeStage fake{};
  fake.next.t_ns = 1000000;
  fake.next.pos_nm = 800;
  fake.next.vel_nm_s = 400000;

  Sample raw{};
  Sample est{};
  Setpoint cmd{};

  mod.heartbeat();
  if (!mod.sense(fake, raw)) return fail("sense");
  mod.last = raw;
  mod.estimate(raw, est);
  mod.control(est, /*cmd_pos_nm=*/1200, cmd);
  if (!mod.actuate(fake, cmd)) return fail("actuate healthy");
  if (fake.written.pos_nm != 1200 || fake.written.force_mN != 12)
    return fail("healthy setpoint != mock_cycle.py (1200 nm, 12 mN)");
  if (mod.heartbeat_count != 1) return fail("heartbeat");
  if (mod.fault != Fault::None) return fail("unexpected fault");

  // scripts/mock_cycle.py --inject-fault missed-heartbeat
  // safe state: hold last-good pos 800 nm, force 0.
  mod.flag_missed_heartbeat();
  fake.did_write = false;
  mod.control(est, 1200, cmd);
  if (mod.actuate(fake, cmd)) return fail("missed heartbeat should stick");
  if (mod.fault != Fault::MissedHeartbeat) return fail("sticky fault");
  if (!fake.did_write) return fail("safe-state write");
  if (fake.written.pos_nm != 800 || fake.written.force_mN != 0)
    return fail("safe hold != mock_cycle.py missed-heartbeat");

  std::printf("ok wafer-stage-x 1ms mock cycle\n");
  return 0;
}
