%if %mandriva_branch == Cooker
%define release 4
%else
%define subrel 1
%define release 4
%endif

%define relpkg 0
%define srcver 0.83.4

# don't update this package before a fusioninventory plugin is available

Epoch: 1

Summary: A web based park management
Name: glpi
Version: %{srcver}%{relpkg}
Release: %{release}
License: GPLv2
Group: Monitoring
URL: http://www.glpi-project.org/
Source0: http://forge.indepnet.net/attachments/download/656/%{name}-%{srcver}.tar.gz
Requires: php-xml
Requires: mod_php
Requires: apache-mod_socache_shmcb # if we're using apache...
Requires: php-mysql
Requires: php-mbstring
BuildArch: noarch
#Epoch: 1

%description
GLPI is web based database application allowing to managed computers and
peripherals park. Its goal is to help technicians about maintenance expiration,
stock flow and license counting.

%prep

%setup -q -n %name

%install

install -d -m 755 %{buildroot}%{_datadir}/%{name}

install -m 644 *.php *.js %{buildroot}%{_datadir}/%{name}

for i in ajax css front inc install lib locales pics plugins scripts; do
    cp -ar $i %{buildroot}%{_datadir}/%{name}
done

install -d -m 755 %{buildroot}%{_sysconfdir}/glpi
install -m 644 config/*.php %{buildroot}%{_sysconfdir}/glpi
pushd %{buildroot}%{_datadir}/%{name}
ln -sf ../../..%{_sysconfdir}/glpi config
popd

find %{buildroot}%{_datadir}/%{name} -name .htaccess | xargs rm -f

cat > %{buildroot}%{_sysconfdir}/glpi/config_path.php <<EOF
<?php
// for packaging defaults

define("GLPI_CONFIG_DIR",     "%{_sysconfdir}/glpi");
define("GLPI_DOC_DIR",        "%{_localstatedir}/lib/%{name}");
define("GLPI_CACHE_DIR",      "%{_localstatedir}/lib/%{name}/_cache/");
define("GLPI_CRON_DIR",       "%{_localstatedir}/lib/%{name}/_cron");
define("GLPI_DUMP_DIR",       "%{_localstatedir}/lib/%{name}/_dumps");
define("GLPI_GRAPH_DIR",      "%{_localstatedir}/lib/%{name}/_graphs");
define("GLPI_LOCK_DIR",       "%{_localstatedir}/lib/%{name}/_lock/");
define("GLPI_PLUGIN_DOC_DIR", "%{_localstatedir}/lib/%{name}/_plugins");
define("GLPI_SESSION_DIR",    "%{_localstatedir}/lib/%{name}/_sessions");
define("GLPI_LOG_DIR",        "%{_localstatedir}/log/%{name}");
?>
EOF

install -d -m 755 %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d
cat > %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf <<EOF
Alias /%{name} %{_datadir}/%{name}

<Directory %{_datadir}/%{name}>
    Options -FollowSymLinks
    Require all granted
    # recommanded value
    php_value memory_limit 64M
</Directory>

<Directory %{_datadir}/%{name}/install>
    # 15" should be enough for migration in most case
    php_value max_execution_time 900
    php_value memory_limit 128M
</Directory>

<Directory %{_datadir}/%{name}/files>
    Require all denied
</Directory>

<Directory %{_datadir}/%{name}/inc>
    Require all denied
</Directory>

<Directory %{_datadir}/%{name}/locales>
    Require all denied
</Directory>

<Directory %{_datadir}/%{name}/mysql>
    Require all denied
</Directory>

<Directory %{_datadir}/%{name}/scripts>
    Require all denied
</Directory>
EOF

install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}/_cache
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}/_cron
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}/_dumps
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}/_graphs
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}/_lock
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}/_plugins
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}/_sessions
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}/_tmp
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}/_uploads

install -d -m 755 %{buildroot}%{_localstatedir}/log/%{name}

install -d -m 755 %{buildroot}%{_sysconfdir}/logrotate.d
cat > %{buildroot}%{_sysconfdir}/logrotate.d/%{name} <<EOF
/var/log/glpi/*.log {
    notifempty
    missingok
    create 644 apache apache
}
EOF

install -d -m 755 -p %{buildroot}%{_sysconfdir}/cron.d
cat > %{buildroot}%{_sysconfdir}/cron.d/%{name} <<EOF
# Run cron from to execute task even when no user connected
*/4 * * * * apache %{_bindir}/php %{_datadir}/%{name}/front/cron.php
EOF



