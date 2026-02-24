# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: %{CURRENT_YEAR} %{AUTHOR} <%{EMAIL}>

# Target: static library
qt_add_qml_module(newproject_static
    STATIC
    URI org.kde.newproject
    VERSION 1.0
    QML_FILES
        contents/ui/Main.qml
        contents/ui/About.qml
)

target_sources(newproject_static PUBLIC
    app.cpp
)

target_link_libraries(newproject_static PUBLIC
    Qt6::Core
    Qt6::Gui
    Qt6::Qml
    Qt6::Quick
    Qt6::QuickControls2
    Qt6::Svg
    KF6::I18n
    KF6::CoreAddons
    KF6::ConfigCore
    KF6::ConfigGui
)
target_include_directories(newproject_static PUBLIC ${CMAKE_BINARY_DIR})

target_link_libraries(newproject_static PUBLIC Qt::Widgets)

kconfig_add_kcfg_files(newproject_static GENERATE_MOC newprojectconfig.kcfgc)

# Target: main executable
add_executable(newproject main.cpp)
target_link_libraries(newproject PUBLIC newproject_static newproject_staticplugin)
install(TARGETS newproject ${KDE_INSTALL_TARGETS_DEFAULT_ARGS})
