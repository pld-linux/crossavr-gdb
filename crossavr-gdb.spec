Summary:	A GNU source-level debugger for C, C++ and Fortran
Summary(de):	Symbolischer Debugger fЭr C und andere Sprachen
Summary(es):	Depurador de programas C y otras lenguajes
Summary(fr):	DИbugger symbolique pour C et d'autres langages
Summary(pl):	Symboliczny odpluskwiacz dla C i innych jЙzykСw
Summary(pt_BR):	Depurador de programas C e outras linguagens
Summary(ru):	Символический отладчик для C и других языков
Summary(tr):	C ve diПer diller iГin sembolik hata ayЩklayЩcЩ
Summary(uk):	Символьний в╕дладчик для С та ╕нших мов
Summary(zh_CN):	[©╙╥╒]C╨мфДкШсОят╣д╣ВйтфВ
Summary(zh_TW):	[.-A╤}╣o]C╘M.$)B╗Д.-A╔L╩y.$)B╗╔╙╨╫у╦у╬╧
Name:		crossavr-gdb
Version:	6.1.1
Release:	0.1
License:	GPL
Group:		Development/Debuggers
Source0:	ftp://ftp.gnu.org/gnu/gdb/gdb-%{version}.tar.bz2
# Source0-md5:	dd25473f61a3a2e1b08dee5f67ebae28
Patch0:		gdb-ncurses.patch
Patch1:		gdb-readline.patch
Patch2:		gdb-info.patch
Patch3:		gdb-passflags.patch
Patch4:		gdb-headers.patch
BuildRequires:	XFree86-devel
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	ncurses-devel >= 5.2
BuildRequires:	readline-devel >= 4.2
BuildRoot:	%{tmpdir}/gdb-%{version}-root-%(id -u -n)

%define         target          avr

%description
Gdb is a full featured, command driven debugger. Gdb allows you to
trace the execution of programs and examine their internal state at
any time. Gdb works for C and C++ compiled with the GNU C compiler
gcc.

%description -l de
dem Sie die AusfЭhrung von Programmen verfolgen und jederzeit den
inneren Zustand ЭberprЭfen kЖnnen. Er funktioniert fЭr C und mit GNU C
kompiliertes C++.

%description -l es
Este es un debugger orientado a comandos repleto de caracterМsticas.
Te permite rastrear la ejecuciСn de programas y examinar su estado
interno a cualquier momento. Funciona para C y C++ compilado con el
compilador GNU C.

%description -l fr
DИbugger complet, pilotИ par commandes. Permet de tracer l'exИcution
des programmes et d'examiner Ю tout moment leur Иtat interne.
Fonctionne avec les binaires C et C++ compilИs avec le compilateur C
de GNU, gcc.

%description -l pl
Gdb jest rozbudowanym odpluskwiaczem (debuggerem), pozwalaj╠cym
╤ledziФ wykonywanie programu i badaФ jego stan wewnЙtrzny. Gdb
umo©liwia odpluskwianie programСw napisanych w C/C++ i skompilowanych
przy pomocy kompilatora GNU (gcc).

%description -l pt_BR
Este И um debugger orientado a comandos repleto de caracterМsticas.
Ele permite Ю vocЙ rastrear a execuГЦo de programas e examinar o seu
estado interno a qualquer momento. Ele funciona para para C e C++
compilado com o compilador GNU C.

%description -l ru
Это полноценный отладчик, управляемый командами. Он позволяет
трассировать исполнение программ и изучать их внутреннее состояние в
любой момент времени. Работает с программами на C и C++,
скомпилированными GNU компилятором C (gcc, egcs, pgcc).

%description -l tr
Bir komut arayЭzЭ Эzerinden programcЩya programЩnЩ adЩm adЩm izleme
(trace) ve herhangi bir anda programЩn durumunu inceleme olanaПЩ
verir.

%description -l uk
Це повноц╕нний в╕дладчик, що керу╓ться командами. В╕н дозволя╓
трасувати виконання програм та вивчати ╖х внутр╕шн╕й стан в дов╕льний
момент часу. Працю╓ з програмами на C та C++, зкомп╕льованими
комп╕ляторами GNU C (gcc, egcs, pgcc).

%prep
%setup -q -n gdb-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
for dir in `find gdb/ -name 'configure.in'`; do
	dir=$(dirname "$dir")
	olddir=$(pwd)
	cd $dir
	%{__aclocal}
	%{__autoconf}
	cd $olddir
done
cp -f /usr/share/automake/config.* .
# !! Don't enable shared here !!
# This will cause serious problems --misiek
%configure2_13 \
	--target=%{target} \
	--disable-shared \
	--enable-nls \
	--without-included-gettext \
	--without-included-regex \
	--enable-gdcli \
	--enable-gdbmi \
	--enable-multi-ice \
	--enable-netrom \
	--with-cpu=%{_target_cpu} \
	--enable-tui \
%ifnarch alpha
	--with-mmalloc
%endif

# something is wrong after above - e.g. $exeext=="no" - fix it:
cd gdb
%configure \
	--target=%{target}
cd ..

%{__make}
%{__make} info

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_infodir}

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	bindir=$RPM_BUILD_ROOT%{_bindir} \
	sbindir=$RPM_BUILD_ROOT%{_sbindir} \
	infodir=$RPM_BUILD_ROOT%{_infodir} \
	includedir=$RPM_BUILD_ROOT%{_includedir} \
	libdir=$RPM_BUILD_ROOT%{_libdir} \
	mandir=$RPM_BUILD_ROOT%{_mandir}

bzip2 -dc %{SOURCE1} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-gdb*
%{_mandir}/man1/%{target}-gdb*.1*
