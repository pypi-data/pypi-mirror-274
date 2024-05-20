![Build Status](flet-route.png)
# This makes it easy to manage multiple views with dynamic routing.

This is an utility class based on repath library which allows matching ExpressJS-like routes and parsing their parameters, for example `/account/:account_id/orders/:order_id`.

## Differences from flet-route
- Flet-Route-Static is made to work with Flet Static Websites. The standard Flet-Route Package does not support this at the moment.
- Changes:
    - Removed `repath`  dependency.
    - Removed `flet` dependency (Static websites install `flet-pyodide` by itself)
    - Removed `CLI` commands (Does not need to be available in static websites)
### How To Use:
- Add `flet-easy-static` to your project `requirements.txt`
- How To Import Package:
```python
# Method 1: Importing the package as fs in your project 
import flet_route_static as fs
# Method 2: Check if the platform is emscripten and import the package accordingly
# This method is useful if you want to run the same code on both the desktop and the web and you don't have to install flet_route_static package on your desktop
if sys.platform == "emscripten":  # Check if in Pyodide environment
    import flet_route_static as fs
else:
    import flet_route as fs
  ```
- Now you can safely run `flet publish` on your static website application
### This pacakge is just a small modification of the original `Flet-Route` package and all the credit goes to the original author [Saurabh ](https://github.com/saurabhwadekar) 


### How to make `--route-url-strategy path` work in flet-route-static:
- Since a static webpage with flet is a singe page application, the `--route-url-strategy path` does not work as expected when hosted (Not when running main.py)
  - #### For Apache:
    - Check if `Include conf/extra/httpd-vhosts.conf` is uncommented in `httpd.conf`
    - Check if `LoadModule rewrite_module modules/mod_rewrite.so` is uncommented in `httpd.conf`
    - Modify `httpd-vhosts.conf` to look like this:
      ```apacheconf
      <VirtualHost *:80>
      ServerAdmin webmaster@yourdomain.com
      DocumentRoot "C:/xampp/htdocs"
      ServerName localhost
    
      <Directory "C:/xampp/htdocs/">
          Options Indexes FollowSymLinks Includes ExecCGI
          AllowOverride All
          Require all granted
    
          RewriteEngine On
          RewriteBase /
    
          # Exclude phpmyadmin and acustom from rewrite rules
          RewriteCond %{REQUEST_URI} ^/phpmyadmin [NC,OR]
          RewriteCond %{REQUEST_URI} ^/!custom [NC]
          RewriteRule ^ - [L]
    
          # If a file or directory exists, serve it directly
          RewriteCond %{REQUEST_FILENAME} -f [OR]
          RewriteCond %{REQUEST_FILENAME} -d
          RewriteRule ^ - [L]
    
          # Otherwise, rewrite all other requests to index.html
          RewriteRule ^ /index.html [L]
      </Directory>
    
      # Configuration for phpMyAdmin
      Alias /phpmyadmin "C:/xampp/phpMyAdmin"
    
      <Directory "C:/xampp/phpMyAdmin">
          Options Indexes FollowSymLinks
          AllowOverride All
          <RequireAny>
              # Localhost
              Require ip 127.0.0.1
              # IPv6 Localhost
              Require ip ::1
              # Specific IP
              Require ip 192.168.10.161     
          </RequireAny>
      </Directory>
    
      # Configuration for acustom directory
      Alias /!custom "C:/xampp/htdocs/!custom"
    
      <Directory "C:/xampp/htdocs/!custom">
          Options Indexes FollowSymLinks
          AllowOverride None
          Require all granted
      </Directory>
      </VirtualHost>
    
      # Configuration for phpMyAdmin
      Alias /phpmyadmin "C:/xampp/phpMyAdmin"
    
      <Directory "C:/xampp/phpMyAdmin">
          Options Indexes FollowSymLinks
          AllowOverride All
          <RequireAny>
              # Localhost
              Require ip 127.0.0.1
              # IPv6 Localhost
              Require ip ::1
              # Specific IP
              Require ip 192.168.10.161     
          </RequireAny>
      </Directory>
    
      # Configuration for acustom directory
      Alias /!custom "C:/xampp/htdocs/!custom"
    
      <Directory "C:/xampp/htdocs/!custom">
          Options Indexes FollowSymLinks
          AllowOverride None
          Require all granted
      </Directory>
      </VirtualHost>

    - This `httpd-vhosts.conf` file is for XAMPP. Modify it according to your server configuration
    - `!custom` is a directory in `htdocs` which is not affected by the rewrite rules
      - `htdocs` is the same directory where the `index.html` is located. In linux systems the directory is `/var/www/html` normally
    - `phpmyadmin` is also not affected by the rewrite rules
    - Everything else is redirected to `index.html` so that the SPA can handle the routing (Fixes so `website.com/route` works as expected)
  - #### For Nginx:
    - Work In Progress


## Installation
```
pip install flet-route-static
```

## Upgradation
```
pip install flet-route-static --upgrade
```


#### [📖 Read the documentation ](https://saurabhwadekar.github.io/flet-route-doc)


## Original Author:

<b>Name :</b> Saurabh Wadekar<br>
<b>Email :</b> saurabhwadekar420@gmail.com<br>
<b>County :</b> 🇮🇳INDIA🇮🇳<br>

### Changes made by: 
- SmokyAce
- Discrd: smokyace
