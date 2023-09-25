import { radixSort, stoogeSort } from './sorting-algorithms.js';
import {
  getArray,
  getArrayWithSortedSubArrays,
  getReversedArray,
  getSwappedArray,
  getSortedArray
} from './data.js';
import { getPerformance } from './utils.js';
import { showBreakLine, showSortStatistic } from './view.js';

const lengths = [100000, 1000000, 5000000];
const arrays = [
  getArray,
  getReversedArray,
  getSortedArray,
  getSwappedArray,
  getArrayWithSortedSubArrays
];
const types = [
  'Звичайний масив',
  'Масив впорядкований наоборот',
  'Впорядкований масив',
  'Масив зі свопами',
  'Масив з впорядкованими підмасивами'
];

arrays.forEach((array, i) => {
  for (const length of lengths) {
    showSortStatistic({
      length,
      type: types[i],
      time: getPerformance(radixSort.bind(null, array(length)))
      // time: getPerformance(stoogeSort.bind(null, array(length)))
    });
  }

  showBreakLine();
});
