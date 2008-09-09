%define name glpi
%define version 0.71.1
%define release %mkrel 1

Summary: A web based park management
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.gz
License: GPL
Group: Monitoring
Url: http://glpi.indepnet.org/
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires: apache-base > 2.0.54-5mdk
BuildArch: noarch
Requires: php-xml
Requires: mod_php > 2.0.54

%description
GLPI is web based database application allowing to managed computers
and peripherals park. Its goal is to help technicians about maintenance
expiration, stock flow and license counting.

%prep
%setup -q -n %name

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p %buildroot%_var/www

(
cd %buildroot%_var/www
tar xzf %{SOURCE0}
)

# remove .htaccess files
find $RPM_BUILD_ROOT%{_var}/www/%{name} -name .htaccess -exec rm -f {} \;

## strip away annoying ^M
find $RPM_BUILD_ROOT%{_var}/www/%{name} -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find $RPM_BUILD_ROOT%{_var}/www/%{name} -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

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
rm -rf $RPM_BUILD_ROOT

%posttrans
%_post_webapp

%postun
%_postun_webapp

%files
%defattr(-,root,root)
%doc README.urpmi
%doc CHANGELOG.txt AUTHORS.txt README.txt
%_sysconfdir/httpd/conf/webapps.d/%{name}.conf
%_var/www/%name



