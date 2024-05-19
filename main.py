from modules.WebDriverInstaller import *
from modules.EsetTools import *
from modules.SharedTools import *
from modules.EmailAPIs import *

import traceback
import colorama
import platform
import datetime
import argparse
import time
import sys
import os
import re

LOGO = """
███████╗███████╗███████╗████████╗   ██╗  ██╗███████╗██╗   ██╗ ██████╗ ███████╗███╗   ██╗
██╔════╝██╔════╝██╔════╝╚══██╔══╝   ██║ ██╔╝██╔════╝╚██╗ ██╔╝██╔════╝ ██╔════╝████╗  ██║
█████╗  ███████╗█████╗     ██║      █████╔╝ █████╗   ╚████╔╝ ██║  ███╗█████╗  ██╔██╗ ██║
██╔══╝  ╚════██║██╔══╝     ██║      ██╔═██╗ ██╔══╝    ╚██╔╝  ██║   ██║██╔══╝  ██║╚██╗██║   
███████╗███████║███████╗   ██║      ██║  ██╗███████╗   ██║   ╚██████╔╝███████╗██║ ╚████║   
╚══════╝╚══════╝╚══════╝   ╚═╝      ╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝ ╚══════╝╚═╝  ╚═══╝                                                                      
                                                Project Version: v1.4.8.0
                                                Project Devs: rzc0d3r, AdityaGarg8, k0re,
                                                              Fasjeit, alejanpa17, Ischunddu,
                                                              soladify, AngryBonk, Xoncia
"""

args = {
    'chrome': True,
    'firefox': False,
    'edge': False,

    'key': True,
    'account': False,
    'business_key': False,
    'business_account': False,
    'only_update': False,

    'skip_webdriver_menu': False,
    'no_headless': False,
    'custom_browser_location': '',
    'email_api': 'developermail',
    'custom_email_api': False,
    'try_auto_cloudflare': False
}

MENU_EXECUTION = True

class MenuAction(object):
    def __init__(self, title, func):
        self.title = title
        self.function = func

    def render_title(self):
        return self.title
    
    def run(self):
        if isinstance(self.function, ViewMenu):
            self.function.view()
        else:
            self.function()

class OptionAction(object):
    def __init__(self, title, action, args_names, choices=[], default_value=None):
        self.title = title
        self.action = action
        self.value = default_value
        self.choices = choices
        self.args_names = args_names
        
    def render_title(self):
        if self.action in ['store_true', 'choice']:
            return f'{self.title} (selected: {colorama.Fore.YELLOW}{self.value}{colorama.Fore.RESET})'
        elif self.action == 'manual_input':
            return f'{self.title} (saved: {colorama.Fore.YELLOW}{self.value}{colorama.Fore.RESET})'
        elif self.action == 'bool_switch':
            if args[self.args_names.replace('-', '_')]:
                return f'{self.title} {colorama.Fore.GREEN}(enabled){colorama.Fore.RESET}'
            return f'{self.title} {colorama.Fore.RED}(disabled){colorama.Fore.RESET}'
        
    def run(self):
        if self.action == 'bool_switch':
            args[self.args_names.replace('-', '_')] = not args[self.args_names.replace('-', '_')]
            return True
        while MENU_EXECUTION:
            clear_console()
            print(self.title+'\n')
            menu_items = []
            if self.choices != []:
                menu_items = self.choices
            else:
                menu_items = self.args_names
            if self.action != 'manual_input':
                for index in range(0, len(menu_items)):
                    menu_item = menu_items[index]
                    print(f'{index+1} - {menu_item}')
                print()
            try:
                if self.action == 'manual_input':
                    self.value = input('>>> ').strip()
                    args[self.args_names.replace('-', '_')] = self.value # self.args_names is str
                    break
                index = int(input('>>> ').strip()) - 1
                self.value = menu_items[index]
                if index in range(0, len(menu_items)):
                    if self.action == 'store_true':
                        for args_name in self.args_names: # self.args_names is list
                            args[args_name.replace('-', '_')] = False
                        args[self.value.replace('-', '_')] = True # self.value == args_name
                    elif self.action == 'choice':
                        args[self.args_names.replace('-', '_')] = self.value # self.args_names is str
                    break
            except ValueError:
                pass

