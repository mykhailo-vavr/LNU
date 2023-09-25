import {
  showArray,
  showChart,
  showLine,
  showTableFromArray,
  showTableFromObject
} from './view.js';
import { getSample } from './utils.js';
import {
  getEmpiricalFunction,
  getFrequencyTable,
  getVariationSeries,
  getMode,
  getMedian,
  getSelectiveAverage,
  getDeviation,
  getVariance,
  getStandard,
  getVariation,
  getSelectiveVariance,
  getSwing,
  getStandardDeviation,
  getAsymmetry,
  getExcess,
  getQuantiles
} from './task1.js';
import {
  getDeviationInterval,
  getIntervalVariationsSeries,
  getSelectiveVarianceInterval,
  getMedianInterval,
  getModeInterval,
  getSelectiveAverageInterval,
  getStandardDeviationInterval,
  getStandardInterval,
  getVarianceInterval,
  getVariationInterval,
  getSwingInterval,
  getMomentsInterval,
  getAsymmetryInterval,
  getExcessInterval
} from './task2.js';

// const sample = getSample(60);
const sample = [
  5, 5, 7, 7, 7, 7, 7, 10, 10, 10, 10, 10, 10, 10, 10, 15, 15, 15, 15,
  15
];
const variationSeries = getVariationSeries([...sample]);

///////////////

showLine({
  header: '-------------- Завдання 1 --------------'
});

const frequencyTable = getFrequencyTable([...sample]);

///////////////

showLine({
  header: 'Вибірка',
  content: sample.decorateArray()
});
showLine({
  header: 'Варіаційний ряд',
  content: variationSeries.decorateArray()
});
showTableFromObject({
  header: 'Частотна таблиця',
  lines: frequencyTable
});

///////////////

showChart({
  label: 'Полігон частот',
  type: 'line',
  data: Object.values(frequencyTable),
  labels: Object.keys(frequencyTable)
});
showChart({
  label: 'Діаграма частот',
  type: 'bar',
  data: Object.values(frequencyTable),
  labels: Object.keys(frequencyTable)
});

///////////////

showArray({
  header: 'Емпірична функія',
  array: getEmpiricalFunction(frequencyTable)
});

///////////////

showLine({
  header: 'Мода',
  content: getMode(frequencyTable)
});
showLine({
  header: 'Медіана',
  content: getMedian(variationSeries)
});
showLine({
  header: 'Середнє вибіркове',
  content: getSelectiveAverage(frequencyTable)
});
showLine({
  header: 'Девіація',
  content: getDeviation(frequencyTable)
});
showLine({
  header: 'Варінса',
  content: getVariance(frequencyTable)
});
showLine({
  header: 'Стандарт',
  content: getStandard(frequencyTable)
});
showLine({
  header: 'Варіація',
  content: getVariation(frequencyTable)
});
showLine({
  header: 'Вибіркова дисперсія',
  content: getSelectiveVariance(frequencyTable)
});
showLine({
  header: 'Середньоквадратичне відхилення',
  content: getStandardDeviation(frequencyTable)
});
showLine({
  header: 'Розмах',
  content: getSwing(frequencyTable)
});
showLine({
  header: 'Асиметрія',
  content: getAsymmetry(frequencyTable)
});
showLine({
  header: 'Ексцес',
  content: getExcess(frequencyTable)
});
showLine({
  header: 'Кваритилі',
  content: getQuantiles(variationSeries, 4)
});
showLine({
  header: 'Октилі',
  content: getQuantiles(variationSeries, 8)
});
showLine({
  header: 'Децилі',
  content: getQuantiles(variationSeries, 10)
});

////////////////////////////

showLine({
  header: '-------------- Завдання 2 --------------'
});

const intervalVariationsSeries =
  getIntervalVariationsSeries(variationSeries);

////////////////////////////

showTableFromArray({
  header: 'Інтервальний розподіл',
  lines: intervalVariationsSeries
});

////////////////////////////

showChart({
  label: 'Гістограма розподілу',
  data: intervalVariationsSeries.map(item => item[1]),
  labels: intervalVariationsSeries.map(
    ([[a, b]]) => a.toFixed(3) + ' - ' + b.toFixed(3)
  ),
  type: 'bar'
});

////////////////////////////

showLine({
  header: 'Мода',
  content: getModeInterval(intervalVariationsSeries)
});

showLine({
  header: 'Медіана',
  content: getMedianInterval(intervalVariationsSeries)
});

showLine({
  header: 'Середнє вибіркове',
  content: getSelectiveAverageInterval(intervalVariationsSeries)
});

showLine({
  header: 'Девіація',
  content: getDeviationInterval(intervalVariationsSeries)
});

showLine({
  header: 'Варіанса',
  content: getVarianceInterval(intervalVariationsSeries)
});

showLine({
  header: 'Стандарт',
  content: getStandardInterval(intervalVariationsSeries)
});

showLine({
  header: 'Варіація',
  content: getVariationInterval(intervalVariationsSeries)
});

showLine({
  header: 'Вибіркова дисперсія',
  content: getSelectiveVarianceInterval(intervalVariationsSeries)
});

showLine({
  header: 'Середньоквадратичне відхилення',
  content: getStandardDeviationInterval(intervalVariationsSeries)
});

showLine({
  header: 'Розмах',
  content: getSwingInterval(intervalVariationsSeries)
});

showLine({
  header: 'Моменти',
  content: getMomentsInterval(
    intervalVariationsSeries
  ).decorateArray()
});

showLine({
  header: 'Асиметрія',
  content: getAsymmetryInterval(intervalVariationsSeries)
});

showLine({
  header: 'Ексцес',
  content: getExcessInterval(intervalVariationsSeries)
});
