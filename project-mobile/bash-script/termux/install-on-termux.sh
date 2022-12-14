#!/bin/bash



STRINGS=$(cat << \EOF
####################################################################
DEPENDENCY_PATH="/data/data/com.termux/files/home/dependency-files"
DEPENDENCY_NAMES="PATHS FORCE_INSTALL TOGGLE SCRIPTS STRINGS START_HOME START_ROOT CUSTOM_EXIT CUSTOM_ROOT_START ROOT_COMMANDS HOME_COMMANDS"
ETC_HOSTS_CONFIG="127.0.0.1 localhost"
PACKAGES_FOR_HOME="git wget proot vim termux-api"
PACKAGES_FOR_ROOT="sudo vim python3-pip subversion"
PIP3_PACKAGES_FOR_ROOT="pillow onnxruntime numpy torchvision gdown term-image"
TOGGLE_PREFIX="#TOGGLE_"
PROJECT_GITHUB_LINK="https://github.com/diamond2sword/visual-recognition-project/trunk/project-mobile/project-v1"
PICTURE_NAME="test.jpg"
PROJECT_INSTALL_FILE_NAME="install.py"
PROJECT_MAIN_FILE_NAME="test_onnx.py"
PROJECT_ANY_CLASS_NAME="Any"
PROJECT_NAME="project"
PROJECT_TEST_DATASET_NAME="test-dataset"
RUN_PROJECT_AT_START=true
EOF
)

SCRIPTS=$(cat << \EOF
####################################################################
add_sh_suffix_to () {
    dependency_name=$1
    file_name=${dependency_name}.sh
    echo $file_name
}

include () {
    dependency_name=$1
    file_name=$(add_sh_suffix_to $dependency_name)
    file_path=$DEPENDENCY_PATH/$file_name
    shift
    dependency_args=("$@")
    bash $file_path ${dependency_args[@]}
    source $file_path ${dependency_args[@]}
}

include_dependencies_default () {
    include PATHS
    include FORCE_INSTALL 5
    include TOGGLE
}
EOF
)



