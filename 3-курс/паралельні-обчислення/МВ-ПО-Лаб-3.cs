using System;
using System.Threading;
using MathNet.Numerics.LinearAlgebra;
using System.Diagnostics;

// Михайло Ваврикович, ПМІ-33, 5 варіант, лабораторна 3

// Метод квадратного кореня

/*
Результати вимірювань:

Розмір матриці = 1000
к-сть потоків | паралельно (мс) | послідовно(мс)
4             | 3323 | 4574
8             | 3136 | 4694
16            | 2750 | 4437
32            | 2671 | 4520

Розмір матриці = 1500
к-сть потоків | паралельно (мс) | послідовно(мс)
8             | 11555 | 15688
16            | 10493 | 14967
32            | 9863 | 15007
64            | 9363 | 15009

Розмір матриці = 2000
к-сть потоків | паралельно (мс) | послідовно(мс)
16            | 25559 | 38246
32            | 24880 | 37200
64            | 23309 | 38428
128           | 23100 | 37012

Для оптимального часу виконання при багапоточному обчисленні
кількість потоків потрібно підбирати в залежності від розміру матриці.
*/

class Program
{
    static Matrix<double> CreateMatrixForSquareRootMethod(int n, double min = -100, double max = 100)
    {
        Matrix<double> matrix = Matrix<double>.Build.Dense(n, n);
        Random random = new Random();

        for (int i = 0; i < n; ++i)
        {
            for (int j = i; j < n; j++)
            {
                if (i == j)
                {
                    matrix[i, j] = Math.Round((max - min) * random.NextDouble() + min, 2) + 100 * max;
                    continue;
                }
            
                matrix[i, j] = matrix[j, i] = Math.Round((max - min) * random.NextDouble() + min, 2);
            }
        }

        return matrix;
    }

    static Vector<double> CreateVectorForSquareRootMethod(int n, double min = -100, double max = 100)
    {
        Vector<double> vector = Vector<double>.Build.Dense(n, n);
        Random random = new Random();

        for (int i = 0; i < n; ++i)
            vector[i] = Math.Round((max - min) * random.NextDouble() + min, 2);

        return vector;
    }

    static (int, int)[] GetThreadsDistribution(int n, int countOfThreads)
    {
        (int, int)[] threadsDistribution = new (int start, int end)[countOfThreads];
        int perStep = n / countOfThreads;

        for (int i = 0; i < threadsDistribution.Length - 1; i++)
        {
            threadsDistribution[i] = (i * perStep, (i + 1) * perStep);
        }
        threadsDistribution[threadsDistribution.Length - 1] = ((threadsDistribution.Length - 1) * perStep, n);

        return threadsDistribution;
    }

    static bool IsValidMatrix(Matrix<double> matrix)
    {
        return matrix.Determinant() > 0 && matrix.Equals(matrix.Transpose());
    }

    static Matrix<double> GetU(Matrix<double> matrix)
    {
        Matrix<double> U = Matrix<double>.Build.Dense(matrix.RowCount, matrix.ColumnCount);
            
        for (int i = 0; i < U.RowCount; i++)
        {
            for (int j = 0; j < U.RowCount; j++)
            {
                if (j < i)
                {
                    U[i, i] = 0;
                }
                else if (i == j)
                {
                    double sum = 0;

                    for (int k = 0; k < i; k++)
                        sum += Math.Pow(U[k, i], 2);                           

                    if(matrix[i, i] - sum < 0)
                    {
                        throw new Exception($"\nSquare root is negative. Index of line: {i}\n");
                    }

                    U[i, j] = Math.Sqrt(matrix[i, i] - sum);
                } 
                else
                {
                    double sum = 0;

                    for (int k = 0; k < i; k++)
                        sum += U[k, i] * U[k, j];

                    U[i, j] = (matrix[i, j] - sum) / U[i, i];
                }
            }

        }

        return U;
    }

