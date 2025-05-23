#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/common/common.hh>
#include <ignition/math/Pose3.hh>

namespace gazebo
{
  class MovingObstacle : public ModelPlugin
  {
  private:
    physics::ModelPtr model;
    event::ConnectionPtr updateConnection;
    double angle;
    // double radius;
    // double angular_speed;
    // Add missing member variables
    ignition::math::Vector3d center;  // Center of circular motion
    double radius = 1.0;              // Radius of circular path
    double speed = 0.5;               // Speed of rotati
    double center_x; // Center of rotation X
    double center_y; // Center of rotation Y
    double center_z; // Center of rotation Z

  public:
    void Load(gazebo::physics::ModelPtr _model, sdf::ElementPtr _sdf) {
    this->model = _model;

    // Default values
    double center_x = 0.0;
    double center_y = 0.0;
    double radius = 1.0;
    double speed = 0.5;

    // Read parameters from SDF
    if (_sdf->HasElement("center_x")) {
        center_x = _sdf->Get<double>("center_x");
    }
    if (_sdf->HasElement("center_y")) {
        center_y = _sdf->Get<double>("center_y");
    }
    if (_sdf->HasElement("radius")) {
        radius = _sdf->Get<double>("radius");
    }
    if (_sdf->HasElement("speed")) {
        speed = _sdf->Get<double>("speed");
    }

    // Store values
    this->center = ignition::math::Vector3d(center_x, center_y, 0);
    this->radius = radius;
    this->speed = speed;

    // Connect to the update event
    this->updateConnection = event::Events::ConnectWorldUpdateBegin(
        std::bind(&MovingObstacle::OnUpdate, this)
    );
}

void OnUpdate() {
    double time = this->model->GetWorld()->SimTime().Double();

    // Compute circular motion
    double x = this->center.X() + this->radius * cos(this->speed * time);
    double y = this->center.Y() + this->radius * sin(this->speed * time);

    // Set new position
    ignition::math::Pose3d newPose(x, y, 0, 0, 0, 0);
    this->model->SetWorldPose(newPose);
}

  };

  GZ_REGISTER_MODEL_PLUGIN(MovingObstacle)
}
