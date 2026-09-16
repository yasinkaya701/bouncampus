export type CampusLocale = 'tr' | 'en';

type DirectoryEntry = {
  tr: string;
  en: string;
  code?: string;
  officialCode?: boolean;
};

const DIRECTORY: Record<string, DirectoryEntry> = {
  'B-SOUTH-TB': { tr: 'Anderson Hall — Fen-Edebiyat Fakültesi', en: 'Anderson Hall — Faculty of Arts and Sciences', code: 'TB', officialCode: true },
  'B-SOUTH-IB': { tr: 'Washburn Hall — İktisadi ve İdari Bilimler Fakültesi', en: 'Washburn Hall — Faculty of Economics and Administrative Sciences', code: 'İB', officialCode: true },
  'B-SOUTH-M': { tr: 'Perkins Hall — Mühendislik Fakültesi', en: 'Perkins Hall — Faculty of Engineering', code: 'M', officialCode: true },
  'B-SOUTH-ALH': { tr: 'Albert Long Hall', en: 'Albert Long Hall' },
  'B-SOUTH-GH': { tr: 'Gates Hall — Genel İdare Binası', en: 'Gates Hall — General Administration Building' },
  'B-SOUTH-HH': { tr: 'Hamlin Hall', en: 'Hamlin Hall', code: 'HH', officialCode: true },
  'B-SOUTH-OFB': { tr: 'Öğrenci Faaliyetleri Binası', en: 'Student Activities Building' },
  'B-SOUTH-NB': { tr: 'Natuk Birkan Binası', en: 'Natuk Birkan Building', code: 'NB', officialCode: true },
  'B-SOUTH-JF': { tr: 'John Freely Binası', en: 'John Freely Hall', code: 'JF', officialCode: true },
  'B-SOUTH-GY': { tr: 'Güney Kampüs Yemekhanesi', en: 'South Campus Cafeteria' },
  'B-NORTH-KB': { tr: 'Fen ve Mühendislik Binası — Kare Blok', en: 'Science and Engineering Building — Kare Block', code: 'KB', officialCode: true },
  'B-NORTH-NH': { tr: 'Yeni Bina — New Hall', en: 'New Hall', code: 'NH', officialCode: true },
  'B-NORTH-LIB': { tr: 'Aptullah Kuran Kütüphanesi', en: 'Aptullah Kuran Library' },
  'B-NORTH-KY': { tr: 'Kuzey Kampüs Yemekhanesi', en: 'North Campus Cafeteria' },
  'B-NORTH-BM': { tr: 'Bilgisayar Mühendisliği Binası', en: 'Computer Engineering Building', code: 'BM', officialCode: true },
  'B-NORTH-EF': { tr: 'Eğitim Fakültesi', en: 'Faculty of Education', code: 'EF', officialCode: true },
  'B-NORTH-YD': { tr: 'YADYOK II', en: 'School of Foreign Languages II', code: 'KYD', officialCode: true },
  'B-NORTH-ETA': { tr: 'ETA-B Blok', en: 'ETA-B Block', code: 'ET', officialCode: true },
  'B-NORTH-KP': { tr: 'Kuzey Park Binası', en: 'North Park Building', code: 'KP', officialCode: true },
  'B-NORTH-SBU': { tr: 'SineBU', en: 'SineBU' },
  'B-NORTH-Y34': { tr: '3. ve 4. Kuzey Yurtları', en: 'North Dormitories 3 and 4' },
};

export const officialBuildingCodeSource = 'https://bogazici.edu.tr/tr/pages/derslik-kisaltmalari-ve-acilimlari/127';
export const officialSouthCampusSource = 'https://bogazici.edu.tr/tr/campuses/guney-kampus/2';
export const officialNorthCampusSource = 'https://bogazici.edu.tr/en/campuses/north-campus/3';

export function presentBuilding(building: { id: string; name: string; code: string }, locale: CampusLocale) {
  const entry = DIRECTORY[building.id];
  return {
    name: entry ? (locale === 'tr' ? entry.tr : entry.en) : building.name,
    code: entry?.code ?? building.code,
    officialCode: Boolean(entry?.officialCode),
  };
}

export function buildingTypeLabel(type: string, locale: CampusLocale) {
  const labels: Record<string, [string, string]> = {
    Academic: ['Akademik', 'Academic'],
    Cultural: ['Kültür', 'Cultural'],
    Admin: ['İdari', 'Administrative'],
    Dorm: ['Yurt', 'Dormitory'],
    'Student Center': ['Öğrenci alanı', 'Student space'],
    Dining: ['Yemekhane', 'Dining'],
    Library: ['Kütüphane', 'Library'],
    Research: ['Araştırma', 'Research'],
  };
  const match = labels[type];
  return match ? match[locale === 'tr' ? 0 : 1] : type;
}
