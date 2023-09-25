import {
  getDFBinomical,
  getP,
  getProbabilitiesBinomical,
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

export const runTask2 = async () => {
  let data;
  await getDataFromFile('src/data/data.json').then(
    res => (data = res)
  );
  const intervalVariationsSeries = data.task2.intervals.map(
    (intervals, i) => [intervals, data.task2.values[i]]
  );

  let alpha = +prompt('Введіть рівень значущості: ', 0.05);
  let manually = confirm(
    'Задати параметри для другого завдання вручну?'
  );
  let p;
  if (manually) {
    p = +prompt('Введіть p: ');
  }

  ///////////////

  showLine({
    header:
      '-------------- Завдання 2. Біномний розподіл --------------'
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
    header: 'Параметр p',
    content: p || getP(intervalVariationsSeries)
  });

  showArray({
    header: 'Pi',
    array: getProbabilitiesBinomical(intervalVariationsSeries, p).map(
      (prob, i) => `p${i + 1}: ${prob}`
    )
  });

  const [mergedIntervals] = mergeIntervals(
    getProbabilitiesBinomical(intervalVariationsSeries, p),
    intervalVariationsSeries
  );

  showTableFromArray({
    header: 'Згрупований інтервальний розподіл',
    lines: mergedIntervals
  });

  showLine({
    header: 'Число ступенів вільності',
    content: getDFBinomical(mergedIntervals)
  });

  showLine({
    header: 'χ<sup>2</sup><sub>емпіричне</sub>',
    content: getXEmpirical(
      mergedIntervals,
      getProbabilitiesBinomical(mergedIntervals, p)
    )
  });

  showLine({
    header: 'χ<sup>2</sup><sub>критичне</sub>',
    content: getXCritical(getDFBinomical(mergedIntervals), alpha)
  });

  showLine({
    header: 'Висновок',
    content:
      getXEmpirical(
        mergedIntervals,
        getProbabilitiesBinomical(mergedIntervals, p)
      ) < getXCritical(getDFBinomical(mergedIntervals), alpha)
        ? 'Оскільки, χ<sup>2</sup><sub>емпіричне</sub> < χ<sup>2</sup><sub>критичне</sub> , то приймаємо гіпотезу'
        : 'Оскільки, χ<sup>2</sup><sub>емпіричне</sub> > χ<sup>2</sup><sub>критичне</sub> , то гіпотезу відхиляємо'
  });
};
