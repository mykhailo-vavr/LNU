#include <iostream>
#include <vector>
#include <chrono>
#include <thread>

// Михайло Ваврикович, ПМІ-33, 5 варіант, лабораторна 9

// З матриці випадкових чисел a(i,j) cтворити матрицю

/*
Результати вимірювань:

Розмір матриці = 1000x1000
к-сть потоків | паралельно (мс) | послідовно(мс)
4             | 212				| 304
8             | 170				| 235
16            | 163				| 234
32            | 188				| 233

Розмір матриці = 5000x5000
к-сть потоків | паралельно (мс) | послідовно(мс)
8             | 3872			| 5601
16            | 4815			| 5706
32            | 5473			| 5662
64            | 6179			| 5617

При надмірній кількості потоків швидкість виконання падає (результат не буде оптимальним)
При збільшенні розмірів матриці, стає наявнішим перевага у швидкості виконання алгоритму у багатьох потоках
*/

using namespace std;
using namespace std::chrono;
using Matrix = vector<vector<int>>;
using Row = vector<int>;
using Chunk = pair<int, int>;
using ThreadsDistribution = vector<Chunk>;

Matrix createMatrix(int n,  int m, bool isEmpty = false) {
	Matrix matrix = Matrix(n);
	
	for (int i = 0; i < n; i++) {
		matrix[i] = Row(m);

		if(!isEmpty) {
			for (int j = 0; j < m; j++) {
				matrix[i][j] = rand() % 10;
			}
		}
	}

	return matrix;
}

void showMatrix(Matrix matrix) {
	for (int i = 0; i < matrix.size(); i++) {
		for (int j = 0; j < matrix[i].size(); j++) {
			cout << matrix[i][j] << " ";
		}
		cout << endl;
	}
}

ThreadsDistribution getThreadsDistribution(int n, int countOfThreads)
{
	ThreadsDistribution threadsDistribution = ThreadsDistribution(countOfThreads);
	int perStep = n / countOfThreads;
	for (int i = 0; i < threadsDistribution.size(); i++)
	{
		threadsDistribution[i] = make_pair(i * perStep, (i + 1) * perStep);
	}
	threadsDistribution[threadsDistribution.size() - 1] = make_pair((threadsDistribution.size() - 1) * perStep, n);

	return threadsDistribution;
}

Matrix createModifiedMatrixSync(Matrix matrix) {
	Matrix modifiedMatrix = Matrix(matrix.size());

	for (int i = 0; i < matrix.size(); i++) {
		modifiedMatrix[i] = Row(matrix[i].size());

		for (int j = 0; j < matrix[i].size(); j++) {
			if (i == matrix.size() - 1) {
				modifiedMatrix[i][j] = matrix[i][j] + matrix[1][j];
			}
			else if (i < matrix.size()) {
				modifiedMatrix[i][j] = matrix[i][j] + matrix[i + 1][j];
			}
		}
	}

	return modifiedMatrix;
}

Matrix createModifiedMatrixAsync(Matrix matrix, int countOfThreads) {
	Matrix modifiedMatrix = Matrix(matrix.size());

	ThreadsDistribution threadsDistribution = getThreadsDistribution(matrix.size(), countOfThreads);
	int completedThreads = 0;
	vector<thread> threads = vector<thread>();

	for (int threadNumber = 0; threadNumber < countOfThreads; ++threadNumber) {
		Chunk chunk = threadsDistribution[threadNumber];

		thread th([&modifiedMatrix, &completedThreads, matrix, chunk]() mutable {
			for (int i = chunk.first; i < chunk.second; i++) {
				modifiedMatrix[i] = Row(matrix[i].size());

				for (int j = 0; j < matrix[i].size(); j++) {
					if (i == matrix.size() - 1) {
						modifiedMatrix[i][j] = matrix[i][j] + matrix[1][j];
					}
					else if (i < matrix.size()) {
						modifiedMatrix[i][j] = matrix[i][j] + matrix[i + 1][j];
					}
				}
			}

			completedThreads++;
		});

		// cout << th.get_id() << endl;

		th.detach();
	}


	while (completedThreads != countOfThreads) {
		continue;
	}

	return modifiedMatrix;
}

void createModifiedMatrix(Matrix matrix, bool showMatrices = false, bool async = false, int countOfThreads = 1)
{
	if (showMatrices) {
		showMatrix(matrix);
		cout << endl;
	};

	Matrix modifiedMatrix = async ? createModifiedMatrixAsync(matrix, countOfThreads) : createModifiedMatrixSync(matrix);
	if (showMatrices) showMatrix(modifiedMatrix);

}

void createModifiedMatrixMeasurements(Matrix matrix, bool showMatrices = false, bool async = false, int countOfThreads = 1)
{
	string type = async ? "many threads" : "one thread";

	cout << "Measurements results in " << type << "\n\n";

	auto start = high_resolution_clock::now();
	createModifiedMatrix(matrix, showMatrices, async, countOfThreads);
	auto stop = high_resolution_clock::now();

	cout << "\nExecution Time: " << duration_cast<microseconds>(stop - start).count() / 1000 << " ms\n";
}

int main()
{
	int n = 1000, m = 5000;
	bool showMatrices = false;
	bool async = true;
	int countOfThreads = 12;

	Matrix matrix = createMatrix(n, m);
	
	createModifiedMatrixMeasurements(matrix, showMatrices);

	cout << "\n====================\n\n";

	createModifiedMatrixMeasurements(matrix, showMatrices, async, countOfThreads);
}