const fs = require("fs");

function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function getRandomElement(array) {
  return array[Math.floor(Math.random() * array.length)];
}

function getRandomDate(startYear = 2022, endYear = 2024) {
  const year = getRandomInt(startYear, endYear);
  const month = getRandomInt(1, 12);
  const day = getRandomInt(1, 28);
  const hour = getRandomInt(0, 23);
  const minute = getRandomInt(0, 59);
  const second = getRandomInt(0, 59);

  return new Date(year, month - 1, day, hour, minute, second).toISOString();
}

function generateRandomCoordinates() {
  return {
    latitude: parseFloat((Math.random() * 180 - 90).toFixed(4)),
    longitude: parseFloat((Math.random() * 360 - 180).toFixed(4)),
  };
}

const routerTypes = [
  {
    type: "wifi",
    namePrefix: [
      "Office",
      "Conference",
      "Guest",
      "Public",
      "Private",
      "5G",
      "Dual-Band",
      "High-Speed",
      "Mesh",
      "Enterprise",
    ],
    nameSuffix: [
      "WiFi",
      "Router",
      "Access Point",
      "AP",
      "Hotspot",
      "Network",
      "Wireless",
      "Hub",
    ],
    generateSpecificFields: () => {
      return {
        wifiChannels: Array.from({ length: getRandomInt(2, 8) }, () =>
          getRandomInt(1, 48)
        ),
        supportsDualBand: Math.random() > 0.3, // 70% chance of dual band support
      };
    },
  },
  {
    type: "enterprise",
    namePrefix: [
      "Data Center",
      "Corporate",
      "Cloud",
      "Gateway",
      "Core",
      "Edge",
      "Server Room",
      "Branch",
      "Global",
      "Regional",
    ],
    nameSuffix: [
      "Router",
      "Gateway",
      "Switch",
      "Network",
      "Hub",
      "Infrastructure",
      "Node",
      "Platform",
    ],
    generateSpecificFields: () => {
      return {
        portCount: getRandomInt(24, 384),
        supportedProtocols: (() => {
          const protocols = [
            "BGP",
            "OSPF",
            "IS-IS",
            "EIGRP",
            "RIP",
            "MPLS",
            "LISP",
            "PIM",
            "VRRP",
            "HSRP",
          ];
          const count = getRandomInt(2, 6);
          const selected = [];

          while (selected.length < count) {
            const protocol = getRandomElement(protocols);
            if (!selected.includes(protocol)) {
              selected.push(protocol);
            }
          }

          return selected;
        })(),
        throughputGbps: getRandomElement([1, 10, 25, 40, 100, 400]),
      };
    },
  },
  {
    type: "home",
    namePrefix: [
      "Home",
      "Residential",
      "Family",
      "Smart Home",
      "Personal",
      "Living Room",
      "Apartment",
      "House",
      "Basic",
      "Premium",
    ],
    nameSuffix: [
      "Router",
      "Gateway",
      "Network",
      "Hub",
      "WiFi",
      "Connection",
      "Internet",
    ],
    generateSpecificFields: () => {
      return {
        connectedDevices: getRandomInt(1, 30),
        parentalControlsEnabled: Math.random() > 0.5,
        maxBandwidthMbps: getRandomElement([100, 200, 300, 500, 1000]),
      };
    },
  },
];

function generateRouter(id) {
  const routerType = getRandomElement(routerTypes);
  const createdAt = getRandomDate(2022, 2023);
  const updatedAt = new Date(
    new Date(createdAt).getTime() +
      Math.random() * (new Date() - new Date(createdAt))
  ).toISOString();

  const namePrefix = getRandomElement(routerType.namePrefix);
  const nameSuffix = getRandomElement(routerType.nameSuffix);
  const name = `${namePrefix} ${nameSuffix}`;

  return {
    id: `r-${String(id).padStart(6, "0")}`,
    name,
    type: routerType.type,
    createdAt,
    updatedAt,
    coordinates: generateRandomCoordinates(),
    ...routerType.generateSpecificFields(),
  };
}

function generateRouterData(count = 100) {
  const routers = [];

  for (let i = 1; i <= count; i++) {
    routers.push(generateRouter(i));
  }

  return { routers };
}

const routerData = generateRouterData(2000);
fs.writeFileSync("db.json", JSON.stringify(routerData, null, 2));

console.log(`Generated db.json with ${routerData.routers.length} routers.`);
