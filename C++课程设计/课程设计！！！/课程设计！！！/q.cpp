#if 0
#include<iostream>
#include<thread>//线程库
#include<string.h>
#include<windows.h>//windows是用来使用system语句和插入图标，这里主要用于sleep(ms)，代表计算机暂停特定时间
#include<conio.h>//conio是控制台字符输入输出操作
#include<stdlib.h>//C
#include<fstream>
#include<mmsystem.h>//mmsystem是与多媒体有关的大多数接口
#pragma comment(lib,"winmm.lib")
using namespace std;
#include <stdio.h>

int main() {
    COORD pos;
    pos.X = 20;
    pos.Y = 20;

    // 获取标准输出句柄，如果你想要输出到错误流，使用 STD_ERROR_HANDLE
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), pos);

    // 使用 printf_s 替代 printf
    printf_s("hello\n");
    return 0;
}
#endif