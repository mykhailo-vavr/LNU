const getIntervalCount = length => {
  for (let i = 1; i < length; i++) {
    if (Math.pow(2, i) < length && length <= Math.pow(2, i + 1)) {
      return i + 1;
    }
  }
};

const getCountOfItems = intervalVariationsSeries => {
  const [_, values] = getDataFromIntervalVariationsSeries(
    intervalVariationsSeries
  );
  return values.reduce((p, c) => p + c, 0);
};

const getDataFromIntervalVariationsSeries =
  intervalVariationsSeries => {
    const intervals = intervalVariationsSeries.map(([keys]) => keys);
    const values = intervalVariationsSeries.map(
      ([_, values]) => values
    );

    return [intervals, values];
  };

export const getIntervalVariationsSeries = variationSeries => {
  const min = Math.min(...variationSeries);
  const max = Math.max(...variationSeries);
  const intervalsCount = getIntervalCount(variationSeries.length);
  const step = (max - min) / intervalsCount;
  let temp = min;
  const intervals = [];
  let valuesForInterval = [];

  for (let i = 0; i < variationSeries.length + 1; i++) {
    const intervalRange = [temp, temp + step];

    if (variationSeries[i] <= temp + step) {
      valuesForInterval.push(variationSeries[i]);
      continue;
    }

    intervals.push([intervalRange, valuesForInterval.length]);
    valuesForInterval = [variationSeries[i]];
    temp += step;
  }

  return intervals;
};

////////////////////////////////////////

export const getModeInterval = intervalVariationsSeries => {
  const [intervals, values] = getDataFromIntervalVariationsSeries(
    intervalVariationsSeries
  );

  let index = 0;
  let temp = 0;

  values.forEach((value, i) => {
    if (value > temp) {
      temp = value;
      index = i;
    }
  });

  return +(
    intervals[index - 1][1] +
    ((values[index] - values[index - 1]) /
      (values[index] -
        values[index - 1] +
        (values[index] - values[index + 1]))) *
      (intervals[index][1] - intervals[index - 1][1])
  ).toFixed(3);
};

export const getMedianInterval = intervalVariationsSeries => {
  const [intervals, values] = getDataFromIntervalVariationsSeries(
    intervalVariationsSeries
  );

  const index = Math.ceil(intervalVariationsSeries.length / 2) - 1;

  return (
    intervals[index - 1][1] +
    ((intervals[index][1] - intervals[index - 1][1]) /
      values[index]) *
      (getCountOfItems(intervalVariationsSeries) / 2 -
        getCountOfItems(intervalVariationsSeries.slice(0, index)))
  );
};

export const getSelectiveAverageInterval =
  intervalVariationsSeries => {
    const [intervals, values] = getDataFromIntervalVariationsSeries(
      intervalVariationsSeries
    );

    return +(
      intervals.reduce(
        (prev, [a1, a2], i) => prev + ((a1 + a2) / 2) * values[i],
        0
      ) / getCountOfItems(intervalVariationsSeries)
    ).toFixed(3);
  };

export const getDeviationInterval = intervalVariationsSeries => {
  const selectiveAverage = getSelectiveAverageInterval(
    intervalVariationsSeries
  );
  const [intervals, values] = getDataFromIntervalVariationsSeries(
    intervalVariationsSeries
  );

  return intervals.reduce(
    (prev, [a1], i) =>
      prev + values[i] * (a1 - selectiveAverage) ** 2,
    0
  );
};

export const getVarianceInterval = intervalVariationsSeries =>
  getDeviationInterval(intervalVariationsSeries) /
  (getCountOfItems(intervalVariationsSeries) - 1);

export const getStandardInterval = intervalVariationsSeries =>
  Math.sqrt(getVarianceInterval(intervalVariationsSeries));

export const getVariationInterval = intervalVariationsSeries =>
  getStandardInterval(intervalVariationsSeries) /
  getSelectiveAverageInterval(intervalVariationsSeries);

// Вибіркова дисперсія
export const getSelectiveVarianceInterval =
  intervalVariationsSeries =>
    getDeviationInterval(intervalVariationsSeries) /
    getCountOfItems(intervalVariationsSeries);

// Середньоквадратичнe відхилення
export const getStandardDeviationInterval =
  intervalVariationsSeries =>
    Math.sqrt(getSelectiveVarianceInterval(intervalVariationsSeries));

export const getSwingInterval = intervalVariationsSeries => {
  const [intervals] = getDataFromIntervalVariationsSeries(
    intervalVariationsSeries
  );

  return intervals.at(-1)[1] - intervals[0][0];
};

export const getMomentsInterval = intervalVariationsSeries => {
  const [intervals, values] = getDataFromIntervalVariationsSeries(
    intervalVariationsSeries
  );
  const moments = [];
  const countOfItems = getCountOfItems(intervalVariationsSeries);
  const selectiveAverage = getSelectiveAverageInterval(
    intervalVariationsSeries
  );

  for (let i = 2; i < 5; i++) {
    const moment =
      intervals.reduce(
        (prev, [a1], j) =>
          prev + values[j] * (a1 - selectiveAverage) ** i,
        0
      ) / countOfItems;

    moments.push(+moment.toFixed(5));
  }

  return moments;
};

export const getAsymmetryInterval = intervalVariationsSeries => {
  const [u2, u3] = getMomentsInterval(intervalVariationsSeries);
  return u3 / Math.pow(u2, 3 / 2);
};

export const getExcessInterval = intervalVariationsSeries => {
  const [u2, _, u4] = getMomentsInterval(intervalVariationsSeries);
  return u4 / u2 ** 2 - 3;
};
