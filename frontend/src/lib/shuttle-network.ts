export type ShuttleServiceType = 'campus_loop' | 'inter_campus';
export type ShuttleTelemetryStatus = 'not_connected';

export type ShuttleStop = {
  id: string;
  nameTr: string;
  nameEn: string;
  campus: string;
};

export type ShuttleRoute = {
  id: string;
  serviceType: ShuttleServiceType;
  nameTr: string;
  nameEn: string;
  shortLabel: string;
  stopIds: string[];
  officialScheduleUrl: string;
  distanceKmEstimate: number;
  accessibilityNoteTr: string;
  accessibilityNoteEn: string;
  telemetryStatus: ShuttleTelemetryStatus;
  capacity: null;
  occupancy: null;
};

export type ShuttleNetworkSnapshot = {
  generatedAt: string;
  source: {
    name: string;
    url: string;
    provenance: 'official_public_schedule';
  };
  serviceTypes: Array<{
    id: ShuttleServiceType;
    labelTr: string;
    labelEn: string;
    descriptionTr: string;
    descriptionEn: string;
  }>;
  stops: ShuttleStop[];
  routes: ShuttleRoute[];
  truthBoundary: {
    tr: string;
    en: string;
  };
  climateModel: {
    status: 'scenario_estimate';
    carEmissionKgCo2ePerVehicleKm: number;
    assumedCarOccupancy: number;
    noteTr: string;
    noteEn: string;
  };
};

export const OFFICIAL_SHUTTLE_SOURCE = 'https://mekik.bogazici.edu.tr/';

export const shuttleStops: ShuttleStop[] = [
  { id: 'south-square', nameTr: 'Güney Meydan', nameEn: 'South Square', campus: 'Güney / South' },
  { id: 'etiler-gate', nameTr: 'Etiler Kapı', nameEn: 'Etiler Gate', campus: 'Güney / South' },
  { id: 'north-campus', nameTr: 'Kuzey Kampüs', nameEn: 'North Campus', campus: 'Kuzey / North' },
  { id: 'hisar-campus', nameTr: 'Hisar Kampüs', nameEn: 'Hisar Campus', campus: 'Hisar' },
  { id: 'anadolu-hisari', nameTr: 'Anadolu Hisarı Kampüsü', nameEn: 'Anadolu Hisarı Campus', campus: 'Anadolu Hisarı' },
  { id: 'kandilli-campus', nameTr: 'Kandilli Kampüsü', nameEn: 'Kandilli Campus', campus: 'Kandilli' },
  { id: 'kilyos-campus', nameTr: 'Kilyos Kampüsü', nameEn: 'Kilyos Campus', campus: 'Kilyos' },
  { id: 'zekeriyakoy', nameTr: 'Zekeriyaköy', nameEn: 'Zekeriyaköy', campus: 'Off-campus connection' },
];

