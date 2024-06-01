export const getSample = length =>
  Array.from({ length }, () => Math.round(Math.random() * 10));

Array.prototype.decorateArray = function () {
  return this.join(', ');
};
