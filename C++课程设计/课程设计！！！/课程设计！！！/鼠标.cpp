#if 0
#include <stdint.h>
#include <Windows.h>
#include <stdio.h>


void GetMouseCurPoint()
{
    POINT mypoint;

    for (int i = 0; i < 100; i++)
    {
        GetCursorPos(&mypoint);//获取鼠标当前所在位置
        printf("% ld, % ld \n", mypoint.x, mypoint.y);
        Sleep(1000);
    }
}

void MouseLeftDown()//鼠标左键按下 
{
    INPUT  Input = { 0 };
    Input.type = INPUT_MOUSE;
    Input.mi.dwFlags = MOUSEEVENTF_LEFTDOWN;
    SendInput(1, &Input, sizeof(INPUT));
}

void MouseLeftUp()//鼠标左键放开 
{
    INPUT  Input = { 0 };
    Input.type = INPUT_MOUSE;
    Input.mi.dwFlags = MOUSEEVENTF_LEFTUP;
    SendInput(1, &Input, sizeof(INPUT));
}

void MouseRightDown()//鼠标右键按下 
{
    INPUT  Input = { 0 };
    Input.type = INPUT_MOUSE;
    Input.mi.dwFlags = MOUSEEVENTF_RIGHTDOWN;
    SendInput(1, &Input, sizeof(INPUT));
}

void MouseRightUp()//鼠标右键放开 
{
    INPUT  Input = { 0 };
    Input.type = INPUT_MOUSE;
    Input.mi.dwFlags = MOUSEEVENTF_RIGHTUP;
    SendInput(1, &Input, sizeof(INPUT));

}

void MouseMove(int x, int y)//鼠标移动到指定位置 
{
    double fScreenWidth = ::GetSystemMetrics(SM_CXSCREEN) - 1;//获取屏幕分辨率宽度 
    double fScreenHeight = ::GetSystemMetrics(SM_CYSCREEN) - 1;//获取屏幕分辨率高度 
    double fx = x * (65535.0f / fScreenWidth);
    double fy = y * (65535.0f / fScreenHeight);

    printf("fScreenWidth %lf , fScreenHeight %lf, fx %lf, fy %lf \n", fScreenWidth, fScreenHeight, fx, fy);

    INPUT  Input = { 0 };
    Input.type = INPUT_MOUSE;
    Input.mi.dwFlags = MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE;
    Input.mi.dx = fx;
    Input.mi.dy = fy;
    SendInput(1, &Input, sizeof(INPUT));
}

int main()
{
    //Sleep(1000);          //延时函数

    //GetMouseCurPoint();   //获取鼠标当前所在位置

    MouseMove(10,20);      //x, y坐标从GetMouseCurPoint()的打印中获取

    //Sleep(10);            //move之后需要延时

    //MouseLeftDown();

    //Sleep(1);

    //MouseLeftUp();

    //Sleep(100);

    return 0;
}
#endif