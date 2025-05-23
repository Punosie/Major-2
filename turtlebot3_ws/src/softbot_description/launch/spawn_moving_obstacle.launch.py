import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
def generate_sdf(obstacle):
    sdf_template = """<?xml version="1.0"?>
        <sdf version="1.6">
        <model name="{name}">
            <static>false</static>
            <link name="link">
            
                <inertial>
                    <mass>0.1</mass>  <!-- Reduce the mass to make it lighter -->
                    <inertia>
                        <ixx>0.0001</ixx>
                        <iyy>0.0001</iyy>
                        <izz>0.0001</izz>
                    </inertia>
                </inertial>

                <pose>{x} {y} {z} 0 0 0</pose>
                <visual name="visual">
                    <geometry>
                        <box>
                            <size>0.5 0.5 0.5</size>
                        </box>
                    </geometry>
                    <material>
                        <ambient>1 0 0 1</ambient>
                    </material>
                </visual>
                <collision name="collision">
                    <geometry>
                        <box>
                            <size>0.5 0.5 0.5</size>
                        </box>
                    </geometry>
                </collision>
            </link>

            <!-- Plugin for movement -->
            <plugin name="moving_obstacle_plugin" filename="libmoving_obstacle_plugin.so">
                <center_x>{x}</center_x>
                <center_y>{y}</center_y>
                <radius>0.5</radius>
                <speed>0.3</speed>
            </plugin>
        </model>
        </sdf>
    """

    #Use `.format()` properly
    return sdf_template.format(name=obstacle["name"], x=obstacle["x"], y=obstacle["y"], z=obstacle["z"])


def generate_launch_description():
    # obstacle_data = [
    #     {"name": "obstacle_1", "x": 3.0, "y": -2.0, "z": 0.0},
    #     {"name": "obstacle_2", "x": 0.0, "y": 1.0, "z": 0.0},
    #     {"name": "obstacle_3", "x": -2.0, "y": 0.0, "z": 0.0},
    #     {"name": "obstacle_4", "x": -2.0, "y": -1.25, "z": 0.0}
    # ]
    obstacle_data = [
        # {"name": "obstacle_1", "x": 0.25, "y": -1.0, "z": 0.25},
        # {"name": "obstacle_2", "x": 0.4, "y": 1.5, "z": 0.25},
        {"name": "obstacle_3", "x": 0.0, "y": 1.0, "z": 0.25},
        {"name": "obstacle_4", "x": 0.0, "y": -1.75, "z": 0.25}
    ]

    spawn_commands = []
    for obs in obstacle_data:
        # Generate modified SDF file
        sdf_content = generate_sdf(obs)
        sdf_path = f"/tmp/{obs['name']}.sdf"

        # Write the new SDF file to /tmp
        with open(sdf_path, "w") as f:
            f.write(sdf_content)

        spawn_commands.append(
            Node(
                package="gazebo_ros",
                executable="spawn_entity.py",
                arguments=[
                    "-entity", obs["name"],
                    "-file", sdf_path,  # Use the modified file
                    "-x", str(obs["x"]),
                    "-y", str(obs["y"]),
                    "-z", str(obs["z"])
                ],
                output="screen"
            )
        )

    return LaunchDescription(spawn_commands)


