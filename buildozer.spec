[app]

# (str) Title of your application
title = Event Organizer

# (str) Package name
package.name = eventorganizer

# (str) Package domain (needed for android/ios packaging)
package.domain = com.eventorganizer

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directories to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin, venv

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
requirements = python3,kivy,openssl

# (str) Icon of the application
icon.filename = %(source.dir)s/Event logo.png  # Update according to your logo file name

# (list) Supported orientations
orientation = portrait

# (list) Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
# bin_dir = ./bin

# (str) Path to OpenSSL
openssl = /opt/homebrew/opt/openssl@3  # Update this path if necessary