class ViewMenu(object):
    def __init__(self, title):
        self.title = title
        self.items = []

    def add_item(self, menu_action_object: MenuAction):
        self.items.append(menu_action_object)
    
    def view(self):
        while MENU_EXECUTION:
            clear_console()
            print(self.title+'\n')
            for item_index in range(0, len(self.items)):
                item = self.items[item_index]
                print(f'{item_index+1} - {item.render_title()}')
            print()
            try:
                selected_item_index = int(input('>>> ')) - 1
                if selected_item_index in range(0, len(self.items)):
                    print(self.items[selected_item_index].run())
            except ValueError:
                pass


def RunMenu():
    MainMenu = ViewMenu(LOGO+'\n---- Main Menu ----')

    SettingMenu = ViewMenu(LOGO+'\n---- Settings Menu ----')
    SettingMenu.add_item(
        OptionAction(
            title='Browsers',
            action='store_true',
            args_names=['chrome', 'firefox', 'edge'],
            default_value='chrome'
        )
    )
    SettingMenu.add_item(
        OptionAction(
            title='Modes of operation',
            action='store_true',
            args_names=['key', 'account', 'business-account', 'business-key', 'only-update'],
            default_value='key')
    )
    SettingMenu.add_item(
        OptionAction(
            title='Email APIs',
            action='choice',
            args_names='email-api',
            choices=['1secmail', 'hi2in', '10minutemail', 'tempmail', 'guerrillamail', 'developermail'],
            default_value='developermail'
        )
    )
    SettingMenu.add_item(
        OptionAction(
            title='--skip-webdriver-menu',
            action='bool_switch',
            args_names='skip-webdriver-menu'
        )
    )
    SettingMenu.add_item(
        OptionAction(
            title='--no-headless',
            action='bool_switch',
            args_names='no-headless'
        )
    )
    SettingMenu.add_item(
        OptionAction(
            title='--custom-browser-location',
            action='manual_input',
            args_names='custom-browser-location',
            default_value=''
        )
    )
    SettingMenu.add_item(
        OptionAction(
            title='--custom-email-api',
            action='bool_switch',
            args_names='custom-email-api'
        )
    )
    SettingMenu.add_item(
        OptionAction(
            title='--try-auto-cloudflare',
            action='bool_switch',
            args_names='try-auto-cloudflare'
        )
    )
    SettingMenu.add_item(MenuAction('Back', MainMenu))

    MainMenu.add_item(MenuAction('Settings', SettingMenu))
    MainMenu.add_item(MenuAction(f'{colorama.Fore.LIGHTWHITE_EX}Do it, damn it!{colorama.Fore.RESET}', main))
    MainMenu.add_item(MenuAction('Exit', sys.exit))
    MainMenu.view()

