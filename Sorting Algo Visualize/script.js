let array = [];
let delay = 200;

function renderArray(arr, highlight = {}, sortedIndices = []) {
  const container = document.getElementById("array-container");
  container.innerHTML = "";

  arr.forEach((value, index) => {
    const barContainer = document.createElement("div");
    barContainer.style.display = "flex";
    barContainer.style.flexDirection = "column";
    barContainer.style.alignItems = "center";

    const label = document.createElement("div");
    label.innerText = value;
    label.style.marginBottom = "2px";
    label.style.fontSize = "12px";
    label.style.color = "black";
    label.style.fontWeight = "bold";

    const bar = document.createElement("div");
    bar.style.height = `${value * 5}px`;
    bar.classList.add("bar");

    if (highlight.comparing?.includes(index)) bar.classList.add("comparing");
    if (highlight.swapping?.includes(index)) bar.classList.add("swapping");
    if (sortedIndices.includes(index)) bar.classList.add("sorted");

    barContainer.appendChild(label);
    barContainer.appendChild(bar);
    container.appendChild(barContainer);
  });
}

function generateArray() {
  let custom = document.getElementById("custom-array").value.trim();
  if (custom !== "") {
    array = custom
      .split(",")
      .map(num => parseInt(num.trim()))
      .filter(n => !isNaN(n));
  } else {
    // Default array from your screenshot
    array = [30, 28, 35, 10, 25, 36, 32, 30, 8, 8, 12, 10, 38, 20, 15, 45, 10, 14, 12, 30];
  }
  renderArray(array);
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function bubbleSort(arr) {
  let sortedIndices = [];
  for (let i = 0; i < arr.length - 1; i++) {
    for (let j = 0; j < arr.length - i - 1; j++) {
      renderArray(arr, { comparing: [j, j + 1] }, sortedIndices);
      await sleep(delay);
      if (arr[j] > arr[j + 1]) {
        [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
        renderArray(arr, { swapping: [j, j + 1] }, sortedIndices);
        await sleep(delay);
      }
    }
    sortedIndices.push(arr.length - 1 - i);
  }
  sortedIndices = Array.from({ length: arr.length }, (_, i) => i);
  renderArray(arr, {}, sortedIndices);
}

async function selectionSort(arr) {
  let sortedIndices = [];
  for (let i = 0; i < arr.length; i++) {
    let minIndex = i;
    for (let j = i + 1; j < arr.length; j++) {
      renderArray(arr, { comparing: [minIndex, j] }, sortedIndices);
      await sleep(delay);
      if (arr[j] < arr[minIndex]) {
        minIndex = j;
      }
    }
    if (minIndex !== i) {
      [arr[i], arr[minIndex]] = [arr[minIndex], arr[i]];
      renderArray(arr, { swapping: [i, minIndex] }, sortedIndices);
      await sleep(delay);
    }
    sortedIndices.push(i);
  }
  renderArray(arr, {}, sortedIndices);
}

async function insertionSort(arr) {
  let sortedIndices = [];
  sortedIndices.push(0);
  for (let i = 1; i < arr.length; i++) {
    let key = arr[i];
    let j = i - 1;
    while (j >= 0 && arr[j] > key) {
      renderArray(arr, { comparing: [j, j + 1] }, sortedIndices);
      await sleep(delay);
      arr[j + 1] = arr[j];
      renderArray(arr, { swapping: [j, j + 1] }, sortedIndices);
      await sleep(delay);
      j--;
    }
    arr[j + 1] = key;
    sortedIndices.push(i);
  }
  renderArray(arr, {}, sortedIndices);
}

async function quickSort(arr, low, high, sortedIndices = []) {
  if (low < high) {
    let pi = await partition(arr, low, high, sortedIndices);
    await quickSort(arr, low, pi - 1, sortedIndices);
    await quickSort(arr, pi + 1, high, sortedIndices);
  }
  if (low >= 0 && high >= 0 && low < arr.length && high < arr.length) {
    for (let i = low; i <= high; i++) {
      if (!sortedIndices.includes(i)) sortedIndices.push(i);
    }
    renderArray(arr, {}, sortedIndices);
  }
}

async function partition(arr, low, high, sortedIndices) {
  let pivot = arr[high];
  let i = low - 1;
  for (let j = low; j < high; j++) {
    renderArray(arr, { comparing: [j, high] }, sortedIndices);
    await sleep(delay);
    if (arr[j] < pivot) {
      i++;
      [arr[i], arr[j]] = [arr[j], arr[i]];
      renderArray(arr, { swapping: [i, j] }, sortedIndices);
      await sleep(delay);
    }
  }
  [arr[i + 1], arr[high]] = [arr[high], arr[i + 1]];
  renderArray(arr, { swapping: [i + 1, high] }, sortedIndices);
  await sleep(delay);
  sortedIndices.push(i + 1);
  return i + 1;
}

async function mergeSort(arr, l, r, sortedIndices = []) {
  if (l >= r) return;
  const m = l + Math.floor((r - l) / 2);
  await mergeSort(arr, l, m, sortedIndices);
  await mergeSort(arr, m + 1, r, sortedIndices);
  await merge(arr, l, m, r, sortedIndices);
}

async function merge(arr, l, m, r, sortedIndices) {
  const left = arr.slice(l, m + 1);
  const right = arr.slice(m + 1, r + 1);
  let i = 0, j = 0, k = l;
  while (i < left.length && j < right.length) {
    renderArray(arr, { comparing: [k] }, sortedIndices);
    await sleep(delay);
    if (left[i] <= right[j]) {
      arr[k++] = left[i++];
    } else {
      arr[k++] = right[j++];
    }
  }
  while (i < left.length) arr[k++] = left[i++];
  while (j < right.length) arr[k++] = right[j++];
  for (let idx = l; idx <= r; idx++) {
    if (!sortedIndices.includes(idx)) sortedIndices.push(idx);
  }
  renderArray(arr, {}, sortedIndices);
}

async function startSort() {
  delay = parseInt(document.getElementById("speed").value);
  let algo = document.getElementById("algo").value;
  if (algo === "bubble") await bubbleSort(array);
  else if (algo === "selection") await selectionSort(array);
  else if (algo === "insertion") await insertionSort(array);
  else if (algo === "quick") await quickSort(array, 0, array.length - 1);
  else if (algo === "merge") await mergeSort(array, 0, array.length - 1);
}

// Load default array on start
generateArray();