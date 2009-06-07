%define name glpi
%define version 0.71.6
%define release %mkrel 2
%define _requires_exceptions pear(domxml-php4-to-php5.php)

Summary: A web based park management
Name: %{name}
Version: %{version}
Release: %{release}
License: GPL
Group: Monitoring
Url: http://glpi.indepnet.org/
Source0: %{name}-%{version}.tar.gz
Requires: php-xml
Requires: mod_php > 2.0.54
BuildRequires:	rpm-helper >= 0.16
BuildRequires:	rpm-mandriva-setup >= 1.23
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

mkdir -p %buildroot%_var/www

(
cd %buildroot%_var/www
tar xzf %{SOURCE0}
)

# remove .htaccess files
find %{buildroot}%{_var}/www/%{name} -name .htaccess -exec rm -f {} \;

mkdir -p %buildroot%_sysconfdir/httpd/conf/webapps.d

cat > %buildroot%_sysconfdir/httpd/conf/webapps.d/%{name}.conf <<EOF
# %{name} configuration

Alias /%{name} /var/www/%{name}

<Directory /var/www/%{name}>
    Allow from all
    <Files helpdesk.html>
	ForceType text/html;charset=utf-8
    </Files>
</Directory>
<Directory /var/www/%{name}/docs>
    Deny from all
</Directory>
<Directory /var/www/%{name}/docs>
    Deny from all
</Directory>
<Directory /var/www/%{name}/backups/dump>
    Deny from all
</Directory>
<Directory /var/www/%{name}/backups/dump>
    Deny from all
</Directory>
<Directory /var/www/%{name}/glpi>
    Deny from all
</Directory>

EOF

cat > README.urpmi <<EOF

To properly end installation, you'll have to change permission on
/var/www/%{name}/glpi/config
/var/www/%{name}/docs
/var/www/%{name}/backups/dump
with chown apache

To setup the application, go on http://localhost/glpi/
You'll need a MySQL server and a dedicated database.

EOF

%clean
rm -rf %{buildroot}

%posttrans
%_post_webapp

%postun
%_postun_webapp

%files
%defattr(-,root,root)
%doc README.urpmi
%doc CHANGELOG.txt README.txt
%_sysconfdir/httpd/conf/webapps.d/%{name}.conf
%_var/www/%name
