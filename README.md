# woffu-autologin-script
This is a small script that auto checks you into your Woffu organization, based on the original https://github.com/d-hervas/woffu-autologin-script

I forked this project from the original to add support for automatic detection of working days. Working days are defined as:

* not in the weekend
* not a requested PTO
* and not a bank holiday

The script won't sign in if today is detected as a non-working day.

The simplest way to use it is to set up a cron job / scheduled task that signs you on/off. The script does not know anything about changes in your working hours (i.e. summer schedule) and you need to address that in your cron job.


## Usage Guide
This Python script facilitates automatic sign-ins and sign-outs for Woffu, a platform often used for employee time tracking and management.

### Step 1: Clone the Repository

First, you need to clone the repository to your local machine. Open a terminal or command prompt and run:

```bash
git clone https://github.com/enlavin/woffu-autologin-script.git
cd woffu-autologin-script
```

This command downloads the script and its accompanying files into a directory named woffu-autologin-script and then changes into that directory.
### Step 2: Install Dependencies

The script requires Python to run. Ensure you have Python installed on your system. You can download Python from python.org.

After installing Python, install the necessary Python packages. From within the woffu-autologin-script directory, run:

```bash
pip install -r requirements.txt
```
This command installs all the dependencies listed in the requirements.txt file, ensuring the script has all the Python packages it needs to run. 
### Step 3: Setting Up Credentials

The script uses JSON files to store your Woffu credentials securely. You have two options for credential files:

* .woffu-autologin-script.json
* data.json

Place one of these files in your home directory or in the same directory as the script with the following content:

```json
{
  "username": "your_username",
  "password": "your_password"
}
```
Replace your_username and your_password with your actual Woffu credentials.
If Credentials Are Not Found
If the script cannot find a credentials file or if the file does not contain valid credentials, it will prompt you to manually enter your username and password.
### Step 4: Running the Script

With your credentials set up, you're ready to run the script. Execute it with:
```bash
python run.py
```

The script will search for your credentials, log you into Woffu, and handle sign-in or sign-out based on the current time and your working schedule.
Optional: Environment Variables

You can customize the script's behavior using environment variables:
*    WOFFU_DRY_RUN: If set to 1, yes, or true, the script runs in dry-run mode, simulating actions without making actual sign-ins or sign-outs.
*    WOFFU_WAIT_RANDOM: Defines the maximum wait time in seconds before performing an action, adding randomness to the timing of sign-ins or sign-outs.

Set these variables in your environment before running the script to apply these customizations.

# Telegram support

The telegram support relies on these environtment vars: 
* WOFFU_TELEGRAM_APITOKEN
* WOFFU_TELEGRAM_CHATID

The first one is the Telegram ChatBot API Token that you can get from the @BotFather.
And the second one is the ID of the chat you want it to sent the messages.

Once these two vars are set every execution will output its result to this chat, so you can easily track that your signins are running fine (or not).