export const shuttleRoutes: ShuttleRoute[] = [
  {
    id: 'south-etiler-ring',
    serviceType: 'campus_loop',
    nameTr: 'Güney Meydan ⇄ Etiler Kapı Ring',
    nameEn: 'South Square ⇄ Etiler Gate Loop',
    shortLabel: 'GÜNEY · ETİLER',
    stopIds: ['south-square', 'etiler-gate'],
    officialScheduleUrl: OFFICIAL_SHUTTLE_SOURCE,
    distanceKmEstimate: 1.2,
    accessibilityNoteTr: 'Araç erişilebilirliği için resmî mekik bilgisini kontrol edin.',
    accessibilityNoteEn: 'Check the official shuttle information for vehicle accessibility.',
    telemetryStatus: 'not_connected',
    capacity: null,
    occupancy: null,
  },
  {
    id: 'south-north-loop',
    serviceType: 'campus_loop',
    nameTr: 'Güney Meydan ⇄ Kuzey Kampüs',
    nameEn: 'South Square ⇄ North Campus',
    shortLabel: 'GÜNEY · KUZEY',
    stopIds: ['south-square', 'north-campus'],
    officialScheduleUrl: OFFICIAL_SHUTTLE_SOURCE,
    distanceKmEstimate: 1.8,
    accessibilityNoteTr: 'Araç erişilebilirliği için resmî mekik bilgisini kontrol edin.',
    accessibilityNoteEn: 'Check the official shuttle information for vehicle accessibility.',
    telemetryStatus: 'not_connected',
    capacity: null,
    occupancy: null,
  },
  {
    id: 'south-hisar',
    serviceType: 'inter_campus',
    nameTr: 'Güney Meydan → Etiler Kapı → Hisar Kampüs',
    nameEn: 'South Square → Etiler Gate → Hisar Campus',
    shortLabel: 'GÜNEY · HİSAR',
    stopIds: ['south-square', 'etiler-gate', 'hisar-campus'],
    officialScheduleUrl: OFFICIAL_SHUTTLE_SOURCE,
    distanceKmEstimate: 3.4,
    accessibilityNoteTr: 'Araç erişilebilirliği için resmî mekik bilgisini kontrol edin.',
    accessibilityNoteEn: 'Check the official shuttle information for vehicle accessibility.',
    telemetryStatus: 'not_connected',
    capacity: null,
    occupancy: null,
  },
  {
    id: 'etiler-anadolu-kandilli',
    serviceType: 'inter_campus',
    nameTr: 'Etiler Kapı → Anadolu Hisarı → Kandilli',
    nameEn: 'Etiler Gate → Anadolu Hisarı → Kandilli',
    shortLabel: 'ETİLER · ANADOLU · KANDİLLİ',
    stopIds: ['etiler-gate', 'anadolu-hisari', 'kandilli-campus'],
    officialScheduleUrl: OFFICIAL_SHUTTLE_SOURCE,
    distanceKmEstimate: 15.2,
    accessibilityNoteTr: 'Araç erişilebilirliği için resmî mekik bilgisini kontrol edin.',
    accessibilityNoteEn: 'Check the official shuttle information for vehicle accessibility.',
    telemetryStatus: 'not_connected',
    capacity: null,
    occupancy: null,
  },
  {
    id: 'etiler-kilyos',
    serviceType: 'inter_campus',
    nameTr: 'Etiler Kapı ⇄ Kilyos Kampüsü',
    nameEn: 'Etiler Gate ⇄ Kilyos Campus',
    shortLabel: 'ETİLER · KİLYOS',
    stopIds: ['etiler-gate', 'kilyos-campus'],
    officialScheduleUrl: OFFICIAL_SHUTTLE_SOURCE,
    distanceKmEstimate: 32,
    accessibilityNoteTr: 'Araç erişilebilirliği için resmî mekik bilgisini kontrol edin.',
    accessibilityNoteEn: 'Check the official shuttle information for vehicle accessibility.',
    telemetryStatus: 'not_connected',
    capacity: null,
    occupancy: null,
  },
  {
    id: 'anadolu-kilyos',
    serviceType: 'inter_campus',
    nameTr: 'Anadolu Hisarı → Kilyos Kampüsü',
    nameEn: 'Anadolu Hisarı → Kilyos Campus',
    shortLabel: 'ANADOLU · KİLYOS',
    stopIds: ['anadolu-hisari', 'kilyos-campus'],
    officialScheduleUrl: OFFICIAL_SHUTTLE_SOURCE,
    distanceKmEstimate: 40,
    accessibilityNoteTr: 'Araç erişilebilirliği için resmî mekik bilgisini kontrol edin.',
    accessibilityNoteEn: 'Check the official shuttle information for vehicle accessibility.',
    telemetryStatus: 'not_connected',
    capacity: null,
    occupancy: null,
  },
  {
    id: 'kilyos-zekeriyakoy',
    serviceType: 'inter_campus',
    nameTr: 'Kilyos Kampüsü ⇄ Zekeriyaköy',
    nameEn: 'Kilyos Campus ⇄ Zekeriyaköy',
    shortLabel: 'KİLYOS · ZEKERİYAKÖY',
    stopIds: ['kilyos-campus', 'zekeriyakoy'],
    officialScheduleUrl: OFFICIAL_SHUTTLE_SOURCE,
    distanceKmEstimate: 8,
    accessibilityNoteTr: 'Araç erişilebilirliği için resmî mekik bilgisini kontrol edin.',
    accessibilityNoteEn: 'Check the official shuttle information for vehicle accessibility.',
    telemetryStatus: 'not_connected',
    capacity: null,
    occupancy: null,
  },
];

