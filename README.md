# Ansible Role for Secure Moodle Deployment

Based on the original [Ansible Role for Moodle](https://github.com/geoffreyvanwyk/ansible-role-moodle) by [Geoffrey van Wyk](https://github.com/geoffreyvanwyk).

Extended for security and support for Moodle 5.1+

Deploys, installs, and upgrades [Moodle](https://moodle.org) on [Ubuntu](https://ubuntu.com) servers with enterprise-grade security configurations.

## Features

### Security Enhancements

- **Modern TLS Configuration**: TLS 1.2+ only with Mozilla Modern cipher suites
- **HTTP/2 Support**: Improved performance and security
- **Automatic Let's Encrypt SSL**: Production-ready SSL certificates
- **Security Headers**: HSTS, X-Frame-Options, and more
- **Secure Password Storage**: Encrypted credential management
- **OCSP Stapling**: Enhanced certificate validation
- **SSL Session Caching**: Improved TLS handshake performance

### Deployment Features

- Automated Moodle 5.1+ deployment
- Production and development environment support
- PHP 8.4+ with security hardening
- PostgreSQL 16+ or MariaDB support
- Plugin installation from Moodle Plugin Directory or Git

## Requirements

- **Control Node** (where you run Ansible):

  - Ansible 2.9+
  - Python 3.8+

- **Target Server** (where Moodle will be installed):
  - Ubuntu 20.04 LTS or 22.04 LTS
  - Minimum 2GB RAM (4GB+ recommended)
  - Minimum 10GB disk space
  - SSH access with sudo privileges

## Quick Start

### 1. Install Dependencies

```bash
ansible-galaxy install -r requirements.yml
```

### 2. Create Inventory File

Create an inventory file `cp example.inventory inventory.ini`:

```ini
[production]
moodle_server ansible_host=YOUR_SERVER_IP ansible_user=ubuntu

[production:vars]
moodle_web_domain=example.com
moodle_web_protocol=https
moodle_web_letsencrypt=true
moodle_env=production
moodle_admin_email=admin@example.com
moodle_version=5.1
```

### 3. Run Deployment

```bash
ansible-playbook -i inventory.ini playbook.yml -K
```

## Configuration

### Basic Configuration

| Variable                 | Default      | Description                                |
| ------------------------ | ------------ | ------------------------------------------ |
| `moodle_version`         | `5.1`        | Moodle version to install                  |
| `moodle_env`             | `production` | Environment: `production` or `development` |
| `moodle_web_domain`      | `127.0.0.1`  | Domain name for Moodle                     |
| `moodle_web_protocol`    | `http`       | Protocol: `http` or `https`                |
| `moodle_web_letsencrypt` | `true`       | Use Let's Encrypt for SSL in production    |

### Database Configuration

| Variable             | Default        | Description                         |
| -------------------- | -------------- | ----------------------------------- |
| `moodle_db_install`  | `true`         | Install database service            |
| `moodle_db_type`     | `pgsql`        | Database type: `pgsql` or `mariadb` |
| `moodle_db_name`     | Auto-generated | Database name                       |
| `moodle_db_username` | `moodler`      | Database username                   |
| `moodle_db_password` | Auto-generated | Database password                   |

### Advanced Configuration

See `roles/secure_moodle/defaults/main.yml` for complete configuration options.

## Security Features Explained

### 1. SSL/TLS Configuration

- **TLS 1.2 and 1.3 Only**: Disables older, vulnerable protocols
- **Strong Cipher Suites**: Uses Mozilla Modern compatibility list
- **Perfect Forward Secrecy**: Enabled through ECDHE and DHE ciphers
- **OCSP Stapling**: Reduces certificate validation latency

### 2. HTTP Security Headers

The role configures comprehensive security headers:

- **HSTS**: Forces HTTPS for 2 years with preload
- **CSP**: Content Security Policy to prevent XSS
- **X-Frame-Options**: Prevents clickjacking
- **X-Content-Type-Options**: Prevents MIME sniffing
- **Referrer-Policy**: Controls referrer information
- **Permissions-Policy**: Restricts browser features

### 3. Certificate Management

- **Production**: Automatic Let's Encrypt certificates with auto-renewal
- **Development**: Self-signed 4096-bit RSA certificates
- **Validation**: Pre-deployment certificate verification

### 4. Secure Defaults

- PHP session cookies: HttpOnly, Secure, SameSite=Lax
- Database passwords: 32-character with special characters
- File permissions: Restrictive defaults throughout
- Apache: Disabled directory listing and sensitive file access

## Examples

### Production Deployment with Let's Encrypt

```yaml
# inventory.ini
[production]
web1 ansible_host=203.0.113.10

[production:vars]
moodle_web_domain=learn.example.com
moodle_web_protocol=https
moodle_web_letsencrypt=true
moodle_env=production
moodle_admin_email=admin@example.com
moodle_site_fullname=Example Learning Portal
moodle_site_shortname=ELP
moodle_db_type=pgsql
```

### Development Deployment

```yaml
# inventory.ini
[development]
dev ansible_host=192.168.1.100

[development:vars]
moodle_web_domain=moodle.local
moodle_web_protocol=https
moodle_env=development
moodle_admin_email=dev@example.com
moodle_db_type=pgsql
```

### Installing Plugins

```yaml
# In your playbook or inventory vars
moodle_plugins:
  - name: availability_xp
    archive: "https://moodle.org/plugins/download.php/30440/availability_xp_moodle44_2023110700.zip"

moodle_plugins_git:
  - name: theme_boost_campus
    repository: https://github.com/moodle-an-hochschulen/moodle-theme_boost_campus
    version: MOODLE_401_STABLE
```

## Troubleshooting

### Common Issues

1. **SSL Protocol Error**: See [SECURITY_FIXES.md](SECURITY_FIXES.md#ssl-protocol-error)
2. **Certificate Not Found**: Verify Let's Encrypt installation
3. **HTTP/2 Not Working**: Check Apache module enablement
4. **Database Connection Failed**: Verify credentials and service status

### Verification Commands

```bash
# Check SSL certificate
sudo openssl s_client -connect example.com:443 -showcerts

# Verify Apache configuration
sudo apache2ctl -t
sudo apache2ctl -S

# Check running services
sudo systemctl status apache2
sudo systemctl status postgresql
sudo systemctl status php8.1-fpm

# View logs
sudo tail -f /var/log/apache2/*-ssl-error.log
```

## Testing

### SSL/TLS Testing

```bash
# Online tools
# SSL Labs: https://www.ssllabs.com/ssltest/
# SecurityHeaders: https://securityheaders.com/

```

### Ansible Testing

The role includes Molecule tests for various scenarios:

```bash
# Test default configuration
molecule test

# Test with MariaDB
molecule test -s mariadb

# Test plugin installation
molecule test -s plugins
```

## Security Documentation

For detailed security information, see [SECURITY_FIXES.md](SECURITY_FIXES.md).

## Upgrading

To upgrade an existing Moodle installation:

1. Update `moodle_version` in your inventory
2. Set `moodle_deploy_update: true`
3. Run the playbook:

```bash
ansible-playbook -i inventory.ini playbook.yml -K
```

The role will:

- Pull the latest code from the specified version
- Run database upgrades
- Update plugins
- Apply configuration changes

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Molecule
5. Submit a pull request

## License

GNU General Public License v3.0 or later

See [LICENSE](LICENSE) for full license text.

## Credits

- Original role by [Geoffrey van Wyk](https://github.com/geoffreyvanwyk)
- Security enhancements and Moodle 5.1+ support by the community

## Support

- For bugs and feature requests: Open an issue
- For Moodle questions: [Moodle Forums](https://moodle.org/forums/)
- For security vulnerabilities: See [SECURITY_FIXES.md](SECURITY_FIXES.md)

## Roadmap

- [ ] Support for Nginx web server
- [ ] Redis/Memcached integration
- [ ] Docker deployment option
- [ ] Multi-server (cluster) deployment
- [ ] Automated backup configuration
- [ ] WAF (Web Application Firewall) integration
- [ ] Monitoring and alerting setup
