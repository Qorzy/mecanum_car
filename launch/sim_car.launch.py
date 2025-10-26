from launch import LaunchDescription
from launch.actions import ExecuteProcess, SetEnvironmentVariable
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
import os

def generate_launch_description():
    pkg_share = get_package_share_directory('bldc_car_demo')
    
    # Parametre dosyasının yolunu bul (yeni mecanum.yaml)
    param_file = os.path.join(pkg_share, 'params', 'car.yaml')
    
    # Simülasyon dünyasının yolunu bul
    world_path = os.path.join(pkg_share, 'models', 'worlds', 'flat_world.sdf')
    
    # Gazebo'nun modelleri (model.sdf) bulması için model klasörünün yolu
    models_root = os.path.join(pkg_share, 'models')

    set_model_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=models_root + ':' + os.environ.get('GZ_SIM_RESOURCE_PATH', '')
    )

    # Dünyayı aç
    gz_sim = ExecuteProcess(
        cmd=['gz', 'sim', '-r', world_path],
        output='screen'
    )

    # Mecanum Mapper düğümünü başlat
    mecanum_mapper_node = Node(
        package='bldc_car_demo',
        executable='cmd_vel_to_voltage',  # setup.py'deki ad (değişmedi)
        name='mecanum_cmd_vel_to_voltage', # YAML dosyasıyla eşleşmesi için ad (değişti)
        parameters=[param_file],          # Parametre dosyasını yükle
        output='screen'
    )

    return LaunchDescription([
        set_model_path,
        gz_sim,
        mecanum_mapper_node
    ])