import {
  getDF,
  getProbabilities,
  getSelectiveAverageInterval,
  getStandardInterval,
  getXCritical,
  getXEmpirical,
  mergeIntervals
} from './functions.js';
import { getDataFromFile } from './utils.js';
import {
  showLine,
  showChart,
  showArray,
  showTableFromArray
} from './view.js';

export const runTask1 = async () => {
  let data;
  await getDataFromFile('src/data/data.json').then(
    res => (data = res)
  );
  const intervalVariationsSeries = data.task1.intervals.map(
    (intervals, i) => [intervals, data.task1.values[i]]
  );

  let alpha = +prompt('Введіть рівень значущості: ', 0.05);
  let manually = confirm(
    'Задати параметри для першого завдання вручну?'
  );
  let a, sigma;
  if (manually) {
    a = +prompt('Введіть a: ');
    sigma = +prompt('Введіть сигму: ');
  }

  ///////////////

  showLine({
    header:
      '-------------- Завдання 1. Нормальний розподіл--------------'
  });

  ///////////////

  showTableFromArray({
    header: 'Інтервальний розподіл',
    lines: intervalVariationsSeries
  });

  showChart({
    label: 'Гістограма розподілу',
    data: intervalVariationsSeries.map(item => item[1]),
    labels: intervalVariationsSeries.map(([bounds]) =>
      bounds.join(' - ')
    ),
    type: 'bar'
  });

  ///////////////

  showLine({
    header: 'Параметр а',
    content:
      a || getSelectiveAverageInterval(intervalVariationsSeries)
  });

  showLine({
    header: 'Параметр σ',
    content: sigma || getStandardInterval(intervalVariationsSeries)
  });

  showArray({
    header: 'Pi',
    array: getProbabilities(intervalVariationsSeries, a, sigma).map(
      (prob, i) => `p${i + 1}: ${prob}`
    )
  });

  const [mergedIntervals] = mergeIntervals(
    getProbabilities(intervalVariationsSeries, a, sigma),
    intervalVariationsSeries
  );

  showTableFromArray({
    header: 'Згрупований інтервальний розподіл',
    lines: mergedIntervals
  });

  showLine({
    header: 'Число ступенів вільності',
    content: getDF(mergedIntervals)
  });

  showLine({
    header: 'χ<sup>2</sup><sub>емпіричне</sub>',
    content: getXEmpirical(
      mergedIntervals,
      getProbabilities(mergedIntervals, a, sigma)
    )
  });

  showLine({
    header: 'χ<sup>2</sup><sub>критичне</sub>',
    content: getXCritical(getDF(mergedIntervals), alpha)
  });

  showLine({
    header: 'Висновок',
    content:
      getXEmpirical(
        mergedIntervals,
        getProbabilities(mergedIntervals, a, sigma)
      ) < getXCritical(getDF(mergedIntervals), alpha)
        ? 'Оскільки, χ<sup>2</sup><sub>емпіричне</sub> < χ<sup>2</sup><sub>критичне</sub> , то приймаємо гіпотезу'
        : 'Оскільки, χ<sup>2</sup><sub>емпіричне</sub> > χ<sup>2</sup><sub>критичне</sub> , то гіпотезу відхиляємо'
  });
};
