Name:       nextcloud-client
Summary:    Nextcloud command line sync client
Version:    6.2.0
Release:    0
License:    GPLv2
URL:        https://github.com/nextcloud/desktop
Source0:    %{name}-%{version}.tar.gz
Source1:    libssl-1.0.patch
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(libp11)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(Qt6Concurrent)
BuildRequires:  pkgconfig(Qt6Core)
BuildRequires:  pkgconfig(Qt6Core5Compat)
BuildRequires:  pkgconfig(Qt6DBus)
BuildRequires:  pkgconfig(Qt6Gui)
BuildRequires:  pkgconfig(Qt6Linguist)
BuildRequires:  pkgconfig(Qt6QmlCompiler)
BuildRequires:  pkgconfig(Qt6Quick)
BuildRequires:  pkgconfig(Qt6Svg)
BuildRequires:  pkgconfig(Qt6WebSockets)
BuildRequires:  pkgconfig(Qt6Xml)
BuildRequires:  pkgconfig
BuildRequires:  cmake
BuildRequires:  extra-cmake-modules >= 6.0.0
BuildRequires:  qt6-qtkeychain-devel
BuildRequires:  qt6-rpm-macros
BuildRequires:  qt6-qttools
BuildRequires:  kf6-karchive-devel

%description
%{summary}.

NOTE: The library installs in LIBDIR/nextcloud for compatability reasons with OwnCloud.
This means you will have to have that path in your LD_LIBRARY_PATH variable to use the client.

%if 0%{?_chum}
Title: Nextcloud Sync Client (Qt6)
Type: console-application
PackagedBy: nephros
Categories:
 - Utility
 - FileTools
 - NetworkFilesystems
Custom:
  Repo: https://github.com/nextcloud/desktop
  PackagingRepo: https://gitlab.com/nephros/nextcloud-client
Icon: https://avatars.githubusercontent.com/u/19211038?s=200&v=4
Url:
  Homepage: https://nextcloud.com/install/#install-clients
  Help: https://gitlab.com/nephros/nextcloud-client/-/blob/%{version}/README_SailfishOS.md
%endif


%package devel
Summary:    Development files for %{name}
Requires:   %{name}-libs = %{version}-%{release}

%description devel
%{summary}.


%package libs
Summary:    Libraries for %{name}

%description libs
%{summary}.

%if 0%{?_chum}
Title: Nextcloud Client Libraries
PackagedBy: nephros
Categories:
 - Library
Custom:
  Repo: https://github.com/nextcloud/desktop
  PackagingRepo: https://gitlab.com/nephros/nextcloud-client
Icon: https://avatars.githubusercontent.com/u/19211038?s=200&v=4
Url:
  Homepage: https://nextcloud.com/install/#install-clients
%endif


%package vfs-plugin
Summary:    Plugins for %{name}

%description vfs-plugin
%{summary}.

%if 0%{?_chum}
Title: Nextcloud VFS Plugins
PackagedBy: nephros
Categories:
 - Library
Custom:
  Repo: https://github.com/nextcloud/desktop
  PackagingRepo: https://gitlab.com/nephros/nextcloud-client
Icon: https://avatars.githubusercontent.com/u/19211038?s=200&v=4
Url:
  Homepage: https://nextcloud.com/install/#install-clients
%endif


# add a conditional dep:
%if 0%{?sailfishos_version} <= 40500
BuildRequires:  pkgconfig(Qt5WebKitWidgets)
%endif

%prep
%setup -q -n %{name}-%{version}/upstream

%if 0%{?sailfishos_version} < 40001
patch -p1 < %SOURCE1
%endif

%build
%cmake .  \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir}/nextcloud \
    -DTOKEN_AUTH_ONLY=OFF \
    -DBUILD_SHELL_INTEGRATION=OFF \
    -DBUILD_SHELL_INTEGRATION_ICONS=OFF \
    -DBUILD_SHELL_INTEGRATION_DOLPHIN=OFF \
    -DBUILD_SHELL_INTEGRATION_NAUTILUS=OFF \
    -DBUILD_GUI=OFF \
    -DBUILD_UPDATER=OFF \
    -DBUILD_TESTING=OFF \
    -DBUILD_WITH_WEBENGINE=OFF \
    -DNO_MSG_HANDLER=ON \
    %{nil}

%cmake_build

%install
%cmake_install

%files
%config %{_sysconfdir}/Nextcloud/*
%{_bindir}/nextcloudcmd

%files devel
%license COPYING
%{_includedir}/nextcloudsync/
%{_libdir}/nextcloud/lib*.so

%files libs
%{_libdir}/nextcloud/lib*.so.*

%files vfs-plugin
%{_libdir}/nextcloud/nextcloudsync_vfs_*.so
