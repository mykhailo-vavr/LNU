using System;
using System.Diagnostics;
using System.Threading;
using MathNet.Numerics.LinearAlgebra;

// Михайло Ваврикович, ПМІ-33, 5 варіант, лабораторна 4

// Метод Гауса — Зейделя

/*
Результати вимірювань:

Зі збільшенням розміру матриці або кількості ітерацій -
зростає наглядність ефективності розпаралелювання методу

Для розміру матриці 500 і кількості ітерацій 200 час послідовного виконання 1923 мс,
паралельного 623 мс

Для розміру матриці  < 1000 використовується ~4 потоки, при розмір > 1000 ~8
Також на к-сть потоків впливає кількість ітерацій

*/

class Program
{
    struct GaussSeidelMethodData
    {
        public Matrix<double> matrix;
        public Vector<double> vector;

        public GaussSeidelMethodData(Matrix<double> m, Vector<double> v)
        {
            matrix = m;
            vector = v;
        }
    }

    static Matrix<double> CreateMatrixGaussSeidelMethod(int n)
    {
        Matrix<double> matrix = Matrix<double>.Build.Dense(n, n);
        Random random = new Random();

        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < n; j++)
            {
                matrix[i, j] = random.Next(1, 10);
            }
        }

        return matrix;
    }

    static Vector<double> CreateVectorForGaussSeidelMethod(int n, Matrix<double> matrix)
    {
        Vector<double> vector = Vector<double>.Build.Dense(n, n);
        Random random = new Random();
        double[] x = new double[n];

        for (int i = 0; i < n; i++)
        {
            x[i] = random.Next(1, 10);

            for (int j = 0; j < n; j++)
                vector[i] = matrix[i, j] * x[j];
        }

        return vector;
    }

    static bool IsConvergence(Matrix<double> matrix)
    {
        for (int i = 0; i < matrix.RowCount; i++)
        {
            double sum = 0;

            for (int j = 0; j < matrix.RowCount; j++)
            {
                if (j != i)
                    sum += Math.Abs(matrix[i, j]);
            }
            if (Math.Abs(matrix[i, i]) < sum)
                return false;
        }
        return true;
    }

    static Vector<double> GaussSeidelMethod(Matrix<double> matrix, Vector<double> vector, int countOfIterations, bool showSolutions = false)
    {
        Stopwatch stopwatch = new Stopwatch();

        Console.WriteLine($"Measurements results in one thread\n");
        stopwatch.Start();

        Vector<double> solutions = Vector<double>.Build.Dense(vector.Count);

        for (int n = 0; n < countOfIterations; n++)
        {

            for (int i = 0; i < matrix.RowCount; i++)
            {
                double solution = vector[i];

                for (int j = 0; j < matrix.RowCount; j++)
                {
                    if (i != j)
                        solution -= matrix[i, j] * solutions[j];
                }

                solutions[i] = solution / matrix[i, i];
            }

            if (showSolutions) Console.WriteLine(string.Join(",", solutions));
        }

        stopwatch.Stop();
        Console.WriteLine($"Execution Time: {stopwatch.ElapsedMilliseconds} ms");

        return solutions;
    }

    static Vector<double> AsyncGaussSeidelMethod(Matrix<double> matrix, Vector<double> vector, int countOfIterations, bool showSolutions = false)
    {
        Stopwatch stopwatch = new Stopwatch();

        Console.WriteLine($"Measurements results in many threads\n");
        stopwatch.Start();

        ThreadPool.SetMinThreads(2, 2);
        ThreadPool.SetMaxThreads(100, 100);
        
        Vector<double> solutions = Vector<double>.Build.Dense(vector.Count);

        for (int n = 0; n < countOfIterations; n++)
        {
            ThreadPool.QueueUserWorkItem(
                (object methodData) =>
                {
                    GaussSeidelMethodData data = (GaussSeidelMethodData)methodData;
                    
                    for (int i = 0; i < data.matrix.RowCount; i++)
                    {
                        double solution = data.vector[i];

                        for (int j = 0; j < data.matrix.RowCount; j++)
                        {
                            if (i != j)
                                solution -= data.matrix[i, j] * solutions[j];
                        }

                        solutions[i] = solution / data.matrix[i, i];
                    }

                    Console.WriteLine(Thread.CurrentThread.ManagedThreadId);
                }, new GaussSeidelMethodData(matrix, vector));

            Thread.Sleep(1);
            if (showSolutions) Console.WriteLine(string.Join(",", solutions));
        }

        stopwatch.Stop();
        Console.WriteLine($"Execution Time: {stopwatch.ElapsedMilliseconds} ms");

        return solutions;
    }

    static void Main()
    {
        //Data to check the correct execution of the method
        //Matrix<double> matrix = Matrix<double>.Build.DenseOfArray(
        //    new[,] {
        //        {-0.68, -0.18, 0.02, 0.21 },
        //        { 0.16, -0.88, -0.14, 0.27},
        //        { 0.37, 0.27, -1.02, -0.24},
        //        { 0.12, 0.21, -0.18, -0.75}
        //    }
        //);

        //Vector<double> vector = Vector<double>.Build.DenseOfArray(new[] { -1.83, 0.65, -2.23, 1.13 });

        int size = 1200;
        int countOfIterations = 10;
        bool showSolutions = false;

        Matrix<double> matrix = CreateMatrixGaussSeidelMethod(size);
        Vector<double> vector = CreateVectorForGaussSeidelMethod(size, matrix);

        GaussSeidelMethod(matrix, vector, countOfIterations, showSolutions);

        Console.WriteLine("\n====================\n");

        AsyncGaussSeidelMethod(matrix, vector, countOfIterations, showSolutions);

    }
}