    static Matrix<double> GetAsyncU(Matrix<double> matrix, int countOfThreads)
    {
        (int, int)[] threadsDistribution = GetThreadsDistribution(matrix.RowCount, countOfThreads);

        int completedThreads = 0;

        Matrix<double> U = Matrix<double>.Build.Dense(matrix.RowCount, matrix.ColumnCount);

        for (int threadNumber = 0; threadNumber < countOfThreads; ++threadNumber)
        {
            (int start, int end) = threadsDistribution[threadNumber];
            Thread thread = new Thread(() =>
                {

                    for (int i = start; i < end; i++)
                    {
                        for (int j = 0; j < U.RowCount; j++)
                        {
                            if (j < i)
                            {
                                U[i, i] = 0;
                            }
                            else if (i == j)
                            {
                                double sum = 0;

                                for (int k = 0; k < i; k++)
                                    sum += Math.Pow(U[k, i], 2);

                                if (matrix[i, i] - sum < 0)
                                {
                                    throw new Exception($"\nSquare root is negative. Index of line: {i}\n");
                                }

                                U[i, j] = Math.Sqrt(matrix[i, i] - sum);
                            }
                            else
                            {
                                double sum = 0;

                                for (int k = 0; k < i; k++)
                                    sum += U[k, i] * U[k, j];

                                U[i, j] = (matrix[i, j] - sum) / U[i, i];
                            }
                        }
                    }
                    
                    completedThreads++;
                }
            );

            thread.Start();
        }

        while (completedThreads != countOfThreads) { }

        return U;
        }

    static Vector<double> GetAuxiliaryUnknowns(Matrix<double> U, Vector<double> vector)
    {
        Vector<double> auxiliaryUnknows = Vector<double>.Build.Dense(U.RowCount);

        for (int i = 0; i < U.RowCount; i++)
        {
            double sum = 0;

            for (int k = 0; k < i; k++)
                sum += U[k, i] * auxiliaryUnknows[k];

            auxiliaryUnknows[i] = (vector[i] - sum) / U[i, i];
        }

        return auxiliaryUnknows;
    }

    static Vector<double> GetSolutions(Matrix<double> U, Vector<double> auxiliaryUnknows)
    {
        Vector<double> solutions = Vector<double>.Build.Dense(U.RowCount);

        for (int i = U.RowCount - 1; i >= 0; i--)
        {
            double sum = 0;

            for (int k = i + 1; k < U.RowCount; k++)
            {
                sum += U[i, k] * solutions[k];
            }

            solutions[i] = (auxiliaryUnknows[i] - sum) / U[i, i];
        }

        return solutions;
    }

    static Vector<double> SquareRoot(Matrix<double> matrix, Vector<double> vector, bool showMatrices = false, bool async = false, int countOfThreads = 1)
    {
        if (!IsValidMatrix(matrix)) {
            Console.WriteLine("Invalid matrix");
            return Vector<double>.Build.Dense(0);
        }

        Matrix<double> U = async ? GetAsyncU(matrix, countOfThreads) : GetU(matrix);
        if(showMatrices) Console.WriteLine("== U: ==\n{0}", U);

        Vector<double> auxiliaryUnknows = GetAuxiliaryUnknowns(U, vector);
        if (showMatrices) Console.WriteLine("== Auxiliary unknowns: ==\n{0}", auxiliaryUnknows);

        Vector<double> solutions = GetSolutions(U, auxiliaryUnknows);
        if (showMatrices) Console.WriteLine("== Solutions: ==\n{0}", solutions);

        return solutions;
    }

    static void SquareRootWithMeasurements(Matrix<double> matrix, Vector<double> vector, bool showMatrices = false, bool async = false, int countOfThreads = 1)
    {
        string type = async ? "many threads" : "one thread";
        Stopwatch stopwatch = new Stopwatch();

        Console.WriteLine($"Measurements results in {type}\n");
        stopwatch.Start();

        SquareRoot(matrix, vector, showMatrices, async, countOfThreads);

        stopwatch.Stop();
        Console.WriteLine($"Execution Time: {stopwatch.ElapsedMilliseconds} ms");
    }

    static void Main()
    {
        //Data to check the correct execution of the method

        //Matrix<double> matrix = Matrix<double>.Build.DenseOfArray(
        //    new[,] {
        //        { 4, 2, 2, 1 },
        //        { 2, 5, 1, 2 },
        //        { 2, 1, 5, 1 },
        //        { 1, 2, 1, 4.875 }
        //    }
        //);

        //Vector<double> vector = Vector<double>.Build.DenseOfArray(new[] { 9, 10, 9, 8.875 });

        int size = 200;
        bool showMatrices = false;
        bool async = true;
        int countOfThreads = 10;

        Matrix<double> matrix = CreateMatrixForSquareRootMethod(size);
        Vector<double> vector = CreateVectorForSquareRootMethod(size);

        SquareRootWithMeasurements(matrix, vector, showMatrices);

        Console.WriteLine("\n====================\n");

        SquareRootWithMeasurements(matrix, vector, showMatrices, async, countOfThreads);
    }
}

