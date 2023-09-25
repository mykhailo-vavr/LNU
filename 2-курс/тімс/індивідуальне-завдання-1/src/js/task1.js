const getCountOfItems = frequencyTable =>
  Object.entries(frequencyTable).reduce(
    (prev, [_, value]) => prev + +value,
    0
  );

export const getVariationSeries = sample =>
  sample.sort((a, b) => a - b);

export const getFrequencyTable = sample => {
  const frequencyTable = {};

  for (const item of sample) {
    if (frequencyTable[item]) {
      frequencyTable[item]++;
    } else {
      frequencyTable[item] = 1;
    }
  }

  return frequencyTable;
};

export const getEmpiricalFunction = frequencyTable => {
  const entries = Object.entries(frequencyTable);
  const countOfItems = getCountOfItems(frequencyTable);
  let empiricalFunction = [];
  let temp = 0;

  empiricalFunction.push('0, якщо x < 0');

  for (let i = 0; i < entries.length - 1; i++) {
    empiricalFunction.push(
      `${(entries[i][1] / countOfItems + temp).toFixed(2)}, якщо ${
        entries[i][0]
      } <= x < ${entries[i + 1][0]}`
    );
    temp += entries[i][1] / countOfItems;
  }

  empiricalFunction.push(
    `1, якщо x >= ${Object.keys(frequencyTable).at(-1)}`
  );

  return empiricalFunction;
};

export const getMode = frequencyTable => {
  const entries = Object.entries(frequencyTable);
  let temp = 0;
  let mode;

  entries.forEach(([key, value]) => {
    if (value > temp) {
      temp = value;
      mode = key;
    }
  });

  return mode;
};

export const getMedian = variationSeries => {
  return (variationSeries / length) % 2
    ? variationSeries.slice(variationSeries.length / 2, 2)
    : variationSeries[Math.ceil(variationSeries.length / 2)];
};

export const getSelectiveAverage = frequencyTable =>
  Object.entries(frequencyTable).reduce(
    (prev, [key, value]) => prev + key * value,
    0
  ) / getCountOfItems(frequencyTable);

export const getDeviation = frequencyTable => {
  const selectiveAverage = getSelectiveAverage(frequencyTable);
  return Object.entries(frequencyTable).reduce(
    (prev, [key, value]) =>
      prev + value * (key - selectiveAverage) ** 2,
    0
  );
};

export const getVariance = frequencyTable =>
  getDeviation(frequencyTable) /
  (getCountOfItems(frequencyTable) - 1);

export const getStandard = frequencyTable =>
  Math.sqrt(getVariance(frequencyTable));

export const getVariation = frequencyTable =>
  getStandard(frequencyTable) / getSelectiveAverage(frequencyTable);

// Вибіркова дисперсія
export const getSelectiveVariance = frequencyTable =>
  getDeviation(frequencyTable) / getCountOfItems(frequencyTable);

// Середньоквадратичнe відхилення
export const getStandardDeviation = frequencyTable =>
  Math.sqrt(getSelectiveVariance(frequencyTable));

export const getSwing = frequencyTable => {
  const entries = Object.entries(frequencyTable);
  let min = 0;
  let max = 0;

  entries.forEach(([key, _]) => {
    if (key < min) {
      min = key;
    }
    if (key > max) {
      max = key;
    }
  });

  return max - min;
};

const getMoments = frequencyTable => {
  const moments = [];
  const countOfItems = getCountOfItems(frequencyTable);
  const selectiveAverage = getSelectiveAverage(frequencyTable);

  for (let i = 2; i < 5; i++) {
    const moment =
      Object.entries(frequencyTable).reduce(
        (prev, [key, value]) =>
          prev + value * Math.pow(key - selectiveAverage, i),
        0
      ) / countOfItems;

    moments.push(moment);
  }

  return moments;
};

export const getAsymmetry = frequencyTable => {
  const [u2, u3] = getMoments(frequencyTable);
  return u3 / Math.pow(u2, 3 / 2);
};

export const getExcess = frequencyTable => {
  const [u2, _, u4] = getMoments(frequencyTable);
  return u4 / u2 ** 2 - 3;
};

// Квартиль, октиль, дециль
export const getQuantiles = (sample, number) => {
  if (sample.length % number !== 0) {
    return ["Об'єм вибірки не є кратним " + number];
  }

  const breakpoint = Math.floor(sample.length / number);
  const quantiles = [];
  for (let i = 1; i < sample.length; i++) {
    if (i % breakpoint === 0) {
      quantiles.push(sample[i]);
    }
  }

  return `${quantiles} широта: ${quantiles.at(-1) - quantiles[0]}`;
};
