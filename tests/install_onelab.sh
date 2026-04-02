#!/bin/bash

# Copyright (c) 2018-2026 M. Schuler, TTZ-EMO, Hochschule für angewandte Wissenschaften Würzburg-Schweinfurt.
#
# Dieses Skript ist Teil von PyEMMO
# (siehe https://gitlab.ttz-emo.thws.de/ag-em/pyemmo).
#
# Dieses Programm ist freie Software: Sie können es weiterverbreiten und/oder ändern
# unter den Bedingungen der GNU General Public License, wie sie von der Free Software Foundation veröffentlicht wurde,
# entweder in der Version 3 der Lizenz oder (nach Ihrer Wahl) jeder späteren Version.
#
# Dieses Programm wird in der Hoffnung verteilt, dass es nützlich ist,
# jedoch OHNE JEDE GARANTIE; ohne sogar die implizite Garantie der
# MARKTGÄNGIGKEIT oder DER EIGNUNG FÜR EINEN BESTIMMTEN ZWECK. Siehe die
# GNU General Public License für weitere Details.
#
# Sie sollten eine Kopie der GNU General Public License zusammen mit diesem Programm erhalten haben.
# Falls nicht, siehe <http://www.gnu.org/licenses/>.
#

# Sicherstellen, dass wir im pyemmo-Ordner sind
current_folder_name=$(basename "$PWD")
current_folder_path="$PWD"

if [[ "$current_folder_name" != "pyemmo" && ! -d "$current_folder_path/tests" ]]; then
    if [[ "$current_folder_name" != "tests" ]]; then
        echo "Falscher Ordner! Nicht pyemmo oder tests oder kein Tests-Ordner gefunden"
        exit 1
    fi
    echo "Current folder is $current_folder_path"
else
    # In den tests-Ordner wechseln
    echo "cd tests"
    cd tests
fi

current_folder_name=$(basename "$PWD")
# update current dir
current_folder_path="$PWD"
echo "Current folder name is $current_folder_name"
today=$(date +'%y%m%d')

# Neuste ONELAB-Version herunterladen
# FIXME: Prüfen, ob ONELAB eine neue Version hat, bevor das gesamte Paket wieder heruntergeladen wird...
store_path="$current_folder_path/data/onelab"
onelab_path="$store_path/onelab-Linux64"

echo "Speicherpfad ist $store_path"
echo "isntall path ist $onelab_path"

if [ -d "$onelab_path" ]; then
    echo "ONELAB bereits installiert!"
else
    # ONELAB herunterladen und installieren
    mkdir -p "$store_path"

    zip_filepath="$store_path/onelab.zip"
    echo "Zip-Dateipfad ist: $zip_filepath"

    if [ -f "$zip_filepath" ]; then
        echo "onelab.zip wurde bereits heruntergeladen."
    else
        wget -O "$zip_filepath" 'https://onelab.info/files/onelab-Linux64.zip'
    fi

    if [ -d "$onelab_path" ]; then
        echo "onelab.zip wurde bereits entpackt."
    else
        unzip "$zip_filepath" -d "$store_path"
    fi

    if [ -f "$zip_filepath" ]; then
        rm "$zip_filepath"
    fi
fi

cd ..

# TODO: Prüfen, dass die ausführbaren Dateien tatsächlich existieren, bevor sie zurückgegeben werden!
echo "$store_path/onelab-Linux64/gmsh\n " "$store_path/onelab-Linux64/getdp"
