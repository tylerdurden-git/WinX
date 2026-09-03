#!/bin/bash

echo "Setting up 'Super + X' shortcut..."

# Get current custom keybindings list
binding_list=$(gsettings get org.gnome.settings-daemon.plugins.media-keys custom-keybindings)

# Find next available slot index
if [ "$binding_list" = "@as []" ] || [ "$binding_list" = "[]" ] || [ -z "$binding_list" ]; then
    next_idx=0
    new_list="['/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/']"
else
    # Find count of existing custom shortcuts
    next_idx=$(echo "$binding_list" | grep -o 'custom[0-9]*' | sed 's/custom//' | sort -n | tail -1)
    if [ -z "$next_idx" ]; then
        next_idx=0
    else
        next_idx=$((next_idx + 1))
    fi
    path="/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom${next_idx}/"
    new_list=$(echo "$binding_list" | sed "s|]|, '$path']|")
fi

new_path="/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom${next_idx}/"

# Write schema keys
gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings "$new_list"
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:"$new_path" name 'WinX'
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:"$new_path" command '/usr/local/bin/winx'
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:"$new_path" binding '<Super>x'

echo "✅ Shortcut assigned successfully!"
echo "You can now press 'Win + X' to open the menu."
