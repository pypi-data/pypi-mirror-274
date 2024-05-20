import threading
import time
import requests
import json
import argparse
import os
import readline
import atexit
import sys
from colorama import init, Fore, Back, Style
banner=fr'''#####*************************************#####
#*********     {Fore.CYAN} Welcome to the {Fore.GREEN}      *********#
#      {Fore.CYAN}Kernel Bound Intelligence Project{Fore.GREEN}      #
#***~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~***#
#####*************************************#####
'''
logo=r'''
###*************###
##    (\{&}/)    ##
##    (>'.'<)    ##
##    (")_(")    ##
###################
'''
class KerBIClient:
    def __init__(self):
        parser = argparse.ArgumentParser(description="Flags and arguments for your KerBI console.\n\n")
        parser.add_argument('-c', '--channel', type=str, help="Add this channel to the 'Channel' field of all sent messages.\n")
        parser.add_argument('-w', '--workflow', type=str, help="Use the given workflow, overriding the default basicchat")

        parser.add_argument('-C', '--create_channel', type=str, help="Attempt to create channel upon successful connection, and use it for the rest of the session.\n")

        parser.add_argument('-s', '--server_address', type=str, help="Connect to the kserver running at <server_address> where server address is in format IP:PORT\n")
        parser.add_argument('-K', '--api_key', type=str, help="API key for authentication.\n")

        parser.add_argument('-m', '--message', type=str, help="Send message on successful connection. Use with 'no_console' to send\n")
        parser.add_argument('-A', '--attachment', type=str, help="Attach file with each message. DEPRECATED in favour of console slash commands.\n")

        parser.add_argument('-q', '--quiet', action='store_true', help="Return only the kmessage.text field and suppress all other console output.\n")
        parser.add_argument('-z', '--no_spinner', action='store_true', help="Disable the kerbi spinner.\n")
        parser.add_argument('-x', '--no_console', action='store_true', help="Do not open a console. Used for 'ping' tests and sending solo messages. Great for bash scripting.\n")
        self.args = parser.parse_args()

        if self.args and self.args.server_address:
            self.url = "http://" + self.args.server_address
        else:
            self.url = 'http://localhost:9393/'

    def spinner(self, stop_signal, spinner_strings):
        index = 0
        while not stop_signal():
            print(f'\r{spinner_strings[index % len(spinner_strings)]}', end='', flush=True)
            time.sleep(0.1)
            index += 1

    def send_single_message(self, text):
        try:
            headers = {}
            headers['Authorization'] = 'NO AUTH'
            channel = self.args.channel if self.args.channel is not None else "HOME"
            workflow = self.args.workflow if self.args.workflow is not None else "basicchat"
            attachment = self.args.attachment if self.args.attachment is not None else [""]
            data = {
                "channel": channel,
                "text": text,
                "to": "INT",
                "from": "USR",
                "workflow": workflow,
                "attachments": attachment
            }
            api_url = self.url

            jdata = json.dumps(data, indent=4)

            response = requests.post(api_url, json=data, headers=headers)
            response_kmessage = response.content.decode('utf-8')
            response_kmessage = json.loads(response_kmessage)

            if response.status_code == 200:
                print(response_kmessage['text'])
            else:
                print(f"Failed to send message. Status code: {response.status_code}")
        except Exception as e:
            print(e)

    def send_console_message(self, text):
        try:
            headers = {}
            headers['Authorization'] = 'NO AUTH'

            channel = self.args.channel if self.args.channel is not None else "HOME"
            workflow = self.args.workflow if self.args.workflow is not None else "basicchat"
            attachment = self.args.attachment if self.args.attachment is not None else [""]

            data = {
                "channel": channel,
                "text": text,
                "to": "INT",
                "from": "USR",
                "workflow": workflow,
                "attachments": attachment
            }
            if text.startswith('/'):
                command = self.parse_slash_command(text, data)
            else:
                command = False
            if command and not self.args.quiet:
                print(f"command received: {command}")

            if not self.args or not self.args.no_spinner:
                stop_signal = threading.Event()
                spinner_thread = threading.Thread(target=self.spinner, args=(stop_signal.is_set, [r"(\{&}/)", r"(\{@}/)", r"(\{%}/)", r"(\{#}/)", r"(\{$}/)"]))
                spinner_thread.start()

            # Send the message
            api_url = self.url
            print(Style.DIM)
            jdata = json.dumps(data, indent=4)
            if not args.quiet:
                print(f"Sending kmessage: {jdata}")

            response = requests.post(api_url, json=data, headers=headers)
            response_kmessage = response.content.decode('utf-8')
            response_kmessage = json.loads(response_kmessage)

            if not self.args or not self.args.no_spinner:
                stop_signal.set()
                spinner_thread.join()

            if response.status_code == 200:

                if not self.args or not self.args.quiet:
                    pretty_response = json.dumps(response_kmessage, indent=4)
                    print(f"{pretty_response}{Style.RESET_ALL}")

                print(response_kmessage['text'])
            else:
                print(f"Failed to send message. Status code: {response.status_code}")

#            if self.args and self.args.no_console:
#                quit()

        except KeyboardInterrupt:
            if not self.args or not self.args.no_spinner:
                stop_signal.set()
                spinner_thread.join()
            print("\nCancelling request. Server may still store message.")
            return

        except Exception as e:
            print(f"An error occurred: {e}")
            # Handle the exception as needed

    def console_interface(self):
        global logo, banner
        # The primitive included console allows the HOME channel and the SYSTEM channel
        if not self.args or not self.args.quiet:
            print(Fore.GREEN + banner + Style.RESET_ALL)
            print(Fore.GREEN + logo + Style.RESET_ALL)

        home_dir = os.path.expanduser("~")
        histfile = os.path.join(home_dir, '.klient_history')
        if not os.path.exists(histfile):
            print("No readline history found. Creating ./.klient_history...")
            with open(histfile, 'w') as f:
                pass
        # Load history from the file if it exists
        try:
            readline.read_history_file(histfile)
        except FileNotFoundError:
            print("Readline history not loaded. Console history will not be saved.")

        # Register a function to save the history file on exit
        atexit.register(readline.write_history_file, histfile)

        while True:
          # Wipe the message dictionary (will get defaults from the server)
            command = input(f"{Fore.CYAN}$___>{Style.RESET_ALL}")
            self.send_console_message(command)

    def parse_slash_command(self, text, data):
        slash_command = text.split()[0]

        text = (' '.join(text.split()[1:]))

        if slash_command == '/rag':
            filepath = input('RAG /path/to/file:')
            data['attachments'] = [filepath]
        else:
            print("Slash command not recognized.")
            return False
        return slash_command


def main():
    client = KerBIClient()
    if not client.args or not client.args.quiet:
        print(f"#KerBI Client V0.1#")
        print("Connecting to KerBI...")
        print(f"Server URL: {client.url}")

    try:
        if client.args and client.args.no_console:
            if not sys.stdin.isatty():
                message = sys.stdin.read().strip()
                client.send_single_message(message)
                exit()
            client.send_single_message(client.args.message)
            exit()
        client.console_interface()
#        while True:
#            text = input("> ")
#            client.send_message(text)
    except KeyboardInterrupt:
        print("\n")
        exit()
    except Exception as e:
        print(e)
        exit()


if __name__ == '__main__':
    main()

