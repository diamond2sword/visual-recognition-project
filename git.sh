#!/bin/bash

main () {
	add_ssh_key_to_ssh_agent
	execute_git_command
}

STRINGS=$(cat <<- "EOF"
	REPO_NAME=visual-recognition-project
	GH_EMAIL="diamond2sword@gmail.com"
	GH_NAME="diamond2sword"
	GH_PASSWORD="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"
	SSH_KEY_PASSPHRASE="for(;C==0;){std::cout<<C++}"
	DEFAULT_GIT_COMMAND_NAME="GIT_RESET"
	THIS_FILE_NAME="git.sh"
	BRANCH_NAME="main"
	COMMIT_NAME="update project"
	PROJECT_NAME="project"
	SSH_DIR_NAME=".ssh"
	SSH_KEY_FILE_NAME="id_rsa"
	ROOT_PATH="/root"
	REPO_PATH="$ROOT_PATH/$REPO_NAME"
	THIS_FILE_PATH="$ROOT_PATH/$THIS_FILE_NAME"
	SSH_TRUE_DIR="$REPO_PATH/$SSH_DIR_NAME"
	SSH_REPO_DIR="$REPO_PATH/$SSH_DIR_NAME"
	REPO_URL="https://github.com/$GH_NAME/$REPO_NAME"
	SSH_REPO_URL="git@github.com:$GH_NAME/$REPO_NAME"
EOF
)

execute_git_command () {
	bash -c "{
		$STRINGS
		$SSH_AUTH_EVAL
		$ALL_GIT_COMMANDS
		$INPUT
		$EXEC_GIT_COMMAND
	}"
}

add_ssh_key_to_ssh_agent () {
	bash -c "{
		$STRINGS
		$SSH_AUTH_EVAL
		$SSH_REGISTER_GIT
	}"
}

EXEC_GIT_COMMAND=$(cat <<- "EOF"
	main () {
		reset_git_credentials
		exec_git_command
	}

	exec_git_command () {
		git_command="${INPUT[0]}"
		eval "${!git_command}"
	}

	reset_git_credentials () {
		eval "$GIT_UNSET"
	}
	
	main
EOF
)

ALL_GIT_COMMANDS=$(cat <<- "EOF"
	GIT_UNSET=$(cat << "EOF2"
		cd "$REPO_PATH"
		git config --global --unset credential.helper
		git config --system --unset credential.helper
		git config --global user.name "$GH_NAME"
		git config --global user.email "$GH_EMAIL"
	EOF2
	)

	GIT_PUSH=$(cat << "EOF2"
		cd "$REPO_PATH"
		git add .
		git commit -m "$COMMIT_NAME"
		git remote set-url origin "$SSH_REPO_URL"
		ssh_auth_eval "git push -u origin $BRANCH_NAME"
	EOF2
	)

	GIT_RESET=$(cat << "EOF2"
		rm -r -f "$REPO_PATH"
		mkdir -p "$REPO_PATH"
		cd "$REPO_PATH"
		git clone "$REPO_URL" "$REPO_PATH"
	EOF2
	)

	GIT_CONFIG=$(cat << "EOF2"
		KEY_NAME=${INPUT[1]}
		NEW_VALUE=${INPUT[2]}
		sed -i '{
			/^STRINGS=/{
				:start
				/\nEOF/!{
					/'"$KEY_NAME"'=/{
						b found
					}
					n
					b start
				}
				b exit
				:found
				/^STRINGS=/!{
					s/'"$KEY_NAME"'.*$/'"$KEY_NAME"'='"$NEW_VALUE"'/
				}
			}
			:exit
		}' $THIS_FILE_PATH
	EOF2
	)
EOF
)

SSH_REGISTER_GIT=$(cat << "EOF"
	mkdir -p "$SSH_TRUE_DIR"
	cp -f "$SSH_REPO_DIR/*" "$SSH_TRUE_DIR"
	chmod 600 "$SSH_TRUE_DIR/$SSH_KEY_FILE_NAME"
	eval "$(ssh-agent -s)"
	ssh_auth_eval ssh-add $SSH_TRUE_DIR/$SSH_KEY_FILE_NAME
EOF
)


SSH_AUTH_EVAL=$(cat <<- "EOF"
	ssh_auth_eval () {
		command=("$@")
		ssh_key_passphrase="$SSH_KEY_PASSPHRASE"
		expect << EOF2
			spawn ${command[@]}
			expect {
				-re {Enter passphrase for} {
					send "$ssh_key_passphrase\r"
					exp_continue
				}
				-re {Are you sure you want to continue connecting} {
					send "yes\r"
					exp_continue
				}
				eof
			}
		EOF2
	}
EOF
)

INPUT=$(cat << EOF
	INPUT=($@)
EOF
)

main
