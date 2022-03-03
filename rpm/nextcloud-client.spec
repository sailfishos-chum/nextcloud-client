# 
# Do NOT Edit the Auto-generated Part!
# Generated by: spectacle version 0.32
# 

Name:       nextcloud-client

# >> macros
# << macros

Summary:    Nextcloud command line tool
Version:    2.6.5
Release:    0
Group:      Applications
License:    GPLv2
URL:        https://github.com/nextcloud/desktop
Source0:    %{name}-%{version}.tar.gz
Source100:  nextcloud-client.yaml
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(Qt5Quick)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Svg)
BuildRequires:  pkgconfig(Qt5WebEngineWidgets)
BuildRequires:  pkgconfig
BuildRequires:  qt5-qttools-linguist
BuildRequires:  qt5-qmake
BuildRequires:  libqtwebkit5-widgets-devel
BuildRequires:  sailfish-components-webview-qt5-devel
BuildRequires:  desktop-file-utils

%description


%if "%{?vendor}" == "chum"
PackageName: Nextcloud Client
Type: console-application
PackagerName: nephros
Categories:
 - Utility
 - FileTools
 - NetworkFilesystems
Custom:
  Repo: https://github.com/nextcloud/desktop
Icon: https://avatars.githubusercontent.com/u/19211038?s=200&v=4
Url:
  Homepage: https://nextcloud.com/install/#install-clients
%endif


%prep
%setup -q -n %{name}-%{version}/upstream

# >> setup
# << setup

%build
# >> build pre
# << build pre

%cmake .  \
    -DBUILD_SHELL_INTEGRATION=0 \
    -DBUILD_SHELL_INTEGRATION_DOLPHIN=0 \
    -DBUILD_SHELL_INTEGRATION_ICONS=0 \
    -DBUILD_SHELL_INTEGRATION_NAUTILUS=0 \
    -DNO_SHIBBOLETH=1

make %{?_smp_mflags}

# >> build post
# << build post

%install
rm -rf %{buildroot}
# >> install pre
lrelease -silent -removeidentical translations/*
# << install pre
%make_install

# >> install post

%__install -m 644 -D %{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
%__install -m 644 -D qml/%{name}.qml %{buildroot}%{_datadir}/%{name}/qml/%{name}.qml
#for f in qml/cover/*.qml qml/components/qmldir qml/components/*/*.qml qml/components/*.qml qml/pages/*.qml; do
for f in $(find qml/ -type f -name "*.qml" -o -name qmldir -o -name "*.png"); do
%__install -m 644 -D ${f} %{buildroot}%{_datadir}/%{name}/${f}
done
for f in translations/*.qm; do
%__install -m 644 -D ${f} %{buildroot}%{_datadir}/%{name}/${f}
done
for s in 512 256 128 64 48; do
%__install -m 644 -D icons/%{name}-${s}.png %{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps/%{name}.png
done
# mangle version info
sed -i -e "s/\(^.*version: \).*$/\1%{version}/" %{buildroot}%{_datadir}/%{name}/qml/components/AppInfoSingleton.qml
sed -i -e "s/\(^.*release: \).*$/\1%{release}/" %{buildroot}%{_datadir}/%{name}/qml/components/AppInfoSingleton.qml
# << install post

desktop-file-install --delete-original       \
  --dir %{buildroot}%{_datadir}/applications             \
   %{buildroot}%{_datadir}/applications/*.desktop

%files
%defattr(-,root,root,-)
%license LICENSE
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/*/*/apps/%{name}.png
%{_datadir}/icons/*/*/apps/%{name}.svg
%{_datadir}/%{name}/translations/*.qm
%{_datadir}/%{name}/qml/*
# >> files
# << files
