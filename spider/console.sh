#!/bin/bash                                                                                                                                                    
print_usage()
{
    echo "usage: $0 {start|stop}"
}
case "$1" in
    start)
        python sina_spider.py
        ;;
    stop)
        ps aux|grep "python sina_spider.py" | grep -v grep | awk '{print $2}' | xargs kill -9
        ;;
    *)  
        print_usage
esac

