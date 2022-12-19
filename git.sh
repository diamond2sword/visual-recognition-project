#!/bin/bash

main () {
	include_dependency_strings
	include_dependency_scripts
	reset_cloned_repo
	add_ssh_key_to_ssh_agent
	execute_git_command
}

execute_git_command () {
	bash -c "$STRINGS; $SSH_AUTH_EVAL; $EXEC_GIT_COMMANDS"
}

reset_cloned_repo () {
	rm -r -f "$REPO_PATH"
	mkdir -p "$REPO_PATH"
	git clone "$REPO_URL" "$REPO_PATH"
}

add_ssh_key_to_ssh_agent () {
	bash -c "$STRINGS; $SSH_AUTH_EVAL; $SSH_REGISTER_GIT"
}

include_dependency_scripts () {
	eval "$SSH_AUTH_EVAL"
}

include_dependency_strings () {
	eval "$STRINGS"
}

STRINGS=$(cat << "EOF"
{
	GH_EMAIL="diamond2sword@gmail.com"
	GH_NAME="diamond2sword"
	GH_PASSWORD="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"
	SSH_KEY_PASSPHRASE="for(;C==0;){std::cout<<C++}"
	BRANCH_NAME="main"
	COMMIT_NAME="update project"
	PROJECT_NAME="project"
	REPO_NAME="visual-recognition-project"
	DESKTOP_NAME="Desktop"
	SSH_DIR_NAME=".ssh"
	SSH_KEY_FILE_NAME="id_rsa"
	ROOT_PATH="/root"
	DESKTOP_PATH="$ROOT_PATH/$DESKTOP_NAME"
	REPO_PATH="$DESKTOP_PATH/$REPO_NAME"
	SSH_TRUE_DIR="$ROOT_PATH/$SSH_DIR_NAME"
	SSH_REPO_DIR="$REPO_PATH/$SSH_DIR_NAME"
	REPO_URL="https://github.com/$GH_NAME/$REPO_NAME"
	SSH_REPO_URL="git@github.com:$GH_NAME/$REPO_NAME"
	GIT_COMMAND="git push -u origin $BRANCH_NAME"
}
EOF
)

EXEC_GIT_COMMANDS=$(cat << "EOF"
#!/bin/bash
{
	cd "$REPO_PATH"

	git add .
	git commit -m "$COMMIT_NAME"
	
	git config --global --unset credential.helper
	git config --system --unset credential.helper
	git config --global user.name "$GH_NAME"
	git config --global user.email "$GH_EMAIL"
	git remote set-url origin "$SSH_REPO_URL"
	
	ssh_auth_eval ${GIT_COMMAND[@]}
	
}
EOF
)

SSH_REGISTER_GIT=$(cat << "EOF"
{
	mkdir -p "$SSH_TRUE_DIR"
	cp -r -f "$SSH_REPO_DIR" "$SSH_TRUE_DIR/"
	ssh_auth_eval "ssh-add" "$SSH_TRUE_DIR/$SSH_KEY_FILE_NAME"
	eval "$(ssh-agent -s)"
}
EOF
)

SSH_AUTH_EVAL=$(cat << "EOF"
#!/bin/bash
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
		send "yes\r"
		exp_continue		
	}
	eof
}
EOF2
	}
}
EOF
)

main