PATHS=$(cat << \EOF
####################################################################
TERMUX_PATH="/data/data/com.termux"
HOME_PATH="$TERMUX_PATH/files/home"
CLONE_PATH="$HOME_PATH/ubuntu-in-termux"
UBUNTU_PATH="$CLONE_PATH/ubuntu-fs"
ROOT_PATH="$UBUNTU_PATH/root"
BASHRC_PATH="$ROOT_PATH/.bashrc"
OLD_BASHRC_PATH="$HOME_PATH/.bashrc"
PROJECT_PATH="$ROOT_PATH/$PROJECT_NAME"
TEST_DATASET_PATH="$PROJECT_PATH/$PROJECT_TEST_DATASET_NAME"
CLASS_PATHS=(ls -d $TEST_DATA_SET_PATH/*/)
ANY_CLASS_PATH="$TEST_DATASET_PATH/$PROJECT_ANY_CLASS_NAME"
PROJECT_INSTALL_NAME="install.py"
PROJECT_MAIN_FILE_PATH="$PROJECT_PATH/$PROJECT_MAIN_FILE_NAME"
EOF
)

FORCE_INSTALL=$(cat << \EOF
####################################################################
MAX_FORCE_INSTALL=0

is_number () {
    (($1 + 0)) &> /dev/null && {
        return 0
    }
}

input=$1
is_number $input && {
    MAX_FORCE_INSTALL=$input
}

is_limited () {
    (($MAX_FORCE_INSTALL != 0)) && {
        return 0
    }
}

is_installed () {
    package_manager=$1
    package=$2
    case $package_manager in
        apt|apt-get) dpkg -s $package &> /dev/null && {
            return 0
        };;
        pip3) python3 -c "import pkgutil, sys; sys.exit(0 if pkgutil.find_loader(\"$package\") else 1)" || pip3 show $package &> /dev/null && {
            return 0
        };;
        *) {
             echo "$package_manager is not defined."
        };;
    esac
}

is_installed_all () {
    package_manager=$1
    shift
    packages=("$@")
    for package in ${packages[@]}; do {
        is_installed $package_manager $package && {
            continue
        }
        return 1
    } done
    return 0
}

get_sudo_string () {
    string=""
    is_installed apt sudo && {
        string=sudo
    }
    echo $string
}

update () {
    package_manager=$1
    sudo=$(get_sudo_string)
    case $package_manager in
        apt|apt-get) {
            yes | $sudo $package_manager update
            yes | $sudo $package_manager upgrade
        };;
        pip3) {
            $sudo pip3 install --upgrade --no-input pip
        };;
        *) {
            echo $package_manager is not defined.
        };;
    esac
}

install () {
    package_manager=$1
    package=$2
    sudo=$(get_sudo_string)
    case $package_manager in
        apt | apt-get) {
            yes | $sudo $package_manager install $package
        };;
        pip3) {
            $sudo pip3 install --upgrade --no-input $package
        };;
        *) {
            echo $package_manager is not defined.
        };;
    esac
}

install_all () {
    package_manager=$1
    shift
    packages=("$@")
    for package in ${packages[@]}; do {
        install $package_manager $package
    } done
}

force_install () {
    package_manager=$1
    shift
    packages=("$@")
    max_i=$MAX_FORCE_INSTALL
    i=0
    while :; do {
        is_limited && (($i >= $max_i)) && {
            break
        }
        is_installed_all $package_manager ${packages[@]} && {
            break
        }
        i=$(($i + 1))
        update $package_manager
        install_all $package_manager ${packages[@]}
    } done
}
EOF
)


TOGGLE=$(cat << \EOF
####################################################################
toggle_line_off () {
    toggle_name=$1
    file_path=$2
    toggle_prefix=$TOGGLE_PREFIX
    sed -e "/$toggle_prefix$toggle_name/ s/^#OFF#//" -i $file_path
    sed -e "/$toggle_prefix$toggle_name/ s/^/#OFF#/" -i $file_path
}

toggle_line_on () {
    toggle_name=$1
    file_path=$2
    toggle_prefix=$TOGGLE_PREFIX
    sed -e "/$toggle_prefix$toggle_name/ s/^#OFF#//" -i $file_path
}

set_root_start () {
    mode=$1
    toggle_line_off CUSTOM_ROOT_START $DEPENDENCY_PATH/CUSTOM_ROOT_START.sh
    toggle_line_on CUSTOM_ROOT_START_$mode $DEPENDENCY_PATH/CUSTOM_ROOT_START.sh
}

set_exit () {
    mode=$1
    toggle_line_off CUSTOM_EXIT $DEPENDENCY_PATH/CUSTOM_EXIT.sh
    toggle_line_on CUSTOM_EXIT_$mode $DEPENDENCY_PATH/CUSTOM_EXIT.sh
}

EOF
)


CUSTOM_EXIT=$(cat << \EOF
####################################################################
custom_exit_main () {
    exit_ubuntu #TOGGLE_CUSTOM_EXIT_UBUNTU
#OFF#    exit_termux #TOGGLE_CUSTOM_EXIT_TERMUX
#OFF#    exit_classify #TOGGLE_CUSTOM_EXIT_CLASSIFY
}

exit_classify () {
    set_exit TERMUX
    mkdir -p $ANY_CLASS_PATH
    termux-camera-photo -c 0 $ANY_CLASS_PATH/$PICTURE_NAME
    source $DEPENDENCY_PATH/START_HOME.sh
    return
}

exit_termux () {
    exit
}

exit_ubuntu () {
    set_exit TERMUX
    return
}

EOF
)

CUSTOM_ROOT_START=$(cat << \EOF
####################################################################
custom_root_start_main () {
    start_root_empty #TOGGLE_CUSTOM_ROOT_START_EMPTY
#OFF#    start_root_classify #TOGGLE_CUSTOM_ROOT_START_CLASSIFY
#OFF#    start_root_start_classify #TOGGLE_CUSTOM_ROOT_START_START_CLASSIFY
}

start_root_empty () {
    return
}

start_root_classify () {
    python3 $PROJECT_MAIN_FILE_PATH
    set_root_start EMPTY
}

start_root_start_classify () {
    set_root_start CLASSIFY
    set_exit CLASSIFY
    exit
}
EOF
)


ROOT_COMMANDS=$(cat << \EOF
####################################################################
project-classify () {
    set_exit CLASSIFY
    set_root_start CLASSIFY
    exit
}

project-start () {
    return
}

project-exit () {
    set_exit TERMUX
    set_root_start EMPTY
    exit
}
EOF
)

HOME_COMMANDS=$(cat << \EOF
####################################################################
project-classify () {
    set_exit TERMUX
    set_root_start START_CLASSIFY
    source $DEPENDENCY_PATH/START_HOME.sh
}

project-start () {
    set_exit TERMUX
    set_root_start EMPTY
    source $DEPENDENCY_PATH/START_HOME.sh
}

project-exit () {
    set_exit TERMUX
    set_root_start EMPTY
    exit
}
EOF
)



START_ROOT=$(cat << \EOF
####################################################################
autostart () { 
    include_dependency_strings
    include_dependency_scripts
    include_root_commands
    fix_unresolved_hostname_error
    execute_for_first_boot #TOGGLE_FIRST_BOOT
    execute_custom_root_start
}

execute_custom_root_start () {
    source $DEPENDENCY_PATH/CUSTOM_ROOT_START.sh
    custom_root_start_main
}

execute_for_first_boot () {
    disable_first_boot
    install_dependency_packages
    install_visual_recognition_project
    $RUN_PROJECT_AT_START &> /dev/null & {
        project-classify
    }
}

install_visual_recognition_project () {
    mkdir -p $PROJECT_PATH
    svn export --force $PROJECT_GITHUB_LINK $PROJECT_PATH
    python3 $PROJECT_PATH/$PROJECT_INSTALL_NAME
}

install_dependency_packages () {
    packages=("$PACKAGES_FOR_ROOT")
    pip3_packages=("$PIP3_PACKAGES_FOR_ROOT")
    force_install apt ${packages[@]}
    force_install pip3 ${pip3_packages[@]}
}

disable_first_boot () {
    toggle_line_off FIRST_BOOT $DEPENDENCY_PATH/START_ROOT.sh
    return
}

fix_unresolved_hostname_error () {
    config="$ETC_HOSTS_CONFIG"
    echo "$config" > "/etc/hosts"
}

include_root_commands () {
    source $DEPENDENCY_PATH/ROOT_COMMANDS.sh
}

include_dependency_scripts () {
    source $DEPENDENCY_PATH/SCRIPTS.sh
    include_dependencies_default
}

include_dependency_strings () {
    source $DEPENDENCY_PATH/STRINGS.sh
}

DEPENDENCY_PATH="/data/data/com.termux/files/home/dependency-files"

autostart
EOF
)




START_HOME=$(cat << \EOF
####################################################################
autostart () {
    include_dependency_strings
    include_dependency_scripts
    include_home_commands
    start_ubuntu
    execute_custom_exit
}

execute_custom_exit () {
    source $DEPENDENCY_PATH/CUSTOM_EXIT.sh
    custom_exit_main
}

include_home_commands () {
    source $DEPENDENCY_PATH/HOME_COMMANDS.sh
}

include_dependency_scripts () {
    source $DEPENDENCY_PATH/SCRIPTS.sh
    include_dependencies_default
}

include_dependency_strings () {
    source $DEPENDENCY_PATH/STRINGS.sh
}

start_ubuntu () {
    ubuntu_starter=$CLONE_PATH/startubuntu.sh
    bash $ubuntu_starter
}

DEPENDENCY_PATH="/data/data/com.termux/files/home/dependency-files"

autostart
EOF
)































add_sh_suffix_to () {
    dependency_name=$1
    file_name=${dependency_name}.sh
    echo $file_name
}

create_file_for () {
    commands="$1"
    dependency_name=$2
    file_name=$(add_sh_suffix_to $dependency_name)
    file_path=$DEPENDENCY_PATH/$file_name
    touch $file_path
    echo "$commands" > $file_path
    chmod +x $file_path
}

create_dependency_scripts () {
    mkdir -p $DEPENDENCY_PATH
    dependency_names=("$DEPENDENCY_NAMES")
    for dependency_name in ${dependency_names[@]}; do {
        commands="${!dependency_name}"
        create_file_for "$commands" $dependency_name
    } done
}

include_dependency_strings () {
    eval "$STRINGS"
}

include_dependency_scripts () {
    source $DEPENDENCY_PATH/SCRIPTS.sh
    include_dependencies_default
}

install_dependency_packages () {
    packages=("$PACKAGES_FOR_HOME")
    force_install apt ${packages[@]}
}

install_ubuntu_root_fs () {
    git clone https://github.com/MFDGaming/ubuntu-in-termux.git $CLONE_PATH
    ubuntu_installer=$CLONE_PATH/ubuntu.sh
    chmod +x $ubuntu_installer
    cd $CLONE_PATH
    yes | bash $ubuntu_installer
}

add_autostarter_scripts () {
    echo "source $DEPENDENCY_PATH/START_ROOT.sh" >> $BASHRC_PATH
    echo "source $DEPENDENCY_PATH/START_HOME.sh" >> $OLD_BASHRC_PATH
}

start_ubuntu_fs () {
    source $DEPENDENCY_PATH/START_HOME.sh
}

get_ubuntu_root_fs () {
    include_dependency_strings
    create_dependency_scripts
    include_dependency_scripts
    install_dependency_packages
    install_ubuntu_root_fs
    add_autostarter_scripts
    start_ubuntu_fs
}

get_ubuntu_root_fs
