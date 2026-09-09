#pragma once

// Mock TWINSCAN wafer-stage X module. Not a production scanner API.

#include <cstdint>

namespace asml {
namespace mc {

struct Sample {
  uint64_t t_ns;
  int32_t pos_nm;
  int32_t vel_nm_s;
};

struct Setpoint {
  int32_t pos_nm;
  int32_t force_mN;
};

class Stage {
 public:
  virtual ~Stage() = default;
  virtual bool read(Sample& out) noexcept = 0;
  virtual bool write(const Setpoint& in) noexcept = 0;
};

enum class Fault : uint32_t {
  None = 0,
  TravelLimit = 1,
  Driver = 2,
  MissedHeartbeat = 3,
};

struct WaferStageX {
  int32_t travel_limit_nm;
  Sample last;
  Setpoint last_setpoint;
  uint32_t heartbeat_count;
  Fault fault;
  bool started;

  bool init(int32_t travel_limit_nm) noexcept;
  void heartbeat() noexcept;
  bool sense(Stage& stage, Sample& out) noexcept;
  void estimate(const Sample& in, Sample& out) noexcept;
  void control(const Sample& est, int32_t cmd_pos_nm, Setpoint& out) noexcept;
  bool actuate(Stage& stage, const Setpoint& cmd) noexcept;
  void flag_missed_heartbeat() noexcept;
  void reset() noexcept;
};

}  // namespace mc
}  // namespace asml
