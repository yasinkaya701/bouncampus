export type PhotogrammetryCampus = 'north' | 'hisar' | 'ucaksavar' | 'kandilli' | 'anadolu' | 'kilyos';

export type PhotogrammetryAsset = {
  id: string;
  campus: PhotogrammetryCampus;
  titleTr: string;
  titleEn: string;
  provider: 'Sketchfab';
  author: string;
  modelId: string;
  sourceUrl: string;
  embedUrl: string;
  coverageTr: string;
  coverageEn: string;
  redistribution: 'external-embed-only';
  evidence: string[];
};

const sketchfabEmbed = (modelId: string) =>
  `https://sketchfab.com/models/${modelId}/embed?autostart=1&ui_theme=dark&ui_infos=0&ui_watermark=1`;

/**
 * Provider-hosted Boğaziçi photogrammetry references.
 *
 * Important: we intentionally do not vendor the downloadable model binaries here.
 * The public pages expose embeddable photogrammetry, but redistribution/download
 * rights were not independently verified for this repository. Keeping the binary
 * at the provider boundary lets us use the public embed while preserving provenance.
 */
export const PHOTOGRAMMETRY_ASSETS: PhotogrammetryAsset[] = [
  {
    id: 'north-campus-main',
    campus: 'north',
    titleTr: 'Kuzey Kampüs — 1-2-3-4-5 Yerleşke',
    titleEn: 'North Campus — 1-2-3-4-5 Campus',
    provider: 'Sketchfab',
    author: 'Havadan Harita / Buğrahan Yeni',
    modelId: '7ee0a7f38d434c519be728a3ab493722',
    sourceUrl: 'https://sketchfab.com/models/7ee0a7f38d434c519be728a3ab493722/embed',
    embedUrl: sketchfabEmbed('7ee0a7f38d434c519be728a3ab493722'),
    coverageTr: 'Kuzey Kampüs ana yerleşke fotogrametrisi.',
    coverageEn: 'Photogrammetry of the main North Campus area.',
    redistribution: 'external-embed-only',
    evidence: [
      'https://sketchfab.com/havadanharita/collections/bogazici-universitesi-kuzey-hisar-kampus-5181ff7662c8440db5d2b292b34a1f19',
      'https://harita.bogazici.edu.tr/',
    ],
  },
  {
    id: 'north-campus-dorms',
    campus: 'north',
    titleTr: 'Kuzey Kampüs — 6-7 Yurtlar',
    titleEn: 'North Campus — Dormitories 6-7',
    provider: 'Sketchfab',
    author: 'Havadan Harita / Buğrahan Yeni',
    modelId: 'd153dab298bd472787c6896063f9a9b7',
    sourceUrl: 'https://sketchfab.com/3d-models/6-7-bogazici-universitesi-kuzey-kampus-yurtlar-d153dab298bd472787c6896063f9a9b7',
    embedUrl: sketchfabEmbed('d153dab298bd472787c6896063f9a9b7'),
    coverageTr: 'Kuzey Kampüs yurt yapıları fotogrametrisi.',
    coverageEn: 'Photogrammetry of North Campus dormitory buildings.',
    redistribution: 'external-embed-only',
    evidence: [
      'https://sketchfab.com/havadanharita/collections/bogazici-universitesi-kuzey-hisar-kampus-5181ff7662c8440db5d2b292b34a1f19',
      'https://harita.bogazici.edu.tr/',
    ],
  },
  {
    id: 'ucaksavar-superdorm-sports',
    campus: 'ucaksavar',
    titleTr: 'Uçaksavar — Superdorm & Kapalı Spor Salonu',
    titleEn: 'Uçaksavar — Superdorm & Indoor Sports Hall',
    provider: 'Sketchfab',
    author: 'Havadan Harita / Buğrahan Yeni',
    modelId: '58f91e285e0c4a4dafff412ccc553ecf',
    sourceUrl: 'https://sketchfab.com/3d-models/bogazici-uni-ucaksavar-kampusu-superdormkss-58f91e285e0c4a4dafff412ccc553ecf',
    embedUrl: sketchfabEmbed('58f91e285e0c4a4dafff412ccc553ecf'),
    coverageTr: 'Superdorm ve kapalı spor salonu çevresi fotogrametrisi.',
    coverageEn: 'Photogrammetry around Superdorm and the indoor sports hall.',
    redistribution: 'external-embed-only',
    evidence: [
      'https://webdosya.csb.gov.tr/db/kamuguclendirme/menu/isgpl_faz_02_rev_20240503101742.pdf',
      'https://harita.bogazici.edu.tr/',
    ],
  },
  {
    id: 'kandilli-new-geophysics',
    campus: 'kandilli',
    titleTr: 'Kandilli — Yeni Jeofizik Binası',
    titleEn: 'Kandilli — New Geophysics Building',
    provider: 'Sketchfab',
    author: 'Havadan Harita / Buğrahan Yeni',
    modelId: '364f2ef47974416baa046626efae4fa0',
    sourceUrl: 'https://sketchfab.com/3d-models/bogazici-uni-kandilli-rs-yeni-jeofizik-binas-364f2ef47974416baa046626efae4fa0',
    embedUrl: sketchfabEmbed('364f2ef47974416baa046626efae4fa0'),
    coverageTr: 'Kandilli Rasathanesi Yeni Jeofizik Binası fotogrametrisi.',
    coverageEn: 'Photogrammetry of the New Geophysics Building at Kandilli Observatory.',
    redistribution: 'external-embed-only',
    evidence: [
      'https://webdosya.csb.gov.tr/db/kamuguclendirme/menu/jeofizik_isg_18_20240429121846.pdf',
    ],
  },
  {
    id: 'anadolu-indoor-pool',
    campus: 'anadolu',
    titleTr: 'Anadolu Hisarı — Kapalı Yüzme Havuzu',
    titleEn: 'Anadolu Hisarı — Indoor Swimming Pool',
    provider: 'Sketchfab',
    author: 'Havadan Harita / Buğrahan Yeni',
    modelId: 'bc509269e0c747deb58b4a7b369fba0b',
    sourceUrl: 'https://sketchfab.com/3d-models/bogazici-unianadoluhisar-kapal-yuzme-havuzu-bc509269e0c747deb58b4a7b369fba0b',
    embedUrl: sketchfabEmbed('bc509269e0c747deb58b4a7b369fba0b'),
    coverageTr: 'Anadolu Hisarı Kampüsü kapalı yüzme havuzu fotogrametrisi.',
    coverageEn: 'Photogrammetry of the indoor swimming pool at Anadolu Hisarı Campus.',
    redistribution: 'external-embed-only',
    evidence: ['https://harita.bogazici.edu.tr/'],
  },
  {
    id: 'kilyos-dormitory',
    campus: 'kilyos',
    titleTr: 'Kilyos — Yurt Binası',
    titleEn: 'Kilyos — Dormitory Building',
    provider: 'Sketchfab',
    author: 'Havadan Harita / Buğrahan Yeni',
    modelId: '39aa2add49de4877bedf68e7d618e097',
    sourceUrl: 'https://sketchfab.com/3d-models/bogazici-uni-kilyos-kampusu-yurt-binas-39aa2add49de4877bedf68e7d618e097',
    embedUrl: sketchfabEmbed('39aa2add49de4877bedf68e7d618e097'),
    coverageTr: 'Kilyos / Sarıtepe Kampüsü yurt binası fotogrametrisi.',
    coverageEn: 'Photogrammetry of a dormitory building at Kilyos / Sarıtepe Campus.',
    redistribution: 'external-embed-only',
    evidence: ['https://webdosya.csb.gov.tr/db/kamuguclendirme/menu/isgpl_faz_02_rev_20231005104413.pdf'],
  },
];

export const PHOTOGRAMMETRY_PROVENANCE_NOTE = {
  tr: 'Bu sahneler sağlayıcı tarafından barındırılan fotogrametri embedleridir. İndirilebilir model dosyaları, yeniden dağıtım lisansı ayrıca doğrulanmadığı için repoya kopyalanmaz.',
  en: 'These scenes are provider-hosted photogrammetry embeds. Downloadable model binaries are not copied into the repository because redistribution rights have not been independently verified.',
};
