from __future__ import annotations

import torch
from typing import TYPE_CHECKING
from isaaclab.managers import SceneEntityCfg
if TYPE_CHECKING:
    from isaaclab.envs import ManagerBasedRLEnv


def gait_phase(env: ManagerBasedRLEnv, period: float) -> torch.Tensor:
    if not hasattr(env, "episode_length_buf"):
        env.episode_length_buf = torch.zeros(env.num_envs, device=env.device, dtype=torch.long)

    global_phase = (env.episode_length_buf * env.step_dt) % period / period

    phase = torch.zeros(env.num_envs, 2, device=env.device)
    phase[:, 0] = torch.sin(global_phase * torch.pi * 2.0)
    phase[:, 1] = torch.cos(global_phase * torch.pi * 2.0)
    return phase

def lidar(
        env: ManagerBasedRLEnv,
        sensor_cfg: SceneEntityCfg,
        normalize: bool = True
) -> torch.Tensor:
    
    sensor = env.scene.sensors[sensor_cfg.name]

    hits = sensor.data.ray_hits_w
    origins = sensor.data.pos_w.unsqueeze(1)

    distances = torch.linalg.norm(hits - origins, dim = -1)
    distances = torch.nan_to_num(distances, nan=sensor.cfg.max_distance,)

    if normalize:
        distances = (distances / sensor.cfg.max_distance)

    return distances

def masked_lidar(
        env: ManagerBasedRLEnv,
        sensor_cfg: SceneEntityCfg,
        command_name: str = "base_velocity",
        asset_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
        normalize: bool = True,
        thresh_vel: float = 0.2
) -> torch.Tensor:
    
    "Masks LiDAR scan as an observation until progress becomes lower than a threshold"

    asset = env.scene[asset_cfg.name]    
    sensor = env.scene.sensors[sensor_cfg.name]

    hits = sensor.data.ray_hits_w
    origins = sensor.data.pos_w.unsqueeze(1)

    distances = torch.linalg.norm(hits - origins, dim = -1)
    distances = torch.nan_to_num(distances, nan=sensor.cfg.max_distance,)

    if normalize:
        distances = (distances / sensor.cfg.max_distance)

    cmd = env.command_manager.get_command(command_name)
    cmd_vel = torch.linalg.norm(cmd[:, :2], dim=1)

    cmd_dir = cmd[:, :2] / (torch.linalg.norm(cmd[:, :2], dim=1, keepdim=True) + 1e-6)

    robot_vel = asset.data.root_lin_vel_b[:, :2]
    lin_vel = torch.sum(robot_vel * cmd_dir,dim=1)
    lin_vel = torch.clamp(lin_vel,min=0.0)

    use_lidar = ((cmd_vel > 0.1) & (lin_vel < thresh_vel))
    use_lidar = use_lidar.unsqueeze(1)

    return torch.where(use_lidar, distances, torch.zeros_like(distances))


def masked_voxel_lidar(
        env: ManagerBasedRLEnv,
        sensor_cfg: SceneEntityCfg,
        num_bins: float,
        command_name: str = "base_velocity",
        asset_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
        normalize: bool = True,
        thresh_vel: float = 0.2
) -> torch.Tensor:
    
    "Masks LiDAR scan as an observation until progress becomes lower than a threshold"

    asset = env.scene[asset_cfg.name]    
    sensor = env.scene.sensors[sensor_cfg.name]

    distances = sensor.data.voxel_distances

    if normalize:
        distances = (distances / sensor.cfg.max_distance)

    cmd = env.command_manager.get_command(command_name)
    cmd_vel = torch.linalg.norm(cmd[:, :2], dim=1)

    cmd_dir = cmd[:, :2] / (torch.linalg.norm(cmd[:, :2], dim=1, keepdim=True) + 1e-6)

    robot_vel = asset.data.root_lin_vel_b[:, :2]
    lin_vel = torch.sum(robot_vel * cmd_dir,dim=1)
    lin_vel = torch.clamp(lin_vel,min=0.0)

    use_lidar = ((cmd_vel > 0.1) & (lin_vel < thresh_vel))
    use_lidar = use_lidar.unsqueeze(1)

    masked = torch.where(use_lidar, distances, torch.zeros_like(distances))

    num_envs, num_rays = masked.shape
    rays_per_bin = num_rays // num_bins
    
    masked = masked[:, :rays_per_bin * num_bins]
    voxelized = masked.reshape(num_envs, num_bins, rays_per_bin).mean(dim=2)

    return voxelized