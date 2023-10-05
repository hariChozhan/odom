import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64, UInt16
from sensor_msgs.msg import NavSatStatus, NavSatFix
import sys
import numpy as np


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(NavSatFix, '/navsat_test', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        gps = np.loadtxt(sys.argv[1], delimiter = ",")
        # print(gps)

        self.utimes = gps[:, 0]
        self.modes = gps[:, 1]
        self.num_satss = gps[:, 2]
        self.lats = gps[:, 3]
        self.lngs = gps[:, 4]
        self.alts = gps[:, 5]
        self.tracks = gps[:, 6]
        self.speeds = gps[:, 7]  

    def timer_callback(self):
        # try:
        

        for i, utime in enumerate(self.utimes):

            timestamp = self.get_clock().now().to_msg()

            status = NavSatStatus()

            if self.modes[i]==0 or self.modes[i]==1:
                status.status = NavSatStatus.STATUS_NO_FIX
            else:
                status.status = NavSatStatus.STATUS_FIX

            status.service = NavSatStatus.SERVICE_GPS

            num_sats = UInt16()
            num_sats.data = int(self.num_satss[i])

            fix = NavSatFix()
            fix.header.stamp = timestamp
            fix.status = status

            fix.latitude = np.rad2deg(self.alts[i])
            fix.longitude = np.rad2deg(self.lngs[i])
            fix.altitude = self.alts[i]
            # print(fix.latitude)

            track = Float64()
            track.data = self.tracks[i]

            speed = Float64()
            speed.data = self.speeds[i]
        
        self.publisher_.publish(fix)
        self.get_logger().info('Publishing: "%s"' % fix)


def main(args=None):
    if len(sys.argv) < 2:
        print ('Please specify gps file')
        return 1

    if len(sys.argv) < 3:
        print ('Please specify output rosbag file')
        return 1

    
    
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
