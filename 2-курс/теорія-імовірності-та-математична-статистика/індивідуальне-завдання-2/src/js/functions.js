import { chi2Critical, laplaceValues } from './utils.js';

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
    (prev, [a1, a2], i) =>
      prev + values[i] * ((a1 + a2) / 2 - selectiveAverage) ** 2,
    0
  );
};

export const getVarianceInterval = intervalVariationsSeries =>
  getDeviationInterval(intervalVariationsSeries) /
  (getCountOfItems(intervalVariationsSeries) - 1);

export const getStandardInterval = intervalVariationsSeries =>
  Math.sqrt(getVarianceInterval(intervalVariationsSeries));

const getLaplaceValue = x => {
  const isPositive = x > 0;
  const strX = (x + '').replace('-', '');
  const i = strX[0] === '0' ? strX[2] : strX[0] + strX[2];
  const j = strX[3];

  return isPositive ? laplaceValues[i][j] : -laplaceValues[i][j];
};

const getProbability = (x1, x2, a, sigma) =>
  getLaplaceValue((x2 - a) / sigma) -
  getLaplaceValue((x1 - a) / sigma);

export const getProbabilities = (
  intervalVariationsSeries,
  a,
  sigma
) => {
  const [intervals] = getDataFromIntervalVariationsSeries(
    intervalVariationsSeries
  );

  a = a || getSelectiveAverageInterval(intervalVariationsSeries);
  sigma = sigma || getStandardInterval(intervalVariationsSeries);

  const probabilities = [];

  intervals.forEach(([a1, a2], i) => {
    if (i === 0) {
      probabilities.push(getLaplaceValue((a2 - a) / sigma) + 0.5);
    } else if (i === intervals.length - 1) {
      probabilities.push(0.5 - getLaplaceValue((a1 - a) / sigma));
    } else {
      probabilities.push(getProbability(a1, a2, a, sigma));
    }
  });

  return probabilities;
};

export const mergeIntervals = (probs, intervalVariationsSeries) => {
  let intervals = JSON.parse(
    JSON.stringify(intervalVariationsSeries)
  );
  let probabilities = [...probs];

  for (let i = 0; i < intervals.length - 2; i++) {
    if (
      intervals[i][1] < 5 ||
      intervals[i][1] * probabilities[i] < 10
    ) {
      intervals = [
        ...intervals.slice(0, i),
        [
          [intervals[i][0][0], intervals[i + 1][0][1]],
          intervals[i][1] + intervals[i + 1][1]
        ],
        ...intervals.slice(i + 2)
      ];

      probabilities = [
        ...probabilities.slice(0, i),
        [probabilities[i], probabilities[i + 1]],
        ...probabilities.slice(i + 2)
      ];
      i = 0;
    }
  }

  // for (let i = intervals.length - 1; i > 1; i--) {
  //   if (
  //     intervals[i][1] < 5 ||
  //     intervals[i][1] * probabilities[i] < 10
  //   ) {
  //     intervals = [
  //       ...intervals.slice(-i),
  //       [
  //         [intervals[i][0][0], intervals[i - 1][0][1]],
  //         intervals[i][1] + intervals[i - 1][1]
  //       ],
  //       ...intervals.slice(-(i + 2))
  //     ];

  //     probabilities = [
  //       ...probabilities.slice(-i),
  //       [probabilities[i], probabilities[i - 1]],
  //       ...probabilities.slice(-(i + 2))
  //     ];
  //     i = intervals.length - 1;
  //   }
  // }

  return [intervals, probabilities];
};

export const getXEmpirical = (
  intervalVariationsSeries,
  probabilities
) => {
  console.log(intervalVariationsSeries, probabilities);
  const [_, values] = getDataFromIntervalVariationsSeries(
    intervalVariationsSeries
  );
  const count = getCountOfItems(intervalVariationsSeries);
  return probabilities.reduce(
    (prev, prob, i) =>
      prev + (values[i] - count * prob) ** 2 / (count * prob),
    0
  );
};

export const getDF = mergedIntervals => mergedIntervals.length - 2;

export const getXCritical = (df, a = 0.05) => {
  const aValues = {
    0.995: 0,
    0.99: 1,
    0.975: 2,
    0.95: 3,
    '0.90': 4,
    '0.10': 5,
    0.05: 6,
    0.025: 7,
    0.01: 8,
    0.005: 9
  };

  return chi2Critical[df][aValues[a]];
};

export const getP = intervalVariationsSeries => {
  const [intervals] = getDataFromIntervalVariationsSeries(
    intervalVariationsSeries
  );
  return (
    getSelectiveAverageInterval(intervalVariationsSeries) /
    Math.max(...intervals.map(([a1, a2]) => (a2 + a1) / 2))
  );
};

function f(num) {
  if (num < 0) return -1;
  else if (num == 0) return 1;
  else {
    return num * f(num - 1);
  }
}
export const getProbabilitiesBinomical = (
  intervalVariationsSeries,
  p
) => {
  p = p || getP(intervalVariationsSeries);
  const q = 1 - p;
  const [intervals, values] = getDataFromIntervalVariationsSeries(
    intervalVariationsSeries
  );
  const max = Math.max(...intervals.map(([a1, a2]) => (a2 + a1) / 2));
  const probabilities = [];

  values.forEach((_, i) => {
    probabilities.push(
      (f(max) / (f(i) * f(max - i))) * p ** i * Math.pow(q, max - i)
    );
  });

  return probabilities;
};

export const getDFBinomical = mergedIntervals =>
  mergedIntervals.length - 2;
