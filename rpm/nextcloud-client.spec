Name:       nextcloud-client

Summary:    Nextcloud command line sync client
Version:    3.13.4
Release:    0
License:    GPLv2
URL:        https://github.com/nextcloud/desktop
Source0:    %{name}-%{version}.tar.gz
Source1:    libssl-1.0.patch
Patch0:     no-webengine.patch

BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig
BuildRequires:  cmake

BuildRequires:  sailfish-version > 4.4
BuildRequires:  sailfish-version < 5.2

BuildRequires: opt-qt5-qtbase-devel
BuildRequires: opt-qt5-qtbase-private-devel
BuildRequires: opt-qt5-qtdeclarative-devel
BuildRequires: opt-qt5-qtquickcontrols2-devel
BuildRequires: opt-qt5-qtsvg-devel
#BuildRequires: opt-qt5-qtxml-devel
BuildRequires: opt-qt5-qtxmlpatterns-devel
BuildRequires: opt-qt5-qtkeychain-devel
BuildRequires: opt-qt5-qtwebsockets-devel
# tools
BuildRequires: opt-qt5-linguist
BuildRequires: opt-qt5-qttools
BuildRequires: librsvg-tools
#KF5
BuildRequires: opt-kf5-karchive-devel

# Runtime deps:
%{?_opt_qt5:Requires: %{_opt_qt5}%{?_isa} = %{_opt_qt5_version}}
Requires: opt-qt5-qtbase    >= %{_opt_qt5_version}
Requires: opt-qt5-qtnetwork >= %{_opt_qt5_version}

Requires:  sailfish-version > 4.4
Requires:  sailfish-version < 5.2

%description
%{summary}.

This version is built using the Qt 5.15 packages from Chum

%if 0%{?_chum}
Title: Nextcloud Sync Client (Qt 5.15)
Type: console-application
PackagedBy: nephros
Categories:
 - Utility
 - FileTools
 - NetworkFilesystems
Custom:
  Repo: https://github.com/nextcloud/desktop
  PackagingRepo: https://github.com/sailfishos-chum/nextcloud-client
PackageIcon: https://avatars.githubusercontent.com/u/19211038?s=200&v=4
Links:
  Homepage: https://nextcloud.com/install/#install-clients
  Help: https://github.com/sailfishos-chum/nextcloud-client/-/blob/%{version}/README_SailfishOS.md
%endif


%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries
Requires:   %{name}-libs = %{version}-%{release}

%description devel
%{summary}.


%package libs
Summary:    Libraries for %{name}
Group:      Development/Libraries
Requires:   opt-qt5-qtbase       >= %{_opt_qt5_version}
Requires:   opt-qt5-qtwebsockets >= %{_opt_qt5_version}
Requires:   opt-qt5-qtkeychain   >= %{_opt_qt5_version}
Requires:   opt-qt5-qtsvg        >= %{_opt_qt5_version}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description libs
%{summary}.

%if 0%{?_chum}
Title: Nextcloud Client Libraries (Qt 5.15)
PackagedBy: nephros
Categories:
 - Library
Custom:
  Repo: https://github.com/nextcloud/desktop
  PackagingRepo: https://github.com/sailfishos-chum/nextcloud-client
Icon: https://avatars.githubusercontent.com/u/19211038?s=200&v=4
Url:
  Homepage: https://nextcloud.com/install/#install-clients
%endif


%global __provides_exclude_from ^%{_opt_qt5_archdatadir}/qml/.*\\.so$
%{?opt_qt5_default_filter}

%prep
%setup -q -n %{name}-%{version}/upstream

# no-webengine.patch
%patch0 -p1
%if 0%{?sailfishos_version} < 40001
patch -p1 < %SOURCE1
%endif

%build
export QTDIR=%{_opt_qt5_prefix}
export CMAKE_PREFIX_PATH=%{_opt_qt5_prefix}

%cmake .  \
    -DCMAKE_PREFIX_PATH=%{_opt_qt5_prefix} \
    -DBUILD_GUI=0 \
    -DBUILD_TESTING=OFF \
    -DBUILD_SHELL_INTEGRATION=0 \
    -DBUILD_SHELL_INTEGRATION_DOLPHIN=0 \
    -DBUILD_SHELL_INTEGRATION_ICONS=0 \
    -DBUILD_SHELL_INTEGRATION_NAUTILUS=0

%make_build

%install
%make_install

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%license COPYING
%config %{_sysconfdir}/Nextcloud/*
%{_bindir}/*

%files devel
%{_includedir}/*
%{_libdir}/*.so
#%%{_libdir}/*/*.so
%files libs
%{_libdir}/*.so.*
#%%{_libdir}/*/*.so.*
