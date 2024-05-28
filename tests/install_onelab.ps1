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
"$store_path\onelab-Windows64\gmsh.exe" > 'GMSH_TEST_PATH'
"$store_path\onelab-Windows64\getdp.exe" > 'GETDP_TEST_PATH'
# [System.Environment]::SetEnvironmentVariable('GMSH_TEST_PATH', "$store_path\onelab-Windows64\gmsh.exe", [System.EnvironmentVariableTarget]::User)
# [System.Environment]::SetEnvironmentVariable('GETDP_TEST_PATH', "$store_path\onelab-Windows64\getdp.exe", [System.EnvironmentVariableTarget]::User)

Set-Location ..
