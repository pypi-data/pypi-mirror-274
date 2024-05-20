import os
import sys
from shutil import which
import subprocess
def alias_exists(alias_name):
    home = os.path.expanduser("~")
    shell_config_files = [".bashrc", ".zshrc"]

    for config_file in shell_config_files:
        config_path = os.path.join(home, config_file)
        if os.path.exists(config_path):
            with open(config_path, "r") as file:
                if alias_name in file.read():
                    return True
    return False

def add_alias_to_shell(alias_command):
    home = os.path.expanduser("~")
    shell_config_files = [".bashrc", ".zshrc"]

    for config_file in shell_config_files:
        config_path = os.path.join(home, config_file)
        if os.path.exists(config_path):
            with open(config_path, "a") as file:
                file.write(f"\n{alias_command}\n")

def env_var_exists(var_name):
    home = os.path.expanduser("~")
    shell_config_files = [".bashrc", ".zshrc"]

    for config_file in shell_config_files:
        config_path = os.path.join(home, config_file)
        if os.path.exists(config_path):
            with open(config_path, "r") as file:
                if var_name in file.read():
                    return True
    return False

def add_env_var_to_shell(env_var_command):
    home = os.path.expanduser("~")
    shell_config_files = [".bashrc", ".zshrc"]

    for config_file in shell_config_files:
        config_path = os.path.join(home, config_file)
        if os.path.exists(config_path):
            with open(config_path, "a") as file:
                file.write(f"\n{env_var_command}\n")

def ensure():
    # print('Running post install...')

    # eras_path = '/usr/local/bin/eras' #which("eras")
    # if not eras_path:
    #     print("Could not find 'eras' command in PATH. Please make sure it is installed correctly and run this script again.")
    #     sys.exit(1)
    #
    # alias_command = f"alias eras='{eras_path}'"
    # if not alias_exists("alias eras="):
    #     add_alias_to_shell(alias_command)
    #     print("Alias 'eras' added to shell configuration files.")
    # else:
        # print("Alias 'eras' already exists in shell configuration files.")

    if not env_var_exists("ERAS_OPENAI_KEY"):
        openai_key = input("Please enter your OpenAI API key (ERAS_OPENAI_KEY): ").strip()
        if not openai_key:
            print("Error: OpenAI API key cannot be empty.")
            sys.exit(1)
        env_var_command = f"export ERAS_OPENAI_KEY='{openai_key}'"
        os.environ['ERAS_OPENAI_KEY'] = openai_key # DO THIS FOR THE FIRST INSTALL !!!!
        add_env_var_to_shell(env_var_command)
        print("Environment variable 'ERAS_OPENAI_KEY' added to shell configuration files.")
        print('Please run source ~/.zshrc or open a new terminal window.')
        os.system(f'source {os.path.expanduser("~/.zshrc")}')

    reload_profile(get_profile_file())  # so the first install works with env vars
    # else:
        # print("Environment variable 'ERAS_OPENAI_KEY' already exists in shell configuration files.")

    # if not env_var_exists("ERAS_BASE_URL"):
    #     base_url = input("Please enter the base URL (ERAS_BASE_URL) [Optional] to point at Llama.cpp or other OpenAI server: ").strip()
    #     if base_url:
    #         command2 = f"export ERAS_BASE_URL='{base_url}'"
    #         add_env_var_to_shell(command2)
    #         print("Environment variable 'ERAS_BASE_URL' added to shell configuration files.")
        # else:
            # print("ERAS_BASE_URL not set.")
    # else:
    #     print("Environment variable 'ERAS_BASE_URL' already exists in shell configuration files.")


def get_profile_file():
    shell = os.environ.get('SHELL', '')
    if 'zsh' in shell:
        return os.path.expanduser('~/.zshrc')
    elif 'bash' in shell:
        bash_profile = os.path.expanduser('~/.bash_profile')
        if os.path.exists(bash_profile):
            return bash_profile
        else:
            return os.path.expanduser('~/.bashrc')
    else:
        # Add more shells as needed
        raise ValueError("Unsupported shell type")

def add_api_key_to_profile(api_key, profile_file):
    with open(profile_file, 'a') as file:
        file.write(f'\nexport MY_API_KEY="{api_key}"\n')

def reload_profile(profile_file):
    shell = os.environ.get('SHELL', '')
    if 'zsh' in shell:
        subprocess.run(['zsh', '-c', f'source {profile_file}'], check=True)
    elif 'bash' in shell:
        subprocess.run(['bash', '-c', f'source {profile_file}'], check=True)
    else:
        # Add more shells as needed
        print(f"Please manually source your profile file: {profile_file}")

if __name__ == "__main__":
    ensure()