export function estimateAvoidedCarImpact(route: ShuttleRoute, passengerTrips: number) {
  const safePassengerTrips = Math.max(0, Math.round(passengerTrips));
  const assumedCarOccupancy = 1.2;
  const carEmissionKgCo2ePerVehicleKm = 0.171;
  const avoidedVehicleKm = (route.distanceKmEstimate * safePassengerTrips) / assumedCarOccupancy;
  const avoidedCarKgCo2eEstimate = avoidedVehicleKm * carEmissionKgCo2ePerVehicleKm;

  return {
    passengerTrips: safePassengerTrips,
    avoidedVehicleKm: Number(avoidedVehicleKm.toFixed(1)),
    avoidedCarKgCo2eEstimate: Number(avoidedCarKgCo2eEstimate.toFixed(1)),
    methodology: 'scenario_estimate' as const,
  };
}

export function getShuttleNetworkSnapshot(): ShuttleNetworkSnapshot {
  return {
    generatedAt: new Date().toISOString(),
    source: {
      name: 'Boğaziçi Üniversitesi Mekik Bilgi Sistemi',
      url: OFFICIAL_SHUTTLE_SOURCE,
      provenance: 'official_public_schedule',
    },
    serviceTypes: [
      {
        id: 'campus_loop',
        labelTr: 'Kampüs içi ring',
        labelEn: 'Campus loop',
        descriptionTr: 'Kısa mesafeli ana kampüs hareketleri için ring ve yakın kampüs bağlantıları.',
        descriptionEn: 'Loop and nearby-campus connections for short main-campus movements.',
      },
      {
        id: 'inter_campus',
        labelTr: 'Kampüsler arası mekik',
        labelEn: 'Inter-campus shuttle',
        descriptionTr: 'Hisar, Kandilli, Anadolu Hisarı ve Kilyos gibi yerleşkeler arasında planlı ulaşım.',
        descriptionEn: 'Scheduled mobility between sites such as Hisar, Kandilli, Anadolu Hisarı and Kilyos.',
      },
    ],
    stops: shuttleStops,
    routes: shuttleRoutes,
    truthBoundary: {
      tr: 'BOUNCAMPUS şu anda mekik GPS verisine, gerçek zamanlı doluluk sensörüne veya doğrulanmış araç kapasitesine bağlı değildir. Sefer saatleri için resmî Boğaziçi kaynağı esas alınır; ETA ve doluluk canlı veri olarak sunulmaz.',
      en: 'BOUNCAMPUS is not currently connected to shuttle GPS, real-time occupancy sensors, or verified vehicle capacity. The official Boğaziçi source remains authoritative for departure times; ETA and occupancy are not presented as live data.',
    },
    climateModel: {
      status: 'scenario_estimate',
      carEmissionKgCo2ePerVehicleKm: 0.171,
      assumedCarOccupancy: 1.2,
      noteTr: 'İklim etkisi, seçilen yolculukların özel araç yerine mevcut mekikle yapıldığı varsayımına dayanan senaryo tahminidir; mekik aracının net operasyonel emisyonu değildir.',
      noteEn: 'Climate impact is a scenario estimate assuming selected trips replace private-car travel; it is not the shuttle vehicle’s net operational emissions.',
    },
  };
}
