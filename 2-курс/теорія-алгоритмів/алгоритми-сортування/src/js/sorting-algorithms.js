export function stoogeSort(arr, start = 0, end = arr.length - 1) {
  if (arr[start] > arr[end]) {
    [arr[start], arr[end]] = [arr[end], arr[start]];
  }

  if (end - start + 1 > 2) {
    const temp = Math.floor((end - start + 1) / 3);
    stoogeSort(arr, start, end - temp);
    stoogeSort(arr, start + temp, end);
    stoogeSort(arr, start, end - temp);
  }

  return arr;
}

////////////

export const radixSort = array => {
  const sort = nth => {
    let i, j, k;
    let nextRadix = false;
    const currentPlaceValue = 10 ** nth;
    const nextPlaceValue = 10 ** (nth + 1);
    const buckets = Array.from({ length: 20 }, () => []);
    i = 0;

    for (j = 0; j < array.length; j++) {
      let val = array[j];
      let uVal = Math.abs(val);
      if (uVal >= nextPlaceValue) {
        nextRadix = true;
      }
      const digit = Math.floor(uVal / currentPlaceValue) % 10;
      if (val >= 0) {
        buckets[digit + 10].push(val);
      } else {
        buckets[10 - digit].push(val);
      }
    }
    for (j = 0; j < buckets.length; j++) {
      const bucket = buckets[j];
      for (k = 0; k < bucket.length; k++) {
        array[i++] = bucket[k];
      }
    }
    return nextRadix;
  };
  let radix = 0;
  if (array.length > 1) {
    while (sort(radix++));
  }
  return array;
};
