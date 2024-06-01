const container = document.querySelector('.container');

export const showSortStatistic = ({ length, type, time }) => {
  const line = document.createElement('div');
  line.classList.add('line');
  console.log(time);
  const headerContainer = document.createElement('h2');
  headerContainer.classList.add('line-header');
  headerContainer.textContent = `${type}, розмірність: ${length}`;
  line.append(headerContainer);

  const contentContainer = document.createElement('div');
  contentContainer.classList.add('line-content');
  const timeParsed = new Date(time);
  contentContainer.textContent = `Час виконання: ${
    (timeParsed.getMinutes() ? timeParsed.getMinutes() + 'хв ' : '') +
    (timeParsed.getSeconds() ? timeParsed.getSeconds() + 'c ' : '') +
    (timeParsed.getMilliseconds()
      ? timeParsed.getMilliseconds() + 'мc '
      : ' менше 1мс')
  }`;
  line.append(contentContainer);

  container.append(line);
};

export const showBreakLine = () => {
  const breakLine = document.createElement('p');
  breakLine.classList.add('break_line');
  breakLine.textContent = '------------------';
  container.append(breakLine);
};
