set cindent
" Tab键的宽度
set tabstop=4

" 统一缩进为4
set softtabstop=4
set shiftwidth=4
" 显示行号
set number
" 设置在状态行显示的信息
"set foldcolumn=0
"set foldmethod=indent 
set expandtab
%retab!
"set foldlevel=3 
"set foldenable          
" 开始折叠
" 不要使用vi的键盘模式，而是vim自己的
set nocompatible
" 语法高亮
set syntax=on
" 去掉输入错误的提示声音
set noeb
" 在处理未保存或只读文件的时候，弹出确认
set confirm
" 自动缩进
set autoindent
"set cindent
" 历史记录数
set history=1000
"禁止生成临时文件
set nobackup
set noswapfile
"搜索忽略大小写
set ignorecase
" 总是显示状态行
set laststatus=2
set paste