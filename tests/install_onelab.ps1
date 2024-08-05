#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of Applied Sciences Wuerzburg-Schweinfurt.
#
# This file is part of PyEMMO
# (see https://gitlab.ttz-emo.thws.de/ag-em/pyemmo).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

# Make sure we are in the pyemmo folder
$current_folder_name = Get-Location | Split-Path -Leaf
$current_folder_path = Get-Location
if ($current_folder_name -ne "pyemmo" -and (Test-Path "$current_folder_path\tests") -ne $true) {
    if ($current_folder_name -ne "tests") {
        Write-Error "Wrong folder! Not pyemmo or tests or containing tests"
        exit 1
    }
}
else {
    # Go into tests folder
    Set-Location .\tests
}
$current_folder_name = Get-Location
$today = Get-Date -Format "yyMMdd"
# Download newest ONELAB version
# FIXME: Check ONELAB for new verion BEFORE downloading the whole package again...
# $store_path = Join-Path -Path $current_folder_name  -ChildPath ("data\" + $today + "_onelab")
$store_path = Join-Path -Path $current_folder_name  -ChildPath ("data\onelab")
# $store_path_fake = Join-Path -Path $current_folder_name  -ChildPath ("data\onelab1")
Write-Output "Store path is $store_path"

if (Test-Path $store_path) {
    # Write-Output "Onelab for date $(Get-Date) allready installed"
    Write-Output "Onelab already installed!"
}
else {
    # download and install ONELAB!
    # Remove-Item $test_path -Recurse -Force -Confirm:$false
    New-Item -Path $store_path -ItemType Directory

    $zip_filepath = $store_path + "\onelab.zip"
    Write-Output("Zip file path is: $zip_filepath")
    if (Test-Path $zip_filepath) {
        Write-Output("onelab.zip has already been downloaded.")
    }
    else {
    (New-Object System.Net.WebClient).DownloadFile('https://onelab.info/files/onelab-Windows64.zip', $zip_filepath)
    }
    $onelab_path = Join-Path -Path $store_path  -ChildPath "onelab-Windows64"
    if (Test-Path $onelab_path) {
        Write-Output "onelab.zip already expanded."
    }
    else {
        Expand-Archive ($zip_filepath) -DestinationPath $store_path
        # Remove-Item  $zip_filepath
    }
    if (Test-Path $zip_filepath) {
        Remove-Item $zip_filepath
    }
}
Set-Location ..
    # TODO: Check that executables actually exist before returning them!
Write-Output "$store_path\onelab-Windows64\gmsh.exe" "$store_path\onelab-Windows64\getdp.exe"
