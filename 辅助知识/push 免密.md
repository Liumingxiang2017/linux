# vscode，git提交push免密

解决：每次提交都要输入username,password

当前仓库

git config  credential.helper store
全局配置

git config --global credential.helper store
如果以上设置，push 会优先第一个，如果第一个没有，会再去找全局配置
