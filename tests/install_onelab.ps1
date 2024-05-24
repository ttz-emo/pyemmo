# Make sure we are in the pyemmo folder
$current_folder_name = Get-Location | Split-Path -Leaf
if ($current_folder_name -ne "pyemmo") {
    if ($current_folder_name -ne "tests") {
        Write-Error "Wrong folder! Not pyemmo or tests"
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
Write-Output "Store path is $store_path"

if (Test-Path $store_path) {
    # Write-Output "Onelab for date $(Get-Date) allready installed"
    Write-Output "Onelab allready installed!"
}
else {
    New-Item -Path $store_path -ItemType Directory
}

$zip_filepath = $store_path + "\onelab.zip"
Write-Output("Zip file path is: $zip_filepath")
if (Test-Path $zip_filepath) {
    Write-Output("onelab.zip has allready been downloaded.")
}
else {
    (New-Object System.Net.WebClient).DownloadFile('https://onelab.info/files/onelab-Windows64.zip', $zip_filepath)
}
$onelab_path = Join-Path -Path $store_path  -ChildPath "onelab-Windows64"
if (Test-Path $onelab_path){
    Write-Output "onelab.zip allready expanded."
}
else{
    Expand-Archive ($zip_filepath) -DestinationPath $store_path
    Remove-Item  $zip_filepath
}
# $env:GMSH_TEST_PATH = "$store_path\onelab-Windows64\gmsh.exe"
[System.Environment]::SetEnvironmentVariable('GMSH_TEST_PATH', "$store_path\onelab-Windows64\gmsh.exe", 'User')
$env:GETDP_TEST_PATH = "$store_path\onelab-Windows64\getdp.exe"
Set-Location ..
