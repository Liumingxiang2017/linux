vscode，git提交push，需要每次都输入账号密码username,password
配置name，Email

git config --global user.name "huachuan"
git config --global user.email hc.5@qq.com
解决：每次提交都要输入username,password

当前仓库

git config  credential.helper store
全局配置

git config --global credential.helper store
如果以上设置，push 会优先第一个，如果第一个没有，会再去找全局配置
