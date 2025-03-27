#if 0
#include<iostream>
#include<thread>//线程库
#include<string.h>
#include<windows.h>//windows是用来使用system语句和插入图标，这里主要用于sleep(ms)，代表计算机暂停特定时间
#include<conio.h>//conio是控制台字符输入输出操作
#include<stdlib.h>//C
#include<fstream>
#include <stdio.h>
#include<mmsystem.h>//mmsystem是与多媒体有关的大多数接口
#pragma comment(lib,"winmm.lib")
using namespace std;


void gotoxy(int x, int y)//覆盖清屏 ，从指定行列覆盖
{
	COORD pos = { (short)x,(short)y };
	HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
	SetConsoleCursorPosition(hOut, pos);
	return;
}

void prin(string s, int X, int Y)
{
	HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
	CONSOLE_SCREEN_BUFFER_INFO bInfo;
	GetConsoleScreenBufferInfo(hConsole, &bInfo);
	int y = bInfo.dwMaximumWindowSize.Y, x = bInfo.dwMaximumWindowSize.X;
	gotoxy((x - s.size()) / 2 + X, y / 2 + Y);
	cout << s;
}

void print_kuang() {
    short start_x = 20, start_y = 5;
    short page_x = 80, page_y = 20;
    gotoxy(start_x, start_y);      //将鼠标移动到起始点
    for (short y = 0; y < page_y; y++) {
        if (y == 0 || y == page_y - 1) {
            gotoxy(start_x, start_y + y);
            for (short x = 0; x <= page_x; x++) {
                cout << "=";     //若为第一行或最后一行，则打印page_x个=
            }
        }
        else {
            gotoxy(start_x, start_y + y);
            cout << '|';
            gotoxy(start_x + page_x, start_y + y);
            cout << '|';      //每行开头和末尾打印|
        }
    }
}

int main()
{
	/*system("mode con cols=121 lines=26");*/
    print_kuang();
	
	
	return 0;
}
#endif