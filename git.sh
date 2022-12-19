#!/bin/bash

main () {
        include_dependency_strings
        include_dependency_scripts
        add_ssh_key_to_ssh_agent
        set_input_to_default_if_invalid
        execute_git_command
}

STRINGS=$(cat << "EOF"
{
        REPO_NAME="visual-recognition-project"
        GH_EMAIL="diamond2sword@gmail.com"
        GH_NAME="diamond2sword"
        GH_PASSWORD="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"
        SSH_KEY_PASSPHRASE="for(;C==0;){std::cout<<C++}"
        DEFAULT_GIT_COMMAND_NAME="GIT_RESET"
        BRANCH_NAME="main"
        COMMIT_NAME="update project"
        PROJECT_NAME="project"
        SSH_DIR_NAME=".ssh"
        SSH_KEY_FILE_NAME="id_rsa"
        ROOT_PATH="/root"
        REPO_PATH="$ROOT_PATH/$REPO_NAME"
        SSH_TRUE_DIR="$ROOT_PATH/$SSH_DIR_NAME"
        SSH_REPO_DIR="$REPO_PATH/$SSH_DIR_NAME"
        REPO_URL="https://github.com/$GH_NAME/$REPO_NAME"
        SSH_REPO_URL="git@github.com:$GH_NAME/$REPO_NAME"
}
EOF
)

execute_git_command () {
        bash << EOF
        {
                $STRINGS
                $SSH_AUTH_EVAL
                $INPUT
                $ALL_GIT_COMMANDS
                $EXEC_GIT_COMMAND
        }
EOF
}

set_input_to_default_if_invalid () {
        ! is_input_valid && {
                INPUT=$(cat << EOF
                {
                        GIT_COMMAND_NAME="$DEFAULT_GIT_COMMAND_NAME"
                }
EOF
                )
        }
}

add_ssh_key_to_ssh_agent () {
        bash << EOF
        {
                $STRINGS
                $SSH_AUTH_EVAL
                $SSH_REGISTER_GIT
        }
EOF
}

include_dependency_scripts () {
        eval "$SSH_AUTH_EVAL"
}

include_dependency_strings () {
        eval "$STRINGS"
}

is_input_valid () {
        return $(bash << EOF
        {
                $INPUT
                $ALL_GIT_COMMANDS
                $IS_INPUT_VALID
        }
EOF
        )
}


EXEC_GIT_COMMAND=$(cat << "EOF"
{
        main () {
                change_dir_to_repo
                reset_git_credentials
                exec_git_command
        }

        exec_git_command () {
                eval "${!GIT_COMMAND_NAME}"
        }

        reset_git_credentials () {
                eval "$GIT_UNSET"
        }

        change_dir_to_repo () {
                cd "$REPO_PATH"; pwd
        }

        main
}
EOF
)

IS_INPUT_VALID=$(cat << "EOF"
{
        main () {
                is_input_valid
        }

        is_input_valid () {
                is_input_empty && return 1
                is_input_mispelled && return 1
                exit 0
        }

        is_input_empty () {
                ! [ $GIT_COMMAND_NAME ] && {
                        return 0
                }
        }

        is_input_mispelled () {
                ! [ "${!GIT_COMMAND_NAME}" ] && {
                        return 0
                }
        }

        main
}
EOF
)

ALL_GIT_COMMANDS=$(cat << "EOF"
{
        GIT_UNSET=$(cat << "EOF2"
        {
                git config --global --unset credential.helper
                git config --system --unset credential.helper
                git config --global user.name "$GH_NAME"
                git config --global user.email "$GH_EMAIL"
        }
EOF2
        )

        GIT_PUSH=$(cat << "EOF2"
        {
                git add .
                git commit -m "$COMMIT_NAME"
                git remote set-url origin "$SSH_REPO_URL"
                ssh_auth_eval "git push -u origin $BRANCH_NAME"
        }
EOF2
        )

        GIT_RESET=$(cat << "EOF2"
        {
                rm -r -f "$REPO_PATH"
                mkdir -p "$REPO_PATH"
                git clone "$REPO_URL" "$REPO_PATH"
        }
EOF2
        )
}
EOF
)

SSH_REGISTER_GIT=$(cat << "EOF"
{
        mkdir -p "$SSH_TRUE_DIR"
        cp -r -f "$SSH_REPO_DIR" "$ROOT_PATH"
        eval "$(ssh-agent -s)"
        ssh_auth_eval "ssh-add" "$SSH_TRUE_DIR/$SSH_KEY_FILE_NAME"
}
EOF
)

SSH_AUTH_EVAL=$(cat << "EOF"
{
        ssh_auth_eval () {
                commands=("$@")
                ssh_key_passphrase="$SSH_KEY_PASSPHRASE"
                expect << EOF2
spawn ${commands[@]}
expect {
        -re {Enter passphrase for} {
                send "$ssh_key_passphrase\r"
                exp_continue
        }
        -re {Are you sure you want to continue connecting} {
                send "yes\r"                                                          exp_continue
        }                                                                     eof
}
EOF2
        }
}
EOF
)

INPUT=$(cat << EOF
{
        GIT_COMMAND_NAME=$1
}
EOF
)

main
