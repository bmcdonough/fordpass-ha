# documenting how to implement using the fordpass-ha library outside of homeassistant
## initial configuration uses fordpass.config_flow
```shell
Jun 13 21:45:57 hostname homeassistant/8280ec07e0a1[146]: #033[36m2024-06-13 21:45:57.703 DEBUG (MainThread) [custom_components.fordpass.config_flow:146}] USA#033[0m
Jun 13 21:45:57 hostname homeassistant/8280ec07e0a1[146]: #033[36m2024-06-13 21:45:57.703 DEBUG (MainThread) [custom_components.fordpass.config_flow:190}] Region#033[0m
Jun 13 21:45:57 hostname homeassistant/8280ec07e0a1[146]: #033[36m2024-06-13 21:45:57.703 DEBUG (MainThread) [custom_components.fordpass.config_flow:191}] USA#033[0m
Jun 13 21:45:57 hostname homeassistant/8280ec07e0a1[146]: #033[36m2024-06-13 21:45:57.703 DEBUG (MainThread) [custom_components.fordpass.config_flow:211}] {'region': '71A3AD0A-CF46-4CCF-B473-FC7FE5BC4592', 'locale': 'en-US', 'locale_short': 'USA', 'locale_url': 'https://login.ford.com'}#033[0m
```
### within fordpass.config_flow, function async_step_user
1. requires user_input of username and region
1. jumps to async_step_token, supplying it with None
### within fordpass.config_flow, function async_step_token
1. if user_input is None
1. skips to checking if self.region is not None, we set that with async_step_user with user_input
1. returns with async_show_form
1. supplies auth URL
1. waits for user_input of tokenstr
### within fordpass.config_flow, function generate_url
1. interesting, I do not think it uses the username at all in the generation of the auth url
