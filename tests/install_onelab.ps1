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

$test_path = Join-Path -Path $current_folder_name -ChildPath ("data\*_onelab")
if (Test-Path -Path $test_path -PathType Container) {
    if (Test-Path $store_path) {
        # TODO: add check here that executables exist!
        Write-Output "Onelab for date $(Get-Date) allready installed"
    }
    else {
        # Newest onelab installation missing
        Remove-Item $test_path -Recurse -Force -Confirm:$false # remove previous installation folder
        New-Item -Path $store_path -ItemType Directory # add new directory
        $zip_filepath = $store_path + "\onelab.zip" # path for onelab.zip
        Write-Output("Zip file path is: $zip_filepath")
        if (Test-Path $zip_filepath) {
            # TODO: Does this check make sense since we just created the folder
            Write-Output("onelab.zip has allready been downloaded.")
        }
        else {
            # FIXME: What to do if there is no internet?
            (New-Object System.Net.WebClient).DownloadFile('https://onelab.info/files/onelab-Windows64.zip', $zip_filepath)
        }
        $onelab_path = Join-Path -Path $store_path  -ChildPath "onelab-Windows64"
        if (Test-Path $onelab_path) {
            Write-Output "onelab.zip allready expanded."
        }
        else {
            Expand-Archive ($zip_filepath) -DestinationPath $store_path
            Remove-Item  $zip_filepath
        }
    }
}
"$store_path\onelab-Windows64\gmsh.exe" > 'GMSH_TEST_PATH'
"$store_path\onelab-Windows64\getdp.exe" > 'GETDP_TEST_PATH'
# [System.Environment]::SetEnvironmentVariable('GMSH_TEST_PATH', "$store_path\onelab-Windows64\gmsh.exe", [System.EnvironmentVariableTarget]::User)
# [System.Environment]::SetEnvironmentVariable('GETDP_TEST_PATH', "$store_path\onelab-Windows64\getdp.exe", [System.EnvironmentVariableTarget]::User)

Set-Location ..
