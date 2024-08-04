
#!/bin/bash

# 启动XAMPP的Apache服务器
echo "Starting XAMPP Apache server..."
sudo /Applications/XAMPP/xamppfiles/bin/apachectl start

# 检查Apache服务器是否已启动
if ! pgrep httpd > /dev/null; then
    echo "Failed to start Apache server."
    exit 1
else
    echo "Apache server is running."
fi

# 启动XAMPP的MySQL服务器
echo "Starting XAMPP MySQL server..."
sudo /Applications/XAMPP/xamppfiles/bin/mysql.server start

# 检查MySQL服务器是否已启动
if ! pgrep mysql > /dev/null; then
    echo "Failed to start MySQL server."
    exit 1
else
    echo "MySQL server is running."
fi

# 启动Python应用程序
echo "Starting Python application..."
python app.py &

echo "All services started."