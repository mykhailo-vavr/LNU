function mergeSort(arr) {
	if (arr.length < 2) return;

	let mid = Math.floor(arr.length / 2),
		leftPart = arr.slice(0,mid),
		rightPart = arr.slice(mid);

    mergeSort(leftPart);
    mergeSort(rightPart);

    let i = j = k = 0;

	while (i < leftPart.length && j < rightPart.length) {
		if (leftPart[i] < rightPart[j]) {
			arr[k++] = leftPart[i++];
		}
        else {
			arr[k++] = rightPart[j++];
        }
	}

	while (i < leftPart.length)
		arr[k++] = leftPart[i++];

	while(j < rightPart.length)
		arr[k++] = rightPart[j++];

    return arr;
}

let arr = [6,5,3,1,35,6,8,4,3,4,6,2];
console.log(arr);
mergeSort(arr);
console.log(arr);