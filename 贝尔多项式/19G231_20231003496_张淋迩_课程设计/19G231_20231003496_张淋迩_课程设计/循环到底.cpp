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
}//дһ�������ֵĽ׳�


int Bell_only(int n, int k, int* X, int* J) {
	double part0 = factorial(n);// �������n�Ľ׳�   
	double part1 = 1.0;//����һ��Ҫ�ø�������������������������С��1�����ֱ��ʡ��1���Խ����ɽϴ�Ӱ�죡����
	for (int i = 0; i < n - k + 1; i++) { part1 *= factorial(J[i]); }//��ĸ��Ľ׳˵ĳ˻�
	double part2 = 1.0;
	for (int i = 0; i < n - k + 1; i++) {
		double t = factorial(i + 1);//i+1�Ľ׳�
		double temp = pow(X[i] / t, J[i]);
		part2 *= temp;
	}//����Ľ׳˵ĳ˻�
	double bell_only = (part0 / part1) * part2;
	return bell_only;
}//��һ���̶�n,k����һ��J��bell����ʽ

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
	cout << "������n: ";
	cin >> n;
	int* X = new int[n];
	cout << "������n��X: " << endl;
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