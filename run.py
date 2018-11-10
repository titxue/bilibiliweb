from bili.reptile import runthread

#主函数
def main():
    run = runthread()
    run.run(1000) #运行线程数量


#入口
if __name__ == "__main__":
    # lock = lock() #可以注释掉
    main()
