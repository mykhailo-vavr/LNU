#include <iostream>
#include <vector>
#include <queue>
#include <chrono>
#include <thread>
#include <future>

// Михайло Ваврикович, ПМІ-33, 5 варіант, лабораторна 10

// Метод Гауса — Зейделя

/*
Результати вимірювань:

Зі збільшенням розміру матриці або кількості ітерацій -
зростає наглядність ефективності розпаралелювання методу

Для розміру матриці 500 і кількості ітерацій 200 час послідовного виконання 1923 мс,
паралельного 623 мс

*/

using namespace std;
using namespace std::chrono;
using Row = vector<double>;
using Matrix = vector<Row>;
using Vector = vector<double>;
using Chunk = pair<int, int>;
using ThreadsDistribution = vector<Chunk>;

class Info {
public:
	Matrix matrix;
	Vector vector;
	Vector solutions;
	bool showSolutions;

	Info(Matrix m, Vector v, Vector sols, bool s) {
		this->matrix = m;
		this->vector = v;
		this->solutions = sols;
		this->showSolutions = s;
	}
};

void showMatrix(Matrix matrix) {
	for (int i = 0; i < matrix.size(); i++) {
		for (int j = 0; j < matrix[i].size(); j++) {
			cout << matrix[i][j] << " ";
		}
		cout << endl;
	}
}

void showVector(Vector vector) {
	for (int i = 0; i < vector.size(); i++)
	{
		cout << vector[i] << " ";
	}
	cout << endl;
}

Matrix createMatrixGaussSeidelMethod(int n)
{
	Matrix matrix = Matrix(n);
	srand(time(0));

	for (int i = 0; i < n; i++) {
		matrix[i] = Row(n);

		for (int j = 0; j < n; j++) {
			matrix[i][j] = rand() % 10;
		}
	}

	return matrix;
}

Vector createVectorForGaussSeidelMethod(int n, Matrix matrix)
{
	Vector vector = Vector(n);
	Vector x = Vector(n);
	srand(time(0));

	for (int i = 0; i < n; i++)
	{
		x[i] = rand() % 10;

		for (int j = 0; j < n; j++)
			vector[i] = matrix[i][j] * x[j];
	}

	return vector;
}

bool IsConvergence(Matrix matrix)
{
	for (int i = 0; i < matrix.size(); i++)
	{
		double sum = 0;

		for (int j = 0; j < matrix.size(); j++)
		{
			if (j != i)
				sum += abs(matrix[i][j]);
		}
		if (abs(matrix[i][i]) < sum)
			return false;
	}

	return true;
}

Vector gaussSeidelMethod(Matrix matrix, Vector vector, int countOfIterations, bool showSolutions = false)
{

	cout << "Measurements results in one thread\n";

	auto start = high_resolution_clock::now();

	Vector solutions = Vector(vector.size());

	for (int n = 0; n < countOfIterations; n++)
	{

		for (int i = 0; i < matrix.size(); i++)
		{
			double solution = vector[i];

			for (int j = 0; j < matrix.size(); j++)
			{
				if (i != j)
					solution -= matrix[i][j] * solutions[j];
			}

			solutions[i] = solution / matrix[i][i];
		}

		if (showSolutions) showVector(solutions);
	}

	auto stop = high_resolution_clock::now();
	cout << "\nExecution Time: " << duration_cast<microseconds>(stop - start).count() / 1000 << " ms\n";

	return solutions;
}

void delegat(Info* info)
{
	Matrix matrix = info->matrix;
	Vector vector = info->vector;
	Vector& solutions = info->solutions;
	bool showSolutions = info->showSolutions;

	//cout << this_thread::get_id();

	for (int i = 0; i < matrix.size(); i++)
	{
		double solution = vector[i];

		for (int j = 0; j < matrix.size(); j++)
		{
			if (i != j)
				solution -= matrix[i][j] * solutions[j];
		}

		solutions[i] = solution / matrix[i][i];
	}

	if (showSolutions) showVector(solutions);
}

Vector asyncGaussSeidelMethod(Matrix matrix, Vector vector, int countOfIterations, bool showSolutions = false)
{
	cout << "Measurements results in many threads\n";

	auto start = high_resolution_clock::now();

	Vector solutions = Vector(vector.size());
	queue<future<int>> queue;
	Info info = Info(matrix, vector, solutions, showSolutions);

	for (int n = 0; n < countOfIterations; n++)
	{
		async(std::launch::async, delegat, &info);
	}

	auto stop = high_resolution_clock::now();
	cout << "\nExecution Time: " << duration_cast<microseconds>(stop - start).count() / 1000 << " ms\n";

	return solutions;
}


int main()
{
	/*Row r1{ -0.68, -0.18, 0.02, 0.21 };
	Row r2{ 0.16, -0.88, -0.14, 0.27 };
	Row r3{ 0.37, 0.27, -1.02, -0.24 };
	Row r4{ 0.12, 0.21, -0.18, -0.75 };

	Matrix matrix = Matrix();
	matrix.push_back(r1);
	matrix.push_back(r2);
	matrix.push_back(r3);
	matrix.push_back(r4);

	Vector vector{ -1.83, 0.65, -2.23, 1.13 };*/

	int size = 100;
	int countOfIterations = 200;
	bool showSolutions = false;

	Matrix matrix = createMatrixGaussSeidelMethod(size);;
	Vector vector = createVectorForGaussSeidelMethod(size, matrix);

	gaussSeidelMethod(matrix, vector, countOfIterations, showSolutions);
	asyncGaussSeidelMethod(matrix, vector, countOfIterations, showSolutions);
};