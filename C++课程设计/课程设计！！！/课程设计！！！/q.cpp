#if 0
#include<iostream>
#include<thread>//�߳̿�
#include<string.h>
#include<windows.h>//windows������ʹ��system���Ͳ���ͼ�꣬������Ҫ����sleep(ms)������������ͣ�ض�ʱ��
#include<conio.h>//conio�ǿ���̨�ַ������������
#include<stdlib.h>//C
#include<fstream>
#include<mmsystem.h>//mmsystem�����ý���йصĴ�����ӿ�
#pragma comment(lib,"winmm.lib")
using namespace std;
#include <stdio.h>

int main() {
    COORD pos;
    pos.X = 20;
    pos.Y = 20;

    // ��ȡ��׼���������������Ҫ�������������ʹ�� STD_ERROR_HANDLE
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), pos);

    // ʹ�� printf_s ��� printf
    printf_s("hello\n");
    return 0;
}
#endif