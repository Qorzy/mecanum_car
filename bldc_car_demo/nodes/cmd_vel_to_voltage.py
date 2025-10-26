#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64

class MecanumMapper(Node):
    def __init__(self):
        super().__init__('mecanum_cmd_vel_to_voltage')

        # Params
        p = self.declare_parameter
        self.r   = p('wheel_radius', 0.08).value
        self.Lx = p('half_wheelbase', 0.20).value
        self.Ly = p('half_track',     0.18).value
        self.kv = p('kv',             0.02).value
        self.vmax = p('vmax',           24.0).value

        self.fl_sign = p('fl_sign', 1.0).value
        self.fr_sign = p('fr_sign', 1.0).value
        self.rl_sign = p('rl_sign', 1.0).value
        self.rr_sign = p('rr_sign', 1.0).value

        self.fl_topic = p('fl_topic', '/mecanum/front_left/voltage').value
        self.fr_topic = p('fr_topic', '/mecanum/front_right/voltage').value
        self.rl_topic = p('rl_topic', '/mecanum/rear_left/voltage').value
        self.rr_topic = p('rr_topic', '/mecanum/rear_right/voltage').value

        # Publishers
        self.pub_fl = self.create_publisher(Float64, self.fl_topic, 10)
        self.pub_fr = self.create_publisher(Float64, self.fr_topic, 10)
        self.pub_rl = self.create_publisher(Float64, self.rl_topic, 10)
        self.pub_rr = self.create_publisher(Float64, self.rr_topic, 10)

        # Subscriber
        self.create_subscription(Twist, '/cmd_vel', self.on_cmd, 10)

        self.k_sum = self.Lx + self.Ly
        self.get_logger().info(
            f"Mecanum map /cmd_vel -> {self.fl_topic},{self.fr_topic},{self.rl_topic},{self.rr_topic} | "
            f"r={self.r}, Lx={self.Lx}, Ly={self.Ly}, kv={self.kv}, vmax={self.vmax}"
        )

    def clamp(self, v): return max(-self.vmax, min(self.vmax, v))

    def on_cmd(self, msg: Twist):
        vx = msg.linear.x      # forward (+)
        vy = msg.linear.y      # left (+)
        wz = msg.angular.z     # CCW (+)

        r, k = self.r, self.k_sum

        # wheel speeds (rad/s)
        w_fl = ( vx - vy - k*wz ) / r
        w_fr = ( vx + vy + k*wz ) / r
        w_rl = ( vx + vy - k*wz ) / r
        w_rr = ( vx - vy + k*wz ) / r

        # voltage feed-forward
        Vfl = self.clamp(self.fl_sign * self.kv * w_fl)
        Vfr = self.clamp(self.fr_sign * self.kv * w_fr)
        Vrl = self.clamp(self.rl_sign * self.kv * w_rl)
        Vrr = self.clamp(self.rr_sign * self.kv * w_rr)

        self.pub_fl.publish(Float64(data=Vfl))
        self.pub_fr.publish(Float64(data=Vfr))
        self.pub_rl.publish(Float64(data=Vrl))
        self.pub_rr.publish(Float64(data=Vrr))

def main():
    rclpy.init()
    node = MecanumMapper()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()