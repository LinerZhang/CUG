#include<iostream>
#include<cmath>
using namespace std;


int factorial(int p) {
	int factorial = 1;
	if (p == 0) {
		return 1;
	}
	else{
		for (int i = 1; i < p + 1; i++) {
			factorial *= i;
		}
		return factorial;
	}
}//写一个纯数字的阶乘


int Bell_only(int n, int k, int* X, int* J) {
	double part0 = factorial(n);// 分子里的n的阶乘   
	double part1 = 1.0;//这里一定要用浮点数！！不能用整数，否则小于1的项会直接省成1，对结果造成较大影响！！！
	for (int i = 0; i < n - k + 1; i++) { part1 *= factorial(J[i]); }//分母里的阶乘的乘积
	double part2 = 1.0;
	for (int i = 0; i < n - k + 1; i++) {
		double t = factorial(i + 1);//i+1的阶乘
		double temp = pow(X[i] / t, J[i]);
		part2 *= temp;
	}//外面的阶乘的乘积
	double bell_only = (part0 / part1) * part2;
	return bell_only;
}//求一个固定n,k，和一组J的bell多项式

int judge(int J[], int n, int num, int k) {
	int F=0;
	for (int i = 0; i < num; i++) {
		F += J[i];
	}
	int G=0;
	for (int i = 0; i < num; i++) {
		G += ((i + 1) * J[i]);
	}
	if (F == k && G == n) {
		return 1;
	}
	else return 0;
}

void circle(int p, int num, int n, int* J, int k, int* X, int& sum) {
	if (p < num) {
		for (int q = 0; q <= n; q++) {
			J[p] = q;
			circle(p + 1, num, n, J, k, X, sum);
		}
	}
	else {
		if (judge(J, n, num, k) == 1) {
			cout << "J:";
			for (int i = 0; i < num; i++) { cout << J[i] << " "; }
			cout << endl;
			cout << "Bell:" << Bell_only(n, k, X,J) << endl;
			cout << endl;
			sum += Bell_only(n, k, X, J);
		}
	}
}

int main() {
	int n;
	cout << "请输入n: ";
	cin >> n;
	int* X = new int[n];
	cout << "请输入n个X: " << endl;
	for (int i = 0; i < n; i++) {
		cin >> X[i];
	}

	int sum = 0;
	int k = 1;
	while (k <= n) {
		int num = n - k + 1;
		int* J = new int[num];
		fill(J, J + num, 0);
		circle(0, num, n, J, k, X, sum);
		delete[] J;
		k++;
	}

	cout << "Bell_all: " << sum << endl;
	delete[] X;
	return 0;
}