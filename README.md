# Pterodactyl-Discord-Bot
This is an open source Discord Bot project that allows you to manage the Pterodactyl Panel!

![getting a user](https://gyazo.com/b3153aa8ecbf2c006ad4ca7cc9163c04.gif)


# How to get started
- First what you need to get is your Pterodactyl Panel link and place it in the `PANEL_LINK` [section of the code](/bot.py) (under the `client` variable). Don't forget to include the `http(s)://` on the link too.
```py
 client = PterodactylClient('PANEL_LINK', 'SECRET_APPLICATION_API')
 ```
- You need to obtain your **super secret _applcation_ API** by doing: 
  - 1. Make sure you are in the Panel under _Admin Mode_ and head over to the `Application API` section to the left.
  ![admin application](https://gyazo.com/67b15ab1b11873fdae02f7038f47d8d2.gif)
  
    2. Click `Create New` in the top right corner. 
    
    ![create new](https://i.gyazo.com/c3ca37f6c68338ffc23d4626fe810c3e.png)
    
    3. Select all permissions as `Read & Write` 
    
    ![read and write perms](https://gyazo.com/b75fa03ff5d44d37683670ab13ba2f0b.png)
    
    4. Fill out the description with what you want!
    5. Click `Create Credentials`!
    6. ***Insert the `key` where `SECRET_APPLICATION_API` is in the code [section of the code](/bot.py) (under the `client` variable)***
    
    ![key](https://i.gyazo.com/819203a317365427348c6fad677ef6a6.png)
    ```py
    client = PterodactylClient('PANEL_LINK', 'SECRET_APPLICATION_API')
    ```
    

# Commands
- Normal Commands
  - `,ping` Allows you to check the bots latency.
  - `,uptime` Allows you to check how long the bot has been up for.
- Panel Commands
  - `,create <arg>` Creates `<arg>` which can be: `server`
  - `,getuser <user_attribute>` Allows you to lookup users on the panel.
  - `,link` Allows you to link a Discord user with a panel ID (must have [linked.json](/linked.json) to do it)
# Features
- Customizable: Bot Prefix, Panel Link, Application API, Bot Status, Bot Token
- Allows you to link Panel Users with Discord Users
- More **coming soon**
