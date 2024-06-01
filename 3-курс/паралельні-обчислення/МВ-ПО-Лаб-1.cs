using System;
using System.Linq;
using System.Threading;
using System.Collections.Generic;
using System.Diagnostics;

// Михайло Ваврикович, ПМІ-33, 5 варіант, лабораторна 1

// Знайти рядок максимальної довжини в масиві рядків

/*

При кількості потоків = 12, та елементів масиву рівному 10000000, можна побачити результат у розмірі 2036 мілісекунди
І відповідно при такій же розмірності, але при виконанні програми в одному основному потоці час складає 1396 мілісекунд
 
При розмірі масиву більше ~60000000 позитивних резутьтатів при розпаралеленні 
не спостерігається тобто час в порівнянні з використання одного потоку збільшується

Для оптимального часу виконання при багапоточному обчисленні
кількість потоків потрібно підбирати в залежності від розміру масиву.
Переважно оптимальна кількість потоків 2 < k < 50

 */


class Program
{
    public delegate string D(string[] arr);

    static public string[] GetArrayOfStrings(int length, int stringMaxLength)
    {
        Random rand = new Random();
        string[] arr = new string[length];

        for (int i = 0; i < length; i++)
        {
            arr[i] = new string('a', rand.Next(1, stringMaxLength + 1));
        }

        return arr;
    }

    static public string GetLongestStringInArr(string[] arr)
    {
        Console.WriteLine("Thread {0}", Thread.CurrentThread.ManagedThreadId);

        return arr.Max();
    }

    public static void CalculateInOneThread(string[] arr)
    {
        Stopwatch stopwatch = new Stopwatch();
        stopwatch.Start();

        string longestString = GetLongestStringInArr(arr);

        stopwatch.Stop();
        Console.WriteLine($"Execution Time: {stopwatch.ElapsedMilliseconds} ms");

        Console.WriteLine("Longest word: {0}\nLength: {1}", longestString, longestString.Length);
    }

    public static void CalculateInManyThreads(string[] arr, int countOfThreads)
    {
        Stopwatch stopwatch = new Stopwatch();
        stopwatch.Start();

        D del = GetLongestStringInArr;

        List<IAsyncResult> asyncResults = new List<IAsyncResult>();

        int countOfChunks = arr.Count() / countOfThreads;

        for (int i = 0; i < countOfThreads; i++)
        {
            IAsyncResult asyncResult = del.BeginInvoke(arr.Skip(i * countOfChunks).Take(countOfChunks).ToArray(), null, null);
            asyncResults.Add(asyncResult);
        }

        string longestString = asyncResults.Max(asyncResult =>
        {
            return del.EndInvoke(asyncResult);
        });

        stopwatch.Stop();
        Console.WriteLine($"Execution Time: {stopwatch.ElapsedMilliseconds} ms");

        Console.WriteLine("Longest word: {0}\nLength: {1}", longestString, longestString.Length);
    }

    static void Main()
    {
        const int countOfThreads = 10;
        const int length = 10000000;
        const int stringMaxLength = 30;

        string[] arr = GetArrayOfStrings(length, stringMaxLength);

        Console.WriteLine("Calculation results in one thread:");
        CalculateInOneThread(arr);

        Console.WriteLine("\n==================\n");

        Console.WriteLine("Calculation results in many threads:");
        CalculateInManyThreads(arr, countOfThreads);

        Console.Read();
    }
}
