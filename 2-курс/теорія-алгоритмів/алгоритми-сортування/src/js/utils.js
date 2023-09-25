export const getRandomNumber = () => Math.round(Math.random() * 1000);

export const getRandomInRange = (min, max) =>
  Math.floor(Math.random() * (max - min + 1)) + min;

export const getPerformance = func => {
  const start = Date.now();
  func();
  return Date.now() - start;
};
