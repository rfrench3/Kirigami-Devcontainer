# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: %{CURRENT_YEAR} %{AUTHOR} <%{EMAIL}>

# Target: static library
qt_add_qml_module(kirigamitemplate_static
    STATIC
    URI org.kde.kirigamitemplate
    VERSION 1.0
    QML_FILES
        contents/ui/Main.qml
        contents/ui/About.qml
)

target_sources(kirigamitemplate_static PUBLIC
    app.cpp
)

target_link_libraries(kirigamitemplate_static PUBLIC
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
target_include_directories(kirigamitemplate_static PUBLIC ${CMAKE_BINARY_DIR})

target_link_libraries(kirigamitemplate_static PUBLIC Qt::Widgets)

kconfig_add_kcfg_files(kirigamitemplate_static GENERATE_MOC kirigamitemplateconfig.kcfgc)

# Target: main executable
add_executable(kirigamitemplate main.cpp)
target_link_libraries(kirigamitemplate PUBLIC kirigamitemplate_static kirigamitemplate_staticplugin)
install(TARGETS kirigamitemplate ${KDE_INSTALL_TARGETS_DEFAULT_ARGS})
