#if 0
#include<iostream>
#include<thread>//�߳̿�
#include<string.h>
#include<windows.h>//windows������ʹ��system���Ͳ���ͼ�꣬������Ҫ����sleep(ms)������������ͣ�ض�ʱ��
#include<conio.h>//conio�ǿ���̨�ַ������������
#include<stdlib.h>//C
#include<fstream>
#include <stdio.h>
#include<mmsystem.h>//mmsystem�����ý���йصĴ�����ӿ�
#pragma comment(lib,"winmm.lib")
using namespace std;


void gotoxy(int x, int y)//�������� ����ָ�����и���
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
    gotoxy(start_x, start_y);      //������ƶ�����ʼ��
    for (short y = 0; y < page_y; y++) {
        if (y == 0 || y == page_y - 1) {
            gotoxy(start_x, start_y + y);
            for (short x = 0; x <= page_x; x++) {
                cout << "=";     //��Ϊ��һ�л����һ�У����ӡpage_x��=
            }
        }
        else {
            gotoxy(start_x, start_y + y);
            cout << '|';
            gotoxy(start_x + page_x, start_y + y);
            cout << '|';      //ÿ�п�ͷ��ĩβ��ӡ|
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