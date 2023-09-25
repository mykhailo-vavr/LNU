import { getRandomInRange, getRandomNumber } from './utils.js';

export const getArray = (length, mapfn = getRandomNumber) =>
  Array.from({ length }, mapfn);

export const getArrayWithSortedSubArrays = length =>
  getArray(10, () => 1)
    .map(() => getArray(length / 10).sort((a, b) => a - b))
    .flat(Infinity);

export const getSwappedArray = length => {
  const array = getArray(length).sort((a, b) => a - b);
  const positions = [];

  const getPosition = () => {
    const position = getRandomInRange(0, array.length - 1);
    return positions.includes(position) ? getPosition() : position;
  };

  for (let i = 0; i < array.length / 100; i++) {
    const pos1 = getPosition();
    const pos2 = getPosition();
    [array[pos1], array[pos2]] = [array[pos2], array[pos1]];

    positions.push(pos1, pos2);
  }
  return array;
};

export const getReversedArray = length =>
  getArray(length).sort((a, b) => b - a);

export const getSortedArray = length =>
  getArray(length).sort((a, b) => a - b);
