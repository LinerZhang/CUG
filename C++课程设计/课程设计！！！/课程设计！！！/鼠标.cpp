#if 0
#include <stdint.h>
#include <Windows.h>
#include <stdio.h>


void GetMouseCurPoint()
{
    POINT mypoint;

    for (int i = 0; i < 100; i++)
    {
        GetCursorPos(&mypoint);//��ȡ��굱ǰ����λ��
        printf("% ld, % ld \n", mypoint.x, mypoint.y);
        Sleep(1000);
    }
}

void MouseLeftDown()//���������� 
{
    INPUT  Input = { 0 };
    Input.type = INPUT_MOUSE;
    Input.mi.dwFlags = MOUSEEVENTF_LEFTDOWN;
    SendInput(1, &Input, sizeof(INPUT));
}

void MouseLeftUp()//�������ſ� 
{
    INPUT  Input = { 0 };
    Input.type = INPUT_MOUSE;
    Input.mi.dwFlags = MOUSEEVENTF_LEFTUP;
    SendInput(1, &Input, sizeof(INPUT));
}

void MouseRightDown()//����Ҽ����� 
{
    INPUT  Input = { 0 };
    Input.type = INPUT_MOUSE;
    Input.mi.dwFlags = MOUSEEVENTF_RIGHTDOWN;
    SendInput(1, &Input, sizeof(INPUT));
}

void MouseRightUp()//����Ҽ��ſ� 
{
    INPUT  Input = { 0 };
    Input.type = INPUT_MOUSE;
    Input.mi.dwFlags = MOUSEEVENTF_RIGHTUP;
    SendInput(1, &Input, sizeof(INPUT));

}

void MouseMove(int x, int y)//����ƶ���ָ��λ�� 
{
    double fScreenWidth = ::GetSystemMetrics(SM_CXSCREEN) - 1;//��ȡ��Ļ�ֱ��ʿ�� 
    double fScreenHeight = ::GetSystemMetrics(SM_CYSCREEN) - 1;//��ȡ��Ļ�ֱ��ʸ߶� 
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
    //Sleep(1000);          //��ʱ����

    //GetMouseCurPoint();   //��ȡ��굱ǰ����λ��

    MouseMove(10,20);      //x, y�����GetMouseCurPoint()�Ĵ�ӡ�л�ȡ

    //Sleep(10);            //move֮����Ҫ��ʱ

    //MouseLeftDown();

    //Sleep(1);

    //MouseLeftUp();

    //Sleep(100);

    return 0;
}
#endif