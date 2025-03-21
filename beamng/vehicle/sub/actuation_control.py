import zenoh

from beamng.msg.tier4_vehicle_msgs import ActuationCommandStamped

class ActuationControlSubscriber:
  def __init__(self, vehicle, vehicle_data):
    self.vehicle = vehicle
    self.vehicle_data = vehicle_data

  def callback(self, sample: zenoh.Sample):
    if self.vehicle_data.get_manual_mode():
      return
    
    payload_bytes = bytes(sample.payload)
    payload = bytearray(payload_bytes)
    actuation_cmd = ActuationCommandStamped.deserialize(payload).actuation

    accel = actuation_cmd.accel_cmd
    brake = actuation_cmd.brake_cmd
    steer = actuation_cmd.steer_cmd

    accel = max(0, min(1, accel))
    brake = max(0, min(1, brake))
    
    # steer: Convert the tire angle output from Autoware to a range of -1 to 1
    steer = -1 * max(-0.7, min(steer, 0.7)) / 0.7
    
    print(f'ActuationControlSubscriber: accel={accel}, brake={brake}, steer={steer}')

    self.vehicle.control(
      throttle = accel,
      brake = brake,
      steering = steer
    )
