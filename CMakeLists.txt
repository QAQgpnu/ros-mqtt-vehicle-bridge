cmake_minimum_required(VERSION 3.0.2)
project(ros_mqtt_vehicle_bridge)

add_compile_options(-std=c++14 -Wall -Wextra -Wpedantic)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  std_msgs
)
find_package(PahoMqttCpp REQUIRED)

catkin_package(
  CATKIN_DEPENDS roscpp std_msgs
)

include_directories(${catkin_INCLUDE_DIRS})

add_executable(bridge_node src/bridge_node.cpp)
target_link_libraries(bridge_node
  ${catkin_LIBRARIES}
  PahoMqttCpp::paho-mqttpp3
)

install(TARGETS bridge_node
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY config launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
