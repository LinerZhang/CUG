#if 0
#include<iostream>
#include<windows.h>
using namespace std;
#define kd(VK_NONAME) ((GetAsyncKeyState(VK_NONAME) & 0x8000) ? 1:0)

int main()
{
	while (1)
	{
		//�밴��1:
		if (kd(VK_NUMPAD1) || kd('1')) cout << 1 << "\n";
		//������ 
		if (kd(VK_LBUTTON)) cout << "left\n";
		Sleep(50);
	}
	return 0;
}
#endif