![Workflow Status](https://github.com/ShopwareAcademy/AcademyStorefrontController/actions/workflows/e2e.yml/badge.svg)

# AcademyStorefrontController

A plugin which shows how to create a simple Storefront controller

## Features

- Adds Storefront controller with an external API ([unsplash](https://unsplash.com))
- Displays a link on the product detail page
- Opens modal on clicking the link and show an image

## Installation

1. Install and activate the plugin through the Administration UI:
   - Go to Extensions > My extensions
   - Find "Plugin with custom storefront controller" in the list
   - Click "Install"

Alternatively, you can use the command line:

```bash
bin/console plugin:refresh
bin/console plugin:install --activate AcademyStorefrontController
bin/console cache:clear
```

![pdp-link](https://github.com/user-attachments/assets/580a4cdf-c79b-4591-bc14-dc91ca073d77)
![modal](https://github.com/user-attachments/assets/3a19a75f-6532-4aa4-8df1-e27800987603)
