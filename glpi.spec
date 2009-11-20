%define name glpi
%define version 0.72.3
%define release %mkrel 2
%define _requires_exceptions pear(domxml-php4-to-php5.php)

Name:       %{name}
Version:    %{version}
Release:    %{release}
Summary:    A web based park management
License:    GPL
Group:      Monitoring
Url:        http://glpi.indepnet.org/
Source0:    %{name}-%{version}.tar.gz
Requires:   php-xml
Requires:   mod_php > 2.0.54
BuildRequires:	rpm-helper >= 0.16
BuildRequires:	rpm-mandriva-setup >= 1.23
Requires:  php-mysql
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

install -d -m 755 %{buildroot}%{_datadir}/%{name}/www
install -m 644 *.php *.js %{buildroot}%{_datadir}/%{name}/www

for i in ajax css front install lib pics plugins; do
    cp -ar $i %{buildroot}%{_datadir}/%{name}/www/$i
done

mv %{buildroot}%{_datadir}/%{name}/www/install/mysql \
    %{buildroot}%{_datadir}/%{name}/
pushd %{buildroot}%{_datadir}/%{name}/www/install
ln -s ../../mysql .
popd

for i in locales scripts inc; do
    cp -ar $i %{buildroot}%{_datadir}/%{name}/$i
    pushd %{buildroot}%{_datadir}/%{name}/www
    ln -sf ../$i $i
    popd
done

install -d -m 755 %{buildroot}%{_sysconfdir}/glpi
install -m 644 config/*.php %{buildroot}%{_sysconfdir}/glpi
pushd %{buildroot}%{_datadir}/%{name}/www
ln -sf ../../../..%{_sysconfdir}/glpi config
popd

cat > %{buildroot}%{_sysconfdir}/glpi/config_path.php <<EOF
<?php
// for packaging defaults

define("GLPI_CONFIG_DIR",     "%{_sysconfdir}/glpi");

define("GLPI_DOC_DIR",        "%{_localstatedir}/lib/%{name}");
define("GLPI_DUMP_DIR",       "%{_localstatedir}/lib/%{name}/_dumps");
define("GLPI_CACHE_DIR",      "%{_localstatedir}/lib/%{name}/_cache/");
define("GLPI_CRON_DIR",       "%{_localstatedir}/lib/%{name}/_cron");
define("GLPI_SESSION_DIR",    "%{_localstatedir}/lib/%{name}/_sessions");
define("GLPI_PLUGIN_DOC_DIR", "%{_localstatedir}/lib/%{name}/_plugins");
define("GLPI_LOCK_DIR",       "%{_localstatedir}/lib/%{name}/_lock/");

define("GLPI_LOG_DIR",        "%{_localstatedir}/log/%{name}");
?>
EOF

install -d -m 755 %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d
cat > %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf <<EOF
# %{name} configuration

Alias /%{name} %{_datadir}/%{name}/www

<Directory %{_datadir}/%{name}/www>
    Options -FollowSymLinks
    Allow from all
    # recommanded value
    php_value memory_limit 64M
</Directory>

<Directory %{_datadir}/%{name}/www/install>
    # 15" should be enough for migration in most case
    php_value max_execution_time 900
    php_value memory_limit 128M
</Directory>
EOF

install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}/_dumps
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}/_cache
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}/_cron
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}/_sessions
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}/_plugins
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}/_lock
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}/_tmp

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
*/4 * * * * apache %{_bindir}/php %{_datadir}/%{name}/www/front/cron.php
EOF

%clean
rm -rf %{buildroot}

%posttrans
%_post_webapp

%postun
%_postun_webapp

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
