# ============================================
# Base Image - Ubuntu 24.04 LTS
# ============================================
FROM ubuntu:24.04

# ============================================
# Set environment variables for locale
# ============================================
ENV LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8

# ============================================
# Step 1: Install basic system dependencies
# ============================================
RUN apt update && apt install -y \
    locales \
    software-properties-common \
    curl \
    && locale-gen en_US en_US.UTF-8 \
    && update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

# ============================================
# Step 2: Enable Ubuntu Universe repository
# ============================================
RUN add-apt-repository universe -y

# ============================================
# Step 3: Add ROS2 APT repository
# ============================================
RUN apt-get update && apt install -y curl && \
    ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F\" '{print $4}') && \
    curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb" && \
    dpkg -i /tmp/ros2-apt-source.deb && \
    rm /tmp/ros2-apt-source.deb && \
    rm -rf /var/lib/apt/lists/*

# ============================================
# Step 4: Install ROS development tools
# ============================================
RUN apt-get update && apt install -y ros-dev-tools && \
    rm -rf /var/lib/apt/lists/*

# ============================================
# Step 5: Upgrade system packages
# ============================================
RUN apt-get update && apt upgrade -y && \
    rm -rf /var/lib/apt/lists/*

# ============================================
# Step 6: Install ROS2 Jazzy packages
# ============================================
RUN apt-get update && apt install -y \
    ros-jazzy-desktop \
    ros-jazzy-ros-base \
    && rm -rf /var/lib/apt/lists/*

# ============================================
# Step 7: Setup ROS2 environment for all sessions
# ============================================
RUN echo "source /opt/ros/jazzy/setup.bash" >> /root/.bashrc

# ============================================
# Step 8: Copy ROS2 workspace into container
# ============================================
COPY ros_ws /workspace

# Set working directory to workspace
WORKDIR /ros_ws

# ============================================
# Step 9: Build the ROS2 workspace
# ============================================
RUN . /opt/ros/jazzy/setup.bash && \
    colcon build --symlink-install

# ============================================
# Step 10: Source workspace in bashrc
# ============================================
RUN echo "source /workspace/install/setup.bash" >> /root/.bashrc

# Source ROS2 setup when container starts
CMD ["/bin/bash"]


