import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
import laspy
from sensor_msgs_py import point_cloud2 as pc2
import numpy as np
import os

class PointCloudToLAS(Node):
    def __init__(self):
        super().__init__('pointcloud_to_las')
        self.output_file = "output.las"
        self.first_write = True  # Флаг первого сохранения

        self.subscription = self.create_subscription(
            PointCloud2,
            '/pub_pointcloud2',  # Замените на ваш топик
            self.callback,
            10)
        self.get_logger().info('Node started, waiting for PointCloud2...')

    def callback(self, msg):
        # self.get_logger().info(f'PointCloud fields: {[field.name for field in msg.fields]}')
        try:
            new_points = pc2.read_points(msg, field_names=['x', 'y', 'z', 'rgb'], skip_nans=True)
            point_list = [(p[0], p[1], p[2], p[3] if len(p) > 3 else 0.0) for p in new_points]
            points_np = np.array(point_list, dtype=[
                ('x', np.float32), ('y', np.float32),
                ('z', np.float32), ('rgb', np.float32)
            ])

            # Если файл существует, загружаем предыдущие точки
            if os.path.exists(self.output_file):
                with laspy.open(self.output_file) as lasfile:
                    las = lasfile.read()
                    existing_data = np.vstack([las.x, las.y, las.z]).T
                    if hasattr(las, 'red') and hasattr(las, 'green') and hasattr(las, 'blue'):
                        existing_rgb = np.vstack([las.red, las.green, las.blue]).T
            else:
                existing_data = np.empty((0, 3))
                existing_rgb = np.empty((0, 3))

            # Объединение старых и новых точек
            combined_points = np.concatenate([
                existing_data,
                np.vstack([points_np['x'], points_np['y'], points_np['z']]).T
            ])

            # Подготовка RGB данных (если есть)
            if 'rgb' in points_np.dtype.names:
                rgb = points_np['rgb'].view(np.uint32)
                new_rgb = np.vstack([
                    ((rgb >> 16) & 0xFF),
                    ((rgb >> 8) & 0xFF),
                    (rgb & 0xFF)
                ]).T
                combined_rgb = np.concatenate([existing_rgb, new_rgb])

            # Создание нового LAS-файла с объединенными данными
            las = laspy.create()
            las.x = combined_points[:, 0]
            las.y = combined_points[:, 1]
            las.z = combined_points[:, 2]

            if 'rgb' in points_np.dtype.names:
                las.red = combined_rgb[:, 0]
                las.green = combined_rgb[:, 1]
                las.blue = combined_rgb[:, 2]

            # Сохранение объединенного файла
            las.write(self.output_file)
            self.get_logger().info(f"Saved {len(combined_points)} points to {self.output_file}")
            
        except Exception as e:
            self.get_logger().error(f"Error: {str(e)}")

def main(args=None):
    rclpy.init(args=args)
    node = PointCloudToLAS()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()