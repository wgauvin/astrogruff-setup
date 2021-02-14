source /usr/share/zsh/share/antigen.zsh

antigen use oh-my-zsh

# bundles
antigen bundle z
antigen bundle git
antigen bundle zsh-users/zsh-completions
antigen bundle zsh-users/zsh-autosuggestions
antigen bundle zsh-users/zsh-syntax-highlighting

antigen theme agnoster

antigen apply

# aliases
alias vi='vim'

# add local path to the front
path=("${HOME}/.local/bin" $path)
