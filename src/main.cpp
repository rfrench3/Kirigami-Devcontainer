/*
    SPDX-License-Identifier: GPL-2.0-or-later
    SPDX-FileCopyrightText: %{CURRENT_YEAR} %{AUTHOR} <%{EMAIL}>
*/

#include <QtGlobal>

#include <QApplication>


#include <QIcon>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include <QQuickStyle>
#include <QUrl>

#include "app.h"
#include "version-newproject.h"
#include <KAboutData>
#include <KLocalizedContext>
#include <KLocalizedString>

#include "newprojectconfig.h"

using namespace Qt::Literals::StringLiterals;

int main(int argc, char *argv[])
{

    QApplication app(argc, argv);

    // Default to org.kde.desktop style unless the user forces another style
    if (qEnvironmentVariableIsEmpty("QT_QUICK_CONTROLS_STYLE")) {
        QQuickStyle::setStyle(u"org.kde.desktop"_s);
    }

    KLocalizedString::setApplicationDomain("newproject");
    QCoreApplication::setOrganizationName(u"KDE"_s);

    KAboutData aboutData(
        // The program name used internally.
        u"newproject"_s,
        // A displayable program name string.
        i18nc("@title", "NewProject"),
        // The program version string.
        QStringLiteral(NEWPROJECT_VERSION_STRING),
        // Short description of what the app does.
        i18n("Application Description"),
        // The license this code is released under.
        KAboutLicense::GPL,
        // Copyright Statement.
        i18n("(c) %{CURRENT_YEAR}"));
    aboutData.addAuthor(i18nc("@info:credit", "%{AUTHOR}"),
                        i18nc("@info:credit", "Maintainer"),
                        u"%{EMAIL}"_s,
                        u"https://yourwebsite.com"_s);
    aboutData.setTranslator(i18nc("NAME OF TRANSLATORS", "Your names"), i18nc("EMAIL OF TRANSLATORS", "Your emails"));
    KAboutData::setApplicationData(aboutData);
    QGuiApplication::setWindowIcon(QIcon::fromTheme(u"org.kde.newproject"_s));

    QQmlApplicationEngine engine;

    auto config = NewProjectConfig::self();

    qmlRegisterSingletonInstance("org.kde.newproject.private", 1, 0, "Config", config);

    engine.rootContext()->setContextObject(new KLocalizedContext(&engine));
    engine.loadFromModule("org.kde.newproject", u"Main");

    if (engine.rootObjects().isEmpty()) {
        return -1;
    }

    return app.exec();
}
