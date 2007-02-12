Summary:	A GNU source-level debugger for C, C++ and Fortran
Summary(de.UTF-8):	Symbolischer Debugger für C und andere Sprachen
Summary(es.UTF-8):	Depurador de programas C y otras lenguajes
Summary(fr.UTF-8):	Débugger symbolique pour C et d'autres langages
Summary(pl.UTF-8):	Symboliczny odpluskwiacz dla C i innych języków
Summary(pt_BR.UTF-8):	Depurador de programas C e outras linguagens
Summary(ru.UTF-8):	Символический отладчик для C и других языков
Summary(tr.UTF-8):	C ve diğer diller için sembolik hata ayıklayıcı
Summary(uk.UTF-8):	Символьний відладчик для С та інших мов
Summary(zh_CN.UTF-8):	[开发]C和其他语言的调试器
Summary(zh_TW.UTF-8):	[.-A開發]C和.$)B其.-A他語.$)B言的調試器
Name:		crossavr-gdb
Version:	6.2.1
Release:	0.1
License:	GPL
Group:		Development/Debuggers
Source0:	ftp://ftp.gnu.org/gnu/gdb/gdb-%{version}.tar.bz2
# Source0-md5:	3b3898cfd426e1acd5efc89560aa93ba
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
BuildRequires:	texinfo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		avr

%description
Gdb is a full featured, command driven debugger. Gdb allows you to
trace the execution of programs and examine their internal state at
any time. Gdb works for C and C++ compiled with the GNU C compiler
gcc.

%description -l de.UTF-8
dem Sie die Ausführung von Programmen verfolgen und jederzeit den
inneren Zustand überprüfen können. Er funktioniert für C und mit GNU C
kompiliertes C++.

%description -l es.UTF-8
Este es un depurador orientado a comandos repleto de características.
Te permite rastrear la ejecución de programas y examinar su estado
interno a cualquier momento. Funciona para C y C++ compilado con el
compilador GNU C.

%description -l fr.UTF-8
Débugger complet, piloté par commandes. Permet de tracer l'exécution
des programmes et d'examiner à tout moment leur état interne.
Fonctionne avec les binaires C et C++ compilés avec le compilateur C
de GNU, gcc.

%description -l pl.UTF-8
Gdb jest rozbudowanym odpluskwiaczem (debuggerem), pozwalającym
śledzić wykonywanie programu i badać jego stan wewnętrzny. Gdb
umożliwia odpluskwianie programów napisanych w C/C++ i skompilowanych
przy pomocy kompilatora GNU (gcc).

%description -l pt_BR.UTF-8
Este é um debugger orientado a comandos repleto de características.
Ele permite à você rastrear a execução de programas e examinar o seu
estado interno a qualquer momento. Ele funciona para para C e C++
compilado com o compilador GNU C.

%description -l ru.UTF-8
Это полноценный отладчик, управляемый командами. Он позволяет
трассировать исполнение программ и изучать их внутреннее состояние в
любой момент времени. Работает с программами на C и C++,
скомпилированными GNU компилятором C (gcc, egcs, pgcc).

%description -l tr.UTF-8
Bir komut arayüzü üzerinden programcıya programını adım adım izleme
(trace) ve herhangi bir anda programın durumunu inceleme olanağı
verir.

%description -l uk.UTF-8
Це повноцінний відладчик, що керується командами. Він дозволяє
трасувати виконання програм та вивчати їх внутрішній стан в довільний
момент часу. Працює з програмами на C та C++, зкомпільованими
компіляторами GNU C (gcc, egcs, pgcc).

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
