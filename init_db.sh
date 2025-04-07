#!/bin/bash

FLAG="./file"

echo "正在初始化数据库..."

if [ ! -f $FLAG ]; then
    echo "🔄 首次运行，执行数据库初始化..."
    rm -rf migrations
    python run.py db init
    python run.py db migrate
    python run.py db upgrade
    python run.py generate_data
    touch $FLAG
else
    echo "📦 数据库已初始化，执行升级..."
    python run.py db migrate
    python run.py db upgrade
fi

echo "🚀 启动服务..."
python run.py runserver -h 0.0.0.0