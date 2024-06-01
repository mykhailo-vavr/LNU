const fs = require('fs').promises;

const readJsonFromFile = async filePath => {
  try {
    const data = await fs.readFile(filePath, 'utf8');

    const jsonData = JSON.parse(data);

    return jsonData;
  } catch (error) {
    console.error('Error reading JSON file:', error.message);
    return null;
  }
};

class TramService {
  #data;

  constructor(data) {
    this.#data = data;
  }

  getById(id) {
    const tram = this.#data.find(tram => tram.id === id);

    return tram || null;
  }
}

class StopService {
  #data;

  constructor(data) {
    this.#data = data;
  }

  getById(id) {
    const stop = this.#data.find(tram => tram.id === id);

    return stop || null;
  }
}

class RouteService {
  #data;

  constructor(data, _tramService, _stopService) {
    this.#data = data;
    this.tramService = _tramService;
    this.stopService = _stopService;
  }

  getByStopsIds(fromStopId, toStopId) {
    let from;
    let to;

    for (const { tramId, direct, reverse } of this.#data) {
      for (const id of direct) {
        if (id === fromStopId && !from) {
          from = {
            tramId,
            route: direct,
          };
        }

        if (id === toStopId && !to) {
          to = {
            tramId,
            route: direct,
          };
        }

        if (from && to && from.tramId === to.tramId) {
          return {
            tramId: from.tramId,
            direction: [from.route[0], to.route.at(-1)],
          };
        }
      }

      for (const id of reverse) {
        if (id === fromStopId && !from) {
          from = {
            tramId,
            route: direct,
          };
        }

        if (id === toStopId && !to) {
          to = {
            tramId,
            route: direct,
          };
        }

        if (from && to && from.tramId === to.tramId) {
          return {
            tramId: from.tramId,
            direction: [from.route[0], to.route.at(-1)],
          };
        }
      }
    }

    if (from && to) {
      const hashMap = {};

      from.route.forEach(id => {
        hashMap[id] = 1;
      });

      for (const id of to.route) {
        if (hashMap[id]) {
          return [
            {
              tramId: from.tramId,
              direction: [from.route[0], from.route.at(-1)],
              changeStop: id,
            },
            {
              tramId: to.tramId,
              direction: [to.route[0], to.route.at(-1)],
              changeStop: null,
            },
          ];
        }
      }
    }

    return [];
  }

  format(fromId, toId, routesArr) {
    let str = '';

    routesArr.forEach((item, i) => {
      if (i === 0) {
        str += `Сідайте на ${
          this.tramService.getById(item.tramId).number
        } трамвай (${this.stopService.getById(item.direction[0]).stop} -> ${
          this.stopService.getById(item.direction[1]).stop
        }) на зупинці ${this.stopService.getById(fromId).stop}\n`;
      }

      if (i !== 0) {
        str += `Пересядьте на ${
          this.tramService.getById(item.tramId).number
        } трамвай (${this.stopService.getById(item.direction[0]).stop} -> ${
          this.stopService.getById(item.direction[1]).stop
        })\n`;
      }

      if (item.changeStop) {
        str += `Вийдіть на зупинці ${
          this.stopService.getById(item.changeStop).stop
        }\n`;
      }
    });

    str += `Вийдіть на зупинці ${this.stopService.getById(toId).stop}`;

    return str;
  }
}

const main = async () => {
  const db = await readJsonFromFile('db.json');

  const tramService = new TramService(db.trams);
  const stopService = new StopService(db.stops);
  const routeService = new RouteService(db.routes, tramService, stopService);

  const fromId = 17;
  const toId = 50;

  if (!stopService.getById(fromId) || !stopService.getById(toId)) {
    console.log('Неправильна зупинка або зупинки');
  }

  const data = routeService.getByStopsIds(17, 50);
  console.log(routeService.format(17, 57, data));

  //   console.log(routeService.getByStopsIds(20, 30));
};

main();
