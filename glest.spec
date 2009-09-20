Summary:	A free 3d real time strategy game
Name:		glest
Version:	3.2.2
Release:	%mkrel 1
License:	GPLv2+
Group:		Games/Strategy
URL:		http://www.glest.org/
Source0:	http://www.titusgames.de/%{name}-source-%{version}.tar.bz2
# (tpg) all stuff from http://www.glest.org/files/contrib/translations/
Source1:	%{name}-translations.tar.bz2
Source2:	%{name}-maps.tar.bz2
Source3:	%{name}.sh
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png
Patch0:		glest-source-3.2.2-missing-headers.patch
Patch1:		glest-source-3.2.2-format_not_a_string_literal_and_no_format_arguments.patch
BuildRequires:	zlib-devel
BuildRequires:	openal-devel
BuildRequires:	xerces-c28-devel
BuildRequires:	SDL-devel
BuildRequires:	oggvorbis-devel
BuildRequires:	SDL_net-devel
BuildRequires:  SDL_mixer-devel
BuildRequires:	Mesa-common-devel
BuildRequires:	jam
BuildRequires:	unzip
BuildRequires:	recode
BuildRequires:	lua-devel
BuildRequires:	libwxgtku-devel
BuildConflicts:	libwxgtk-devel
Requires:	%{name}-data
Requires:	x11-font-adobe-utopia-75dpi
Requires:	mesa-demos
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Glest is a 3D OpenGL real time strategy game. It takes place in a 
context which could be compared to that of the pre-renaissance 
Europe, with the licence that magic forces exist in the environment 
and can be controlled.

%prep
%setup -q -n %{name}-source-%{version} -a 1 -a 2
%patch0 -p1
%patch1 -p1

#recode ISO-8859-1..UTF-8 *.txt

pushd translations
for i in *.zip; do unzip -o $i; done
mv tradu_pt-br.lng portugues.lng
popd

#fix french language file
mv translations/fran*.lng translations/francais.lng

pushd maps
for i in *.zip; do unzip -o $i; done
popd

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="$CFLAGS"

./autogen.sh
%configure2_5x \
	--bindir=%{_gamesbindir} \
	--datadir=%{_gamesdatadir} \
	--enable-optimize \
	--with-wx-config=%{_bindir}

jam -d2 %{_smp_mflags}

%install
rm -rf %{buildroot}

# glest has no working "jam install" as of now, so
# we'll have to do the fun manually

mkdir -p %{buildroot}%{_gamesbindir}
install -p -m 755 glest %{buildroot}%{_gamesbindir}/glest.bin
#install -p -m 755 glest_editor %{buildroot}%{_gamesbindir}/
install -m755 %{SOURCE3} -D %{buildroot}%{_gamesbindir}/glest

mkdir -p %{buildroot}%{_gamesdatadir}/%{name}/{data/lang,maps}
install -m644 glest.ini %{buildroot}%{_gamesdatadir}/%{name}
install -m644 translations/*lng %{buildroot}%{_gamesdatadir}/%{name}/data/lang
install -m644 maps/*gbm %{buildroot}%{_gamesdatadir}/%{name}/maps

# Desktop file
mkdir -p %{buildroot}/%{_datadir}/applications
cat > %{buildroot}/%{_datadir}/applications/mandriva-glest.desktop << EOF
[Desktop Entry]
Name=Glest
Comment=Real Time Strategy game
Exec=%{_gamesbindir}/glest
Icon=glest
StartupNotify=true
Terminal=false
Type=Application
Categories=Game;StrategyGame;
EOF

mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
install -m644 %{SOURCE11} -D %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_gamesbindir}/*
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/applications/*
%{_gamesdatadir}/%{name}
