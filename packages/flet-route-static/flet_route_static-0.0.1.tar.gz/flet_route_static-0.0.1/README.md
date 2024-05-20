![Build Status](flet-route.png)
# This makes it easy to manage multiple views with dynamic routing.

This is an utility class based on repath library which allows matching ExpressJS-like routes and parsing their parameters, for example `/account/:account_id/orders/:order_id`.

## Differences from flet-route
- Flet-Route-Static is made to work with Flet Static Websites. The standard Flet-Route Package does not support this at the moment.
- Changes:
    - Removed `repath`  dependency.
    - Removed `flet` dependency (Static websites install `flet-pyodide` by itself)
    - Removed `CLI` commands (Does not need to be available in static websites)

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
### Contact:
  - DISCORD: smokyace