def parse_argv():
    print(LOGO)
    if len(sys.argv) == 1: # Menu
        #global MENU_EXECUTION
        #MENU_EXECUTION = True
        RunMenu()
    else: # CLI
        args_parser = argparse.ArgumentParser()
        # Required
        ## Browsers
        args_browsers = args_parser.add_mutually_exclusive_group(required=True)
        args_browsers.add_argument('--chrome', action='store_true', help='Launching the project via Google Chrome browser')
        args_browsers.add_argument('--firefox', action='store_true', help='Launching the project via Mozilla Firefox browser')
        args_browsers.add_argument('--edge', action='store_true', help='Launching the project via Microsoft Edge browser')
        ## Modes of operation
        args_modes = args_parser.add_mutually_exclusive_group(required=True)
        args_modes.add_argument('--key', action='store_true', help='Generating an ESET-HOME license key (example as AGNV-XA2V-EA89-U546-UVJP)')
        args_modes.add_argument('--account', action='store_true', help='Generating an ESET HOME Account (To activate the free trial version)')
        args_modes.add_argument('--business-account', action='store_true', help='Generating an ESET BUSINESS Account (To huge businesses) - Requires manual captcha input!!!')
        args_modes.add_argument('--business-key', action='store_true', help='Generating an ESET BUSINESS Account and creating a universal license key for ESET products (1 key - 75 devices) - Requires manual captcha input!!!')
        args_modes.add_argument('--only-update', action='store_true', help='Updates/installs webdrivers and browsers without generating account and license key')
        # Optional
        args_parser.add_argument('--skip-webdriver-menu', action='store_true', help='Skips installation/upgrade webdrivers through the my custom wrapper (The built-in selenium-manager will be used)')
        args_parser.add_argument('--no-headless', action='store_true', help='Shows the browser at runtime (The browser is hidden by default, but on Windows 7 this option is enabled by itself)')
        args_parser.add_argument('--custom-browser-location', type=str, default='', help='Set path to the custom browser (to the binary file, useful when using non-standard releases, for example, Firefox Developer Edition)')
        args_parser.add_argument('--email-api', choices=['1secmail', 'hi2in', '10minutemail', 'tempmail', 'guerrillamail', 'developermail'], default='developermail', help='Specify which api to use for mail')
        args_parser.add_argument('--custom-email-api', action='store_true', help='Allows you to manually specify any email, and all work will go through it. But you will also have to manually read inbox and do what is described in the documentation for this argument')
        args_parser.add_argument('--try-auto-cloudflare',action='store_true', help='Removes the prompt for the user to press Enter when solving cloudflare captcha. In some cases it may go through automatically, which will give the opportunity to use tempmail in automatic mode!')
        try:
            global args
            args = vars(args_parser.parse_args())
        except:
            time.sleep(3)
            sys.exit(-1)

