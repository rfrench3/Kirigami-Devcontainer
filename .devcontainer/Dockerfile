FROM archlinux:latest

# Update system and install required packages
RUN pacman -Syu --noconfirm \
    astyle \
    cmake \
    git \
    extra-cmake-modules \
    curl \
    sudo \
    # Basic build tools - gnu
    autoconf \
    automake \
    bison \
    flex \
    gcc \
    gperf \
    make \
    texinfo \
    # Basic build tools - llvm
    clang \
    # Basic build tools - build systems
    meson \
    ninja \
    # Qt-related
    qt6 \
    # kcoreaddons
    pyside6 \
    shiboken6 \
    # kf6
    kirigami \
    kcoreaddons \
    kconfig \
    ki18n \
    kiconthemes \
    kirigami-addons \
    qqc2-desktop-style 

# Create vscode user with sudo access
RUN groupadd --gid 1000 vscode \
    && useradd --uid 1000 --gid 1000 -m -s /bin/bash vscode \
    && echo 'vscode ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers.d/vscode \
    && chmod 0440 /etc/sudoers.d/vscode

# Give vscode access to the input group (for testing controllers)
RUN groupadd -f input \
    && usermod -a -G input vscode

## Let breeze work while testing (not necessary)
ENV XDG_CURRENT_DESKTOP=KDE
