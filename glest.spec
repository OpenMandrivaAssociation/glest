%define	name	glest
%define	version	2.0.0
%define	release	%mkrel 2
%define	Summary	A free 3d real time strategy game

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	%{Summary}
License:	GPL
Group:		Games/Strategy
URL:		http://www.glest.org/
Source0:	%{name}-%{version}.tar.bz2
Source1:	%{name}-translations.tar.bz2
Source2:	%{name}-maps.tar.bz2
Source3:	%{name}.sh
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png
Patch0:		glest-2.0.0-extraqual.patch
Requires:	%{name}-data >= %{version}
BuildRequires:	MesaGLU-devel zlib-devel openal-devel xerces-c-devel dos2unix
BuildRequires:	SDL-devel oggvorbis-devel XFree86-devel SDL_net-devel
BuildRequires:  SDL_mixer-devel Mesa-common-devel jam unzip autoconf >= 2.5 
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Glest is a 3d OpenGL real time strategy game. It takes place in a 
context which could be compared to that of the pre-renaissance 
Europe, with the licence that magic forces exist in the environment 
and can be controlled.

"Deep rests Science in the Mind
as Magic deep in the Heart;
Those on which the Will is strong,
Those will reign on Their behalf."

%prep
%setup -q -a 1 -a 2
%patch0 -p1 -b .extraqual

cd mk/linux
# unfortunately all the files in mk/linux have a dos
# coding and thus a build will fail unless we convert 
# them to unix mode
dos2unix *
dos2unix mk/autoconf/*
dos2unix mk/jam/*

cd -
cd translations
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

cd ../maps
unzip -o 2_kindoms_map.zip 
unzip -o 3_islands_map.zip
unzip -o amazone_map.zip
unzip -o center_punch.zip
unzip -o islands_map.zip
unzip -o neighbors.zip
unzip -o river_world_map.zip
unzip -o the_lake_map.zip
unzip -o up_hill_war.zip

%build
cd mk/linux
sh ./autogen.sh
%configure2_5x --bindir=%{_gamesbindir} \
  --datadir=%{_gamesdatadir}
jam -d2 %{_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
# glest has no working "jam install" as of now, so
# we'll have to do the fun manually
install -m755 mk/linux/glest -D $RPM_BUILD_ROOT%{_gamesbindir}/glest.bin
install -m755 %{SOURCE3} -D $RPM_BUILD_ROOT%{_gamesbindir}/glest

mkdir -p $RPM_BUILD_ROOT%{_gamesdatadir}/%{name}/{data/lang,maps}
install -m644 mk/linux/glest.ini $RPM_BUILD_ROOT%{_gamesdatadir}/%{name}
install -m644 translations/*lng $RPM_BUILD_ROOT%{_gamesdatadir}/%{name}/data/lang
install -m644 maps/*gbm $RPM_BUILD_ROOT%{_gamesdatadir}/%{name}/maps

install -d $RPM_BUILD_ROOT%{_menudir}
cat <<EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}):command="%{_gamesbindir}/%{name}" \
		icon=%{name}.png \
		needs="x11" \
		section="Amusement/Strategy" \
		title="Glest"\
		longtitle="%{Summary}"
EOF

install -d $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=Glest
Comment=%{Summary}
Exec=soundwrapper %_gamesbindir/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-MoreApplications-Games-Strategy;Game;StrategyGame;
EOF

install -m644 %{SOURCE11} -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png


%post
%update_menus

%postun
%clean_menus

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/README docs/README.linux docs/license.txt
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_menudir}/%{name}
%{_gamesdatadir}/%{name}/
%defattr(755,root,root,755)
%{_gamesbindir}/*
%{_datadir}/applications/mandriva-%{name}.desktop