%files
%doc CHANGELOG.txt README.txt
%{_datadir}/%name
%config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/cron.d/%{name}
%dir %attr(-,apache,apache) %{_sysconfdir}/glpi
%config(noreplace) %{_sysconfdir}/glpi/*
%attr(-,apache,apache) %{_localstatedir}/lib/%{name}
%attr(-,apache,apache) %{_localstatedir}/log/%{name}


%changelog
* Fri Aug 03 2012 Sergey Zhemoitel <serg@mandriva.org> 1:0.83.40-1mdv2012.0
+ Revision: 811648
- update to 0.83.4

* Fri Jul 13 2012 Sergey Zhemoitel <serg@mandriva.org> 1:0.83.31-1
+ Revision: 809120
- update to 0.83.31

* Mon Jun 11 2012 Sergey Zhemoitel <serg@mandriva.org> 1:0.83.2-1
+ Revision: 804444
- update to 0.83.2

* Wed Apr 25 2012 Sergey Zhemoitel <serg@mandriva.org> 1:0.83.1-1
+ Revision: 793305
- update to 0.83.1
- update to 0.83.1

* Mon Apr 09 2012 Sergey Zhemoitel <serg@mandriva.org> 1:0.83-1
+ Revision: 790018
- update version to 0.83

* Fri Feb 10 2012 Sergey Zhemoitel <serg@mandriva.org> 1:0.80.7-2
+ Revision: 772435
- new version 0.80.7

* Sat Feb 04 2012 Oden Eriksson <oeriksson@mandriva.com> 1:0.80.6-2
+ Revision: 771124
- various fixes

* Thu Jan 05 2012 Sergey Zhemoitel <serg@mandriva.org> 1:0.80.6-1
+ Revision: 757969
- add new release 0.80.6

* Wed Jan 04 2012 Sergey Zhemoitel <serg@mandriva.org> 1:0.80.5-2
+ Revision: 756433
+ rebuild (emptylog)

* Sun Nov 06 2011 Sergey Zhemoitel <serg@mandriva.org> 1:0.80.5-1
+ Revision: 722492
- new release 0.8.5

* Sun Oct 16 2011 Sergey Zhemoitel <serg@mandriva.org> 1:0.80.4-1
+ Revision: 704919
- imported package glpi
- new version 0.80.4

* Wed Sep 21 2011 Sergey Zhemoitel <serg@mandriva.org> 0.80.31-1
+ Revision: 700765
- new release 0.80.31

* Sat Aug 13 2011 Sergey Zhemoitel <serg@mandriva.org> 0.80.2-1
+ Revision: 694398
- new release 0.80.2
- new release 0.80.2
- new release 0.80.1
- update to 0.80.1 release

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - revert to 0.78.x branch, for fusioninventory compatibility

* Tue May 31 2011 Guillaume Rousse <guillomovitch@mandriva.org> 0.80-1
+ Revision: 682107
- new version

* Wed May 11 2011 Guillaume Rousse <guillomovitch@mandriva.org> 0.78.5-1
+ Revision: 673563
- new version
- new version

  + Sergey Zhemoitel <serg@mandriva.org>
    - update new version 0.78.3

* Sun Jan 23 2011 Guillaume Rousse <guillomovitch@mandriva.org> 0.78.2-1
+ Revision: 632442
- new version

* Mon Nov 15 2010 Guillaume Rousse <guillomovitch@mandriva.org> 0.78.1-1mdv2011.0
+ Revision: 597762
- new version

* Tue Oct 12 2010 Guillaume Rousse <guillomovitch@mandriva.org> 0.78-1mdv2011.0
+ Revision: 585228
- 0.78 final

* Sat Jul 17 2010 Guillaume Rousse <guillomovitch@mandriva.org> 0.78-0.RC2.1mdv2011.0
+ Revision: 554588
- new version

* Wed Mar 03 2010 Sandro Cazzaniga <kharec@mandriva.org> 0.72.4-1mdv2010.1
+ Revision: 513763
- New version
- fix License

* Tue Feb 23 2010 Guillaume Rousse <guillomovitch@mandriva.org> 0.72.3-4mdv2010.1
+ Revision: 510449
- don't ship .htaccess files

* Tue Feb 23 2010 Guillaume Rousse <guillomovitch@mandriva.org> 0.72.3-3mdv2010.1
+ Revision: 510433
- rely on filetrigger for reloading apache configuration begining with 2010.1,
  rpm-helper macros otherwise
- install everything directly under %%{_datadir}/%%{name}, and use apache
  configuration to restrict accesses

* Fri Nov 20 2009 Anne Nicolas <ennael@mandriva.org> 0.72.3-2mdv2010.1
+ Revision: 467625
- Fix #52614 in cooker

* Thu Nov 12 2009 Anne Nicolas <ennael@mandriva.org> 0.72.3-1mdv2010.1
+ Revision: 465413
- new version

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - new version

* Thu Jun 25 2009 Guillaume Rousse <guillomovitch@mandriva.org> 0.71.6-4mdv2010.0
+ Revision: 389132
- add missing directory under GLPI_DOC_DIR (Remi Collet)

* Sun Jun 21 2009 Guillaume Rousse <guillomovitch@mandriva.org> 0.71.6-3mdv2010.0
+ Revision: 387919
- FHS setup, following upstream advices
  (https://dev.indepnet.net/glpi/wiki/GlpiPackaging)

* Sun Jun 07 2009 Guillaume Rousse <guillomovitch@mandriva.org> 0.71.6-2mdv2010.0
+ Revision: 383461
- fix dependencies

* Fri Jun 05 2009 Guillaume Rousse <guillomovitch@mandriva.org> 0.71.6-1mdv2010.0
+ Revision: 383021
- new version
- don't duplicate spec-helper job
- fix build dependencies

* Wed Jan 28 2009 Jérôme Soyer <saispo@mandriva.org> 0.71.5-1mdv2009.1
+ Revision: 334794
- New upstream release

* Sun Jan 04 2009 Olivier Thauvin <nanardon@mandriva.org> 0.71.3-1mdv2009.1
+ Revision: 324879
- 0.71.3

* Thu Nov 13 2008 Nicolas Lécureuil <nlecureuil@mandriva.com> 0.71.2-1mdv2009.1
+ Revision: 302671
- New version 0.71.2

* Tue Sep 09 2008 Olivier Thauvin <nanardon@mandriva.org> 0.71.1-1mdv2009.0
+ Revision: 283114
- 0.71.1

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 0.70-3mdv2009.0
+ Revision: 246211
- rebuild

* Fri Jan 04 2008 Jérôme Soyer <saispo@mandriva.org> 0.70-1mdv2008.1
+ Revision: 145053
- New release

* Fri Dec 21 2007 Olivier Blin <blino@mandriva.org> 0.68.3-1mdv2008.1
+ Revision: 136445
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

