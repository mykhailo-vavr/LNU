using System;
using System.Linq;
using System.Threading;
using System.Collections.Generic;
using System.Diagnostics;

// Михайло Ваврикович, ПМІ-33, 5 варіант, лабораторна 2

// Метод обчислення скалярного добутку двох випадкових векторів.

/*

При n = 10000000, при однопотоковому виконанні час = 413 мс. Для багатопотокового (k = 20) час виконання = 296 мс.

При відносно невеликих n (n < ~100000) програма виконується з однаковим часом для однопотокового та багатопотокового виконання
Розпаралелювання на потоки є помітно ефективнішим, порівняно з послідовним виконанням переважно для доволі великих n (n > ~10000000)
Оптимальна кількість потоків залежить він n. Зазвичай оптимальне k ~ n / 100000

*/


class Program
{
    public delegate List<int> D(List<int> v1, List<int> v2);

    public static List<int> GetVector(int length)
    {
        Random rand = new Random();
        List<int> v = new List<int>();

        for (int i = 0; i < length; i++)
        {
           v.Add(rand.Next(10));
        }

        return v;
    }
    public static List<int> GetScalar(List<int> v1, List<int> v2)
    {
        return v1.Select((value, index) => value * v2[index]).ToList();
    }

    public static void Callback(IAsyncResult asyncResult)
    {
        Console.WriteLine("Thread {0}", Thread.CurrentThread.ManagedThreadId);
    }

    public static void CalculateInOneThread(List<int> v1, List<int> v2)
    {
        Stopwatch stopwatch = new Stopwatch();
        stopwatch.Start();

        D del = GetScalar;

        IAsyncResult asyncResult = del.BeginInvoke(v1, v2, new AsyncCallback(Callback), null);

        while (!asyncResult.IsCompleted)
        {
            Thread.Sleep(1);
        }

        List<int> res = del.EndInvoke(asyncResult);

        stopwatch.Stop();
        Console.WriteLine($"Execution Time: {stopwatch.ElapsedMilliseconds} ms");

        //Console.WriteLine("Result: {0}", string.Join(", ", res));
    }

    public static void CalculateInManyThreads(List<int> v1, List<int> v2, int countOfThreads)
    {
        Stopwatch stopwatch = new Stopwatch();
        stopwatch.Start();

        D del = GetScalar;
        List<Tuple<IAsyncResult, int>> asyncResults = new List<Tuple<IAsyncResult, int>>();
        List<int> res = new List<int>();

        int countOfChunks = v1.Count / countOfThreads;

        for (int i = 0; i < countOfThreads; i++)
        {
            IAsyncResult asyncResult = del.BeginInvoke(
                v1.GetRange(i * countOfChunks, countOfChunks),
                v2.GetRange(i * countOfChunks, countOfChunks),
                new AsyncCallback(Callback),
                null
            );

            asyncResults.Add(new Tuple<IAsyncResult, int>(asyncResult, i * countOfChunks));
        }

        asyncResults.ForEach(asyncResult => {
            while (!asyncResult.Item1.IsCompleted)
            {
                Thread.Sleep(1);
            }

            List<int> result = del.EndInvoke(asyncResult.Item1);
            res.InsertRange(asyncResult.Item2, result);
        });

        stopwatch.Stop();
        Console.WriteLine($"Execution Time: {stopwatch.ElapsedMilliseconds} ms");

      //  Console.WriteLine("Result: {0}", string.Join(", ", res));
    }

    static void Main()
    {
        const int countOfThreads = 100;
        const int length = 10000000;

        List<int> v1 = GetVector(length);
        List<int> v2 = GetVector(length);

        //Console.WriteLine("Vector 1: {0}", string.Join(", ", v1));
        //Console.WriteLine("Vector 2: {0}", string.Join(", ", v2));

        Console.WriteLine("\nCalculation results in one thread:");
        CalculateInOneThread(v1, v2);

        Console.WriteLine("\n==================\n");

        Console.WriteLine("Calculation results in many threads:");
        CalculateInManyThreads(v1, v2, countOfThreads);

        Console.Read();
    }
}
