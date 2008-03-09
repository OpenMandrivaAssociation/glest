%define	name	glest
%define	version	3.1.2
%define	release	%mkrel 1
%define	Summary	A free 3d real time strategy game

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	%{Summary}
License:	GPLv2+
Group:		Games/Strategy
URL:		http://www.glest.org/
Source0:	http://downloads.sourceforge.net/glest/%{name}-source-%{version}.tar.bz2
Source1:	%{name}-translations.tar.bz2
Source2:	%{name}-maps.tar.bz2
Source3:	%{name}.sh
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png
Requires:	%{name}-data >= %{version}
Requires:	x11-font-adobe-utopia-75dpi
BuildRequires:	zlib-devel
BuildRequires:	openal-devel
BuildRequires:	xerces-c-devel
BuildRequires:	SDL-devel
BuildRequires:	oggvorbis-devel
BuildRequires:	SDL_net-devel
BuildRequires:  SDL_mixer-devel
BuildRequires:	Mesa-common-devel
BuildRequires:	jam
BuildRequires:	unzip
BuildRequires:	recode
BuildConflicts:	libwxgtk-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Glest is a 3D OpenGL real time strategy game. It takes place in a 
context which could be compared to that of the pre-renaissance 
Europe, with the licence that magic forces exist in the environment 
and can be controlled.

%prep
%setup -q -n %name-source-%version -a 1 -a 2

recode ISO-8859-1..UTF-8 README* *.txt

pushd translations
unzip catala_1.2.2.zip
mv catala_1.2.2.lng catala.lng

unzip cesky_1.2.1.zip
unzip danish_1.0.9.zip

unzip deutsch_1.0.1.zip
mv deutsch_1.0.1.lng german.lng

unzip dutch_1.0.9.zip
unzip euskara_1.0.9.zip
unzip francais_1.1.1.zip
unzip hebrew_1.2.1.zip

unzip italiano_1.0.1.zip
mv italiano_1.0.1.lng italiano.lng

unzip magyar_1.1.0.zip

unzip norsk_0.8.1.zip
mv norsk_0.8.1.lng norsk.lng

unzip polish_1.0.9.zip

unzip portugues_1.0.1.zip
mv portugues_1.0.1.lng portuges.lng

unzip russian_1.0.9.zip
unzip slovak_1.2.1.zip
unzip turkish_1.0.9.zip
popd

pushd maps
unzip -o 2_kindoms_map.zip 
unzip -o 3_islands_map.zip
unzip -o amazone_map.zip
unzip -o center_punch.zip
unzip -o islands_map.zip
unzip -o neighbors.zip
unzip -o river_world_map.zip
unzip -o the_lake_map.zip
unzip -o up_hill_war.zip
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

%post
%update_menus

%postun
%clean_menus

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc README README.linux license.txt
%attr(755,root,root) %{_gamesbindir}/*
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/applications/*
%{_gamesdatadir}/%{name}