def main():
    if len(sys.argv) == 1: # for Menu
        print()
    try:
        # initialization and configuration of everything necessary for work
        webdriver_installer = WebDriverInstaller()
        # changing input arguments for special cases
        if platform.release() == '7' and sys.platform.startswith('win'): # fix for Windows 7
            args['no_headless'] = True
        elif args['business_account'] or args['business_key'] or args['email_api'] in ['tempmail']:
            args['no_headless'] = True
        
        driver = None
        webdriver_path = None
        browser_name = 'chrome'
        if args['firefox']:
            browser_name = 'firefox'
        if args['edge']:
            browser_name = 'edge'
        if not args['skip_webdriver_menu']: # updating or installing webdriver
            webdriver_path = webdriver_installer.webdriver_installer_menu(args['edge'], args['firefox'])
            if webdriver_path is not None:
                os.chmod(webdriver_path, 0o777)
        if not args['only_update']:
            driver = initSeleniumWebDriver(browser_name, webdriver_path, args['custom_browser_location'], (not args['no_headless']))
            if driver is None:
                raise RuntimeError(f'Initialization {browser_name}-webdriver error!')
        else:
            sys.exit(0)

        # main part of the programd
        if not args['custom_email_api']:
            console_log(f'\n[{args["email_api"]}] Mail registration...', INFO)
            if args['email_api'] == '10minutemail':
                email_obj = TenMinuteMailAPI(driver)
            elif args['email_api'] == 'hi2in':
                email_obj = Hi2inAPI(driver)
            elif args['email_api'] == 'tempmail':
                email_obj = TempMailAPI(driver, args['try_auto_cloudflare'])
            elif args['email_api'] == 'guerrillamail':
                email_obj = GuerRillaMailAPI(driver)
            elif args['email_api'] == 'developermail':
                email_obj = DeveloperMailAPI()
            elif args['email_api'] == '1secmail':
                email_obj = OneSecEmailAPI()
            email_obj.init()
            console_log('Mail registration completed successfully!', OK)
        else:
            email_obj = CustomEmailAPI()
            while True:
                email = input(f'\n[  {colorama.Fore.YELLOW}INPT{colorama.Fore.RESET}  ] {colorama.Fore.CYAN}Enter the email address you have access to: {colorama.Fore.RESET}').strip()
                try:
                    matched_email = re.match(r"[-a-z0-9+]+@[a-z]+\.[a-z]{2,3}", email).group()
                    if matched_email == email:
                        email_obj.email = matched_email
                        console_log('Mail has the correct syntax!', OK)
                        break
                    else:
                        raise RuntimeError
                except:
                    console_log('Invalid email syntax!!!', ERROR)
        eset_password = createPassword(10)
        
        # standart generator
        if args['account'] or args['key']:
            EsetReg = EsetRegister(email_obj, eset_password, driver)
            EsetReg.createAccount()
            EsetReg.confirmAccount()
            output_line = '\n'.join([
                    '',
                    '----------------------------------',
                    f'Account Email: {email_obj.email}',
                    f'Account Password: {eset_password}',
                    '----------------------------------',
                    ''
            ])        
            output_filename = 'ESET ACCOUNTS.txt'
            if args['key']:
                output_filename = 'ESET KEYS.txt'
                EsetKeyG = EsetKeygen(email_obj, driver)
                EsetKeyG.sendRequestForKey()
                license_name, license_key, license_out_date = EsetKeyG.getLicenseData()
                output_line = '\n'.join([
                    '',
                    '----------------------------------',
                    f'Account Email: {email_obj.email}',
                    f'Account Password: {eset_password}',
                    '',
                    f'License Name: {license_name}',
                    f'License Key: {license_key}',
                    f'License Out Date: {license_out_date}',
                    '----------------------------------',
                    ''
                ])
                
        # new generator
        elif args['business_account'] or args['business_key']:
            EsetBusinessReg = EsetBusinessRegister(email_obj, eset_password, driver)
            EsetBusinessReg.createAccount()
            EsetBusinessReg.confirmAccount()
            output_line = '\n'.join([
                    '',
                    '----------------------------------',
                    f'Business Account Email: {email_obj.email}',
                    f'Business Account Password: {eset_password}',
                    '----------------------------------',
                    ''
            ])    
            output_filename = 'ESET ACCOUNTS.txt'
            if args['business_key']:
                output_filename = 'ESET KEYS.txt'
                EsetBusinessKeyG = EsetBusinessKeygen(email_obj, eset_password, driver)
                EsetBusinessKeyG.sendRequestForKey()
                license_name, license_key, license_out_date = EsetBusinessKeyG.getLicenseData()
                output_line = '\n'.join([
                    '',
                    '----------------------------------',
                    f'Business Account Email: {email_obj.email}',
                    f'Business Account Password: {eset_password}',
                    '',
                    f'License Name: {license_name}',
                    f'License Key: {license_key}',
                    f'License Out Date: {license_out_date}',
                    '----------------------------------',
                    ''
                ])        
        # end
        console_log(output_line)
        date = datetime.datetime.now()
        f = open(f"{str(date.day)}.{str(date.month)}.{str(date.year)} - "+output_filename, 'a')
        f.write(output_line)
        f.close()
        driver.quit()
    
    except Exception as E:
        traceback_string = traceback.format_exc()
        if str(type(E)).find('selenium') and traceback_string.find('Stacktrace:') != -1: # disabling stacktrace output
            traceback_string = traceback_string.split('Stacktrace:', 1)[0]
        console_log(traceback_string, ERROR)
    if len(sys.argv) == 1:
        input('Press Enter to exit...')
    else:
        time.sleep(3) # exit-delay
    sys.exit()

if __name__ == '__main__':
    parse_argv() # if Menu, the main function will be called in automatic mode
    if len(sys.argv) > 1: # CLI
        main()