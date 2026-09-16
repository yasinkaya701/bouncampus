import type { ActionItem } from './types';
import type { Locale } from './i18n';

const ACTION_TITLES: Record<string, { tr: string; en: string }> = {
  'ACT-01': { tr: 'New Hall üst kat kullanımını yeniden değerlendir', en: 'Review upper-floor use in New Hall' },
  'ACT-02': { tr: 'Kuzey yemekhane üretim planını talebe göre gözden geçir', en: 'Review North Cafeteria production against demand' },
  'ACT-03': { tr: 'Perkins Hall derslik konsolidasyonunu değerlendir', en: 'Evaluate classroom consolidation in Perkins Hall' },
  'ACT-04': { tr: 'Kare Blok enerji senaryosunu operatörle doğrula', en: 'Validate the Kare Block energy scenario with an operator' },
  'ACT-05': { tr: 'Kütüphane ısıtma varsayımını sahada doğrula', en: 'Field-check the library heating assumption' },
};

export function actionTitle(action: ActionItem, locale: Locale) {
  return ACTION_TITLES[action.id]?.[locale] ?? action.title;
}
