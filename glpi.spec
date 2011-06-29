# don't update this package before a fusioninventory plugin is available
%define name	glpi
%define version	0.78.5
%define release %mkrel 1
%define _requires_exceptions pear(domxml-php4-to-php5.php)

Name:       %{name}
Version:    %{version}
Release:    %{release}
Summary:    A web based park management
License:    GPLv2
Group:      Monitoring
Url:        http://www.glpi-project.org/
Source0:    http://forge.indepnet.net/attachments/download/656/%{name}-%{version}.tar.gz
Requires:   php-xml
Requires:   mod_php
Requires:  php-mysql
%if %mdkversion < 201010
Requires(post):   rpm-helper
Requires(postun):   rpm-helper
%endif
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}

%description
GLPI is web based database application allowing to managed computers
and peripherals park. Its goal is to help technicians about maintenance
expiration, stock flow and license counting.

%prep
%setup -q -n %name

%install
rm -rf %{buildroot}

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
    Order allow,deny
    Allow from all
    # recommanded value
    php_value memory_limit 64M
</Directory>

<Directory %{_datadir}/%{name}/install>
    # 15" should be enough for migration in most case
    php_value max_execution_time 900
    php_value memory_limit 128M
</Directory>

<Directory %{_datadir}/%{name}/files>
    Order deny,allow
    Deny from all
</Directory>

<Directory %{_datadir}/%{name}/inc>
    Order deny,allow
    Deny from all
</Directory>

<Directory %{_datadir}/%{name}/locales>
    Order deny,allow
    Deny from all
</Directory>

<Directory %{_datadir}/%{name}/mysql>
    Order deny,allow
    Deny from all
</Directory>

<Directory %{_datadir}/%{name}/scripts>
    Order deny,allow
    Deny from all
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

%clean
rm -rf %{buildroot}

%post
%if %mdkversion < 201010
%_post_webapp
%endif

%postun
%if %mdkversion < 201010
%_postun_webapp
%endif

%files
%defattr(-,root,root)
%doc CHANGELOG.txt README.txt
%{_datadir}/%name
%config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/cron.d/%{name}
%dir %attr(-,apache,apache) %{_sysconfdir}/glpi
%config(noreplace) %{_sysconfdir}/glpi/*
%attr(-,apache,apache) %{_localstatedir}/lib/%{name}
%attr(-,apache,apache) %{_localstatedir}/log/%{name}
