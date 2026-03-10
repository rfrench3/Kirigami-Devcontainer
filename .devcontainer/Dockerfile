FROM archlinux:latest

RUN pacman -Syu --noconfirm \
    cmake \
    git \
    extra-cmake-modules \
    sudo \
    make \
    clang \
    qt6 \
    kirigami \
    kcoreaddons \
    kconfig \
    ki18n \
    kiconthemes \
    kirigami-addons \
    qqc2-desktop-style \
    plasma-workspace

# # Uncomment for python applications
# RUN pacman -Syu --noconfirm \
#     pyside6 \
#     shiboken6 \

# Create developer user with sudo access
RUN groupadd --gid 1000 developer \
    && useradd --uid 1000 --gid 1000 -m -s /bin/bash developer \
    && echo 'developer ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers.d/developer \
    && chmod 0440 /etc/sudoers.d/developer

## Let breeze work while testing (not necessary)
ENV XDG_CURRENT_DESKTOP=KDE
