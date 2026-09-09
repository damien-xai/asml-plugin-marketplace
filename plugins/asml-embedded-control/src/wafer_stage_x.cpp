#include "wafer_stage_x.hpp"

#include <cstdlib>

namespace asml {
namespace mc {

namespace {

constexpr int32_t kDefaultTravelNm = 150000000;  // ±150 mm software stop
constexpr int32_t kForceM_N = 12;

int32_t clamp_pos(int32_t pos, int32_t limit) noexcept {
  if (pos > limit) return limit;
  if (pos < -limit) return -limit;
  return pos;
}

Setpoint safe_hold(const Sample& last) noexcept {
  // Horizontal axis: hold last-good position, remove force.
  Setpoint s;
  s.pos_nm = last.pos_nm;
  s.force_mN = 0;
  return s;
}

}  // namespace

bool WaferStageX::init(int32_t limit_nm) noexcept {
  travel_limit_nm = limit_nm > 0 ? limit_nm : kDefaultTravelNm;
  last.t_ns = 0;
  last.pos_nm = 0;
  last.vel_nm_s = 0;
  last_setpoint.pos_nm = 0;
  last_setpoint.force_mN = 0;
  heartbeat_count = 0;
  fault = Fault::None;
  started = true;
  return true;
}

void WaferStageX::heartbeat() noexcept { ++heartbeat_count; }

void WaferStageX::flag_missed_heartbeat() noexcept {
  fault = Fault::MissedHeartbeat;
}

void WaferStageX::reset() noexcept {
  // Supervisory only, after the plant is verified idle.
  fault = Fault::None;
}

bool WaferStageX::sense(Stage& stage, Sample& out) noexcept {
  if (!stage.read(out)) {
    fault = Fault::Driver;
    return false;
  }
  return true;
}

void WaferStageX::estimate(const Sample& in, Sample& out) noexcept { out = in; }

void WaferStageX::control(const Sample& est, int32_t cmd_pos_nm,
                          Setpoint& out) noexcept {
  (void)est;
  out.pos_nm = cmd_pos_nm;
  out.force_mN = kForceM_N;
}

bool WaferStageX::actuate(Stage& stage, const Setpoint& cmd) noexcept {
  Setpoint out = cmd;
  if (fault != Fault::None) {
    out = safe_hold(last);
  } else if (std::abs(cmd.pos_nm) > travel_limit_nm) {
    fault = Fault::TravelLimit;
    out = safe_hold(last);
  } else {
    out.pos_nm = clamp_pos(cmd.pos_nm, travel_limit_nm);
  }

  if (!stage.write(out)) {
    fault = Fault::Driver;
    return false;
  }
  last_setpoint = out;
  return fault == Fault::None;
}

}  // namespace mc
}  // namespace asml
