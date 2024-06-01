const container = document.querySelector('.container');

export const showLine = ({ header, content }) => {
  const line = document.createElement('div');
  line.classList.add('line');

  if (header) {
    const headerContainer = document.createElement('h2');
    headerContainer.classList.add('line-header');
    line.append(headerContainer);
    headerContainer.innerHTML = header;
  }

  if (content) {
    const contentContainer = document.createElement('div');
    contentContainer.classList.add('line-content');
    line.append(contentContainer);

    if (typeof content === 'string') {
      contentContainer.innerHTML = content;
    } else {
      contentContainer.append(content);
    }
  }

  container.append(line);
};

export const showTableFromObject = ({ header, lines }) => {
  const content = document.createElement('div');
  for (const [key, value] of Object.entries(lines)) {
    const p = document.createElement('p');
    p.textContent = `${key}: ${value}\n`;
    content.append(p);
  }

  showLine({ header, content });
};

export const showTableFromArray = ({ header, lines }) => {
  const content = document.createElement('div');
  for (const [key, value] of lines) {
    const p = document.createElement('p');
    p.textContent = `${key[0].toFixed(3)}-${key[1].toFixed(
      3
    )}: ${value}\n`;
    content.append(p);
  }

  showLine({ header, content });
};

export const showArray = ({ header, array }) => {
  const content = document.createElement('div');
  for (const item of array) {
    const p = document.createElement('p');
    p.textContent = item;
    content.append(p);
  }

  showLine({ header, content });
};

export const showChart = ({ labels, data, type, label }) => {
  const chart = document.createElement('canvas');
  const className = Math.floor(Math.random() * 1000);
  chart.classList.add(className);
  container.append(chart);

  const content = {
    labels,
    datasets: [
      {
        label,
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 99, 132)',
        data
      }
    ]
  };

  const config = {
    type,
    data: content,
    options: {}
  };

  new Chart(chart, config);
};
