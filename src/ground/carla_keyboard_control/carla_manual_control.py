#!/usr/bin/env python3
import rospy
import sys, termios, tty

from carla_msgs.msg import CarlaEgoVehicleControl

def getKey():
    """读取终端键盘按键，无回车立即读取"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key

def main():
    rospy.init_node("carla_keyboard_control_node")
    pub = rospy.Publisher("/carla/ego_vehicle/vehicle_control_cmd", CarlaEgoVehicleControl, queue_size=10)
    rate = rospy.Rate(20)

    ctrl_msg = CarlaEgoVehicleControl()
    ctrl_msg.throttle = 0.0
    ctrl_msg.steer = 0.0
    ctrl_msg.brake = 0.0
    ctrl_msg.hand_brake = False
    ctrl_msg.reverse = False

    print("===== Carla 键盘控制小车 =====")
    print("w 前进 | s 后退 | a 左转 | d 右转")
    print("空格 = 刹车， q = 退出程序")
    print("================================\n")

    while not rospy.is_shutdown():
        key = getKey()

        # 重置
        ctrl_msg.throttle = 0.0
        ctrl_msg.steer = 0.0
        ctrl_msg.brake = 0.0

        if key == 'w':  # 前进
            ctrl_msg.throttle = 0.4
            ctrl_msg.reverse = False
        elif key == 's':  # 后退
            ctrl_msg.throttle = 0.3
            ctrl_msg.reverse = True
        elif key == 'a':  # 左转
            ctrl_msg.steer = -0.3
        elif key == 'd':  # 右转
            ctrl_msg.steer = 0.3
        elif key == ' ':  # 空格刹车
            ctrl_msg.brake = 1.0
        elif key == 'q':  # q退出
            print("脚本结束")
            break

        pub.publish(ctrl_msg)
        rate.sleep()

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
