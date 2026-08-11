#include <cstdlib>
#include <string>
#include <utility>

#include <mqtt/async_client.h>
#include <ros/ros.h>
#include <std_msgs/String.h>

namespace {

std::string readEnvironment(const char* name) {
  const char* value = std::getenv(name);
  return value == nullptr ? std::string{} : std::string{value};
}

class BridgeCallback : public virtual mqtt::callback {
 public:
  BridgeCallback(mqtt::async_client& client, ros::Publisher& publisher,
                 std::string subscribe_topic, int qos)
      : client_(client),
        publisher_(publisher),
        subscribe_topic_(std::move(subscribe_topic)),
        qos_(qos) {}

  void connected(const std::string& cause) override {
    ROS_INFO_STREAM("Connected to MQTT broker"
                    << (cause.empty() ? "" : ": " + cause));
    try {
      client_.subscribe(subscribe_topic_, qos_)->wait();
      ROS_INFO_STREAM("Subscribed to MQTT topic: " << subscribe_topic_);
    } catch (const mqtt::exception& error) {
      ROS_ERROR_STREAM("Unable to subscribe after connection: " << error.what());
    }
  }

  void connection_lost(const std::string& cause) override {
    ROS_WARN_STREAM("MQTT connection lost"
                    << (cause.empty() ? "" : ": " + cause));
  }

  void message_arrived(mqtt::const_message_ptr message) override {
    std_msgs::String output;
    output.data = message->get_payload_str();
    publisher_.publish(output);
    ROS_DEBUG_STREAM("Forwarded MQTT message from " << message->get_topic()
                                                     << " to ROS");
  }

 private:
  mqtt::async_client& client_;
  ros::Publisher& publisher_;
  std::string subscribe_topic_;
  int qos_;
};

}  // namespace

int main(int argc, char** argv) {
  ros::init(argc, argv, "ros_mqtt_vehicle_bridge");
  ros::NodeHandle node;
  ros::NodeHandle private_node("~");

  std::string broker_uri;
  std::string client_id;
  std::string mqtt_publish_topic;
  std::string mqtt_subscribe_topic;
  std::string ros_publish_topic;
  std::string ros_subscribe_topic;
  int qos = 1;

  private_node.param<std::string>("broker_uri", broker_uri,
                                  "tcp://localhost:1883");
  private_node.param<std::string>("client_id", client_id,
                                  "ros-mqtt-vehicle-bridge");
  private_node.param<std::string>("mqtt_publish_topic", mqtt_publish_topic,
                                  "vehicle/task_cmd");
  private_node.param<std::string>("mqtt_subscribe_topic", mqtt_subscribe_topic,
                                  "vehicle/mqtt_cmd");
  private_node.param<std::string>("ros_publish_topic", ros_publish_topic,
                                  "/vehicle/mqtt_cmd_json");
  private_node.param<std::string>("ros_subscribe_topic", ros_subscribe_topic,
                                  "/vehicle/task_cmd_json");
  private_node.param("qos", qos, 1);

  if (qos < 0 || qos > 2) {
    ROS_FATAL_STREAM("Invalid MQTT QoS " << qos << "; expected 0, 1, or 2");
    return 2;
  }

  const std::string username = readEnvironment("MQTT_USERNAME");
  const std::string password = readEnvironment("MQTT_PASSWORD");

  if (username.empty() != password.empty()) {
    ROS_FATAL("MQTT_USERNAME and MQTT_PASSWORD must be provided together");
    return 2;
  }

  mqtt::async_client client(broker_uri, client_id);
  ros::Publisher ros_publisher =
      node.advertise<std_msgs::String>(ros_publish_topic, 20);
  BridgeCallback callback(client, ros_publisher, mqtt_subscribe_topic, qos);
  client.set_callback(callback);

  mqtt::connect_options connection_options;
  connection_options.set_clean_session(true);
  connection_options.set_automatic_reconnect(true);
  connection_options.set_keep_alive_interval(20);
  if (!username.empty()) {
    connection_options.set_user_name(username);
    connection_options.set_password(password);
  }

  try {
    client.connect(connection_options)->wait();
  } catch (const mqtt::exception& error) {
    ROS_FATAL_STREAM("Unable to connect to MQTT broker: " << error.what());
    return 1;
  }

  ros::Subscriber ros_subscriber = node.subscribe<std_msgs::String>(
      ros_subscribe_topic, 20,
      [&client, &mqtt_publish_topic, qos](const std_msgs::String::ConstPtr& input) {
        try {
          auto message = mqtt::make_message(mqtt_publish_topic, input->data);
          message->set_qos(qos);
          client.publish(message);
          ROS_DEBUG_STREAM("Forwarded ROS message to MQTT topic: "
                           << mqtt_publish_topic);
        } catch (const mqtt::exception& error) {
          ROS_ERROR_STREAM("Unable to publish MQTT message: " << error.what());
        }
      });

  ROS_INFO_STREAM("Bridge ready: ROS " << ros_subscribe_topic << " -> MQTT "
                                        << mqtt_publish_topic << ", MQTT "
                                        << mqtt_subscribe_topic << " -> ROS "
                                        << ros_publish_topic);
  ros::spin();

  ros_subscriber.shutdown();
  try {
    if (client.is_connected()) {
      client.disconnect()->wait();
    }
  } catch (const mqtt::exception& error) {
    ROS_WARN_STREAM("MQTT disconnect failed: " << error.what());
  }

  return 0;
}
