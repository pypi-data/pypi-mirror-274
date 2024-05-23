#pragma once
#include "./quat.h"
#include "./vec3.h"

namespace sapien {

// TODO: unittests
struct Pose {
  inline CUDA_CALLABLE Pose() : q(1.f, 0.f, 0.f, 0.f), p(0.f, 0.f, 0.f) {}
  inline CUDA_CALLABLE Pose(Vec3 p_, Quat q_) : q(q_), p(p_) {}
  inline CUDA_CALLABLE explicit Pose(Vec3 p_) : q({1.f, 0.f, 0.f, 0.f}), p(p_) {}
  inline CUDA_CALLABLE explicit Pose(Quat q_) : q(q_), p({0.f, 0.f, 0.f}) {}

  inline CUDA_CALLABLE Pose getInverse() const {
    Quat q2 = q.getConjugate();
    return {q2.rotate(-p), q2};
  }
  inline CUDA_CALLABLE Vec3 operator*(Vec3 const &v) const { return q.rotate(v) + p; }
  inline CUDA_CALLABLE Pose operator*(Pose const &other) const {
    return {q.rotate(other.p) + p, q * other.q};
  }
  inline CUDA_CALLABLE Pose &operator*=(Pose const &other) {
    *this = *this * other;
    return *this;
  }

  inline CUDA_CALLABLE bool isSane() const { return p.isSane() && q.isSane(); }

  Quat q{1.f, 0.f, 0.f, 0.f};
  Vec3 p{0.f, 0.f, 0.f};
};

static_assert(sizeof(Pose) == 28);

static Pose const POSE_GL_TO_ROS({0, 0, 0}, {-0.5, -0.5, 0.5, 0.5});
static Pose const POSE_ROS_TO_GL({0, 0, 0}, {-0.5, 0.5, -0.5, -0.5});

} // namespace sapien